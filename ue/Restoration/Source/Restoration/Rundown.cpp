#include "Rundown.h"
#include "RestorationClock.h"
#include "RestorationState.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/SpectatorPawn.h"
#include "Kismet/GameplayStatics.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"

DEFINE_LOG_CATEGORY_STATIC(LogRundown, Log, All);

namespace
{
	constexpr float M = 100.0f; // meters -> uu
}

ARundown::ARundown()
{
	PrimaryActorTick.bCanEverTick = true;
	RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	// canon anchors: TAPE LIBRARY (0,-16) · STUDIO A (-15.5,-30) · PATCH BAY (-5.5,-29.5)
	SegmentAnchors = { FVector(0, -16 * M, 0), FVector(-15.5f * M, -30 * M, 0),
	                   FVector(-5.5f * M, -29.5f * M, 0) };
	SegmentNames = { TEXT("STORY CORNER"), TEXT("THE SONG"), TEXT("CRAFT TIME") };
}

void ARundown::BeginPlay()
{
	Super::BeginPlay();
	SetActorLocation(SegmentAnchors[SegIdx]);
	Target = SegmentAnchors[SegIdx];

	// doors from the same table the world was stamped from
	const FString DoorsCsv = FPaths::Combine(FPaths::ProjectDir(), TEXT("Data/Doors.csv"));
	TArray<FString> Lines;
	if (FFileHelper::LoadFileToStringArray(Lines, *DoorsCsv))
	{
		for (int32 i = 1; i < Lines.Num(); ++i)
		{
			TArray<FString> Cols;
			Lines[i].ParseIntoArray(Cols, TEXT(","), false);
			if (Cols.Num() >= 5)
			{
				DoorPositions.Add(FVector(FCString::Atof(*Cols[2]) * M,
				                          FCString::Atof(*Cols[3]) * M, 0));
			}
		}
	}
	UE_LOG(LogRundown, Log, TEXT("Rundown up: %d anchors, %d doors"),
	       SegmentAnchors.Num(), DoorPositions.Num());

	if (URestorationClock* Clock = GetWorld()->GetSubsystem<URestorationClock>())
	{
		Clock->OnPhaseChanged.AddUObject(this, &ARundown::OnPhaseChanged);
	}
	if (UGameInstance* GI = GetWorld()->GetGameInstance())
	{
		State = GI->GetSubsystem<URestorationState>();
	}
	if (State)
	{
		// noise_event -> ReportNoise, exactly as rundown.gd connects it
		State->OnNoise.AddLambda([this](const FVector& P, float /*R*/) { ReportNoise(P); });
	}
	if (bTestLoopFns && State)
	{
		// day/night driver: day 1 -> morning -> day 2 tape 2 -> morning -> day 3 run_complete
		State->SetNight(false);
		State->SetNight(true);
		State->SetNight(false);
		State->LogLineTest(FString::Printf(TEXT("DAYNIGHT day=%d tape=%d run_complete=%d"),
		                                   State->Day, State->CurrentTape, State->bRunComplete ? 1 : 0));
		// stations + the sign flow: register S2, note paper, sign, check respawn + relocate
		State->RegisterStation(TEXT("S2"), FVector(700, -3100, 0));
		const int32 PaperBefore = State->PaperFor(TEXT("S2"));
		const bool bSigned = State->SignLog(TEXT("S2"));
		const FVector Rp = State->RespawnPoint();
		State->LogLineTest(FString::Printf(
			TEXT("SIGNFLOW signed=%d paper %d->%d respawn=%s seg_now=%d"),
			bSigned ? 1 : 0, PaperBefore, State->PaperFor(TEXT("S2")),
			*Rp.ToCompactString(), SegIdx));
		State->MarkRead(TEXT("D01"));
		State->TakeKey(TEXT("QUIET ROOM"), TEXT("the dead-room key"));
	}
	if (State)
	{
		if (bTestForceNight) { State->bIsNight = true; }
		if (bTestForceAF) { State->bAfActive = true; }
		if (bTestForceRecording) { State->bRecording = true; }
		if (bTestSaveRoundtrip)
		{
			// a value of every container kind: int, bool, float, string,
			// map entry, struct array, int array
			State->Strikes = 7;
			State->SeanceWear = 72.5f;
			State->bAfTaught = true;
			State->Decision = TEXT("HIS HAND");
			State->Paper.Add(TEXT("S3"), 1);
			FRestorationSignature Sig; Sig.Station = TEXT("S2"); Sig.Tape = 4;
			Sig.Signed = TEXT("TODAY"); State->Signatures.Add(Sig);
			State->LelandAnswers.Add(1023);
			State->SaveToSlot(TEXT("roundtrip_test"));
			// clobber every field, then load and compare
			State->Strikes = 0; State->SeanceWear = 0; State->bAfTaught = false;
			State->Decision = TEXT(""); State->Paper.Add(TEXT("S3"), 3);
			State->Signatures.Reset(); State->LelandAnswers.Reset();
			const bool bOk = State->LoadFromSlot(TEXT("roundtrip_test"));
			const bool bMatch = bOk && State->Strikes == 7
				&& FMath::IsNearlyEqual(State->SeanceWear, 72.5f) && State->bAfTaught
				&& State->Decision == TEXT("HIS HAND")
				&& State->Paper.FindRef(TEXT("S3")) == 1
				&& State->Signatures.Num() == 1 && State->Signatures[0].Station == TEXT("S2")
				&& State->LelandAnswers.Num() == 1 && State->LelandAnswers[0] == 1023;
			LogLine(FString::Printf(
				TEXT("SAVE-ROUNDTRIP v16 ok=%d match=%d strikes=%d wear=%.1f taught=%d decision=%s paperS3=%d sigs=%d leland=%d"),
				bOk ? 1 : 0, bMatch ? 1 : 0, State->Strikes, State->SeanceWear,
				State->bAfTaught ? 1 : 0, *State->Decision,
				State->Paper.FindRef(TEXT("S3")), State->Signatures.Num(),
				State->LelandAnswers.Num()));
			// leave clean for the AF test that follows
			State->Strikes = 0; State->SeanceWear = 0; State->bAfTaught = false;
			State->Decision = TEXT(""); State->Signatures.Reset();
			State->LelandAnswers.Reset(); State->Paper.Add(TEXT("S3"), 3);
		}
	}
}

AActor* ARundown::ResolveTarget() const
{
	if (APawn* P = UGameplayStatics::GetPlayerPawn(GetWorld(), 0))
	{
		if (!P->IsA(ASpectatorPawn::StaticClass()))
		{
			return P;
		}
	}
	TArray<AActor*> Tagged;
	UGameplayStatics::GetAllActorsWithTag(GetWorld(), FName("RundownTestTarget"), Tagged);
	return Tagged.Num() > 0 ? Tagged[0] : nullptr;
}

void ARundown::ReportNoise(const FVector& WorldPos)
{
	HeardPos = WorldPos;
	HeardT = GetWorld()->GetTimeSeconds();
}

void ARundown::OnPhaseChanged(bool bNowOnAir)
{
	if (bNowOnAir)
	{
		bWarned = false;
		// savor rule + profile widening port with the director (TODO(0.8));
		// the strikes>=3 widening is canon and lives here already
		StrikeR = (StrikesNow() >= 3) ? 2.6f : StrikeRadius;
		WarnR = WarnRadius;
		return;
	}
	// BREAK: relocation grammar, verbatim order — heard noise wins, else cycle
	const float Now = GetWorld()->GetTimeSeconds();
	if (Now - HeardT < 12.0f)
	{
		int32 Best = SegIdx;
		float BestD = TNumericLimits<float>::Max();
		for (int32 i = 0; i < SegmentAnchors.Num(); ++i)
		{
			const float Dh = FVector::Dist(SegmentAnchors[i], HeardPos);
			if (Dh < BestD) { BestD = Dh; Best = i; }
		}
		SegIdx = Best;
		LogLine(FString::Printf(TEXT("RELOCATE toward heard noise at %s -> segment %d"),
		                        *HeardPos.ToString(), SegIdx));
	}
	else
	{
		SegIdx = (SegIdx + 1) % SegmentAnchors.Num();
		LogLine(FString::Printf(TEXT("RELOCATE cycle -> segment %d (profile UNKNOWN)"), SegIdx));
	}
	Target = SegmentAnchors[SegIdx];
}

bool ARundown::DoorFoldCheck(float Now)
{
	if (FoldT > 0.0f)
	{
		return true;
	}
	for (int32 i = 0; i < DoorPositions.Num(); ++i)
	{
		if (FVector::Dist2D(GetActorLocation(), DoorPositions[i]) < AfDoorNear * M)
		{
			const float* Last = FoldCool.Find(i);
			if (!Last || Now - *Last > 6.0f)
			{
				FoldCool.Add(i, Now);
				FoldT = AfFoldSeconds; // the 2.2s toll — the player's counterplay (LAW 11)
				return true;
			}
		}
	}
	return false;
}

void ARundown::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	const float Now = GetWorld()->GetTimeSeconds();
	if (StrikeCooldown > 0.0f)
	{
		StrikeCooldown -= DeltaSeconds;
	}
	if (FoldT > 0.0f)
	{
		FoldT -= DeltaSeconds;
		return;
	}

	// test scaffolding: scripted recording cutoff
	if (TestRecordingOffAfter > 0.0f && State && State->bRecording)
	{
		TestClock += DeltaSeconds;
		if (TestClock >= TestRecordingOffAfter)
		{
			State->bRecording = false;
			LogLine(TEXT("TEST recording off"));
		}
	}

	// ---- THE AF LAYER (tally contract, LAW 10) --------------------------
	if (State && State->bAfActive)
	{
		AActor* Prey = ResolveTarget();
		if (State->bRecording && Prey)
		{
			SetActorHiddenInGame(false); // he shows for the contract
			const float Pd = FVector::Dist(GetActorLocation(), Prey->GetActorLocation()) / M;
			if (State->InDeadRoom(Prey->GetActorLocation()))
			{
				// he holds at the felt door (LAW 11)
				const FVector DeadDoor(1900.0f, 0.0f, 0.0f);
				if (FVector::Dist(GetActorLocation(), DeadDoor) > 0.6f * M)
				{
					if (DoorFoldCheck(Now)) { return; }
					SetActorLocation(FMath::VInterpConstantTo(GetActorLocation(), DeadDoor,
					                                          DeltaSeconds, AfApproachSpeed * M));
				}
				else if (!bDeadroomLine)
				{
					bDeadroomLine = true;
					LogLine(TEXT("AF holds at the felt door"));
				}
				return;
			}
			if (Pd > AfLoomDist)
			{
				if (DoorFoldCheck(Now)) { return; }
				SetActorLocation(FMath::VInterpConstantTo(GetActorLocation(),
				                                          Prey->GetActorLocation(),
				                                          DeltaSeconds, AfApproachSpeed * M));
			}
			else if (!bAfSeenOnce)
			{
				bAfSeenOnce = true;
				LogLine(FString::Printf(TEXT("AF loom d=%.1f (the jaw works its lever)"), Pd));
			}
			AfCool = -100.0f;
			return;
		}
		// tally cooled: the countdown, then the arithmetic (never betrayal)
		if (Prey && AfCool < -50.0f && !State->bRecording && !State->bIsNight
		        && !IsHidden())
		{
			AfCool = State->bAfTaught ? AfCoolSeconds : 4.0f;
			if (!State->bAfTaught)
			{
				State->bAfTaught = true;
				LogLine(TEXT("AF tally cools (taught)"));
			}
			else
			{
				LogLine(TEXT("AF tally cools"));
			}
		}
		if (AfCool > -50.0f && !State->bIsNight)
		{
			AfCool -= DeltaSeconds;
			if (AfCool <= 0.0f)
			{
				if (Prey && FVector::Dist(GetActorLocation(), Prey->GetActorLocation()) / M
				        < StrikeR + 0.4f)
				{
					LogLine(TEXT("STRIKE af tally-cool"));
					State->Strike(Prey);
				}
				AfCool = -100.0f;
				SetActorHiddenInGame(true); // gone until the next contract
				SetActorLocation(SegmentAnchors[SegIdx]);
			}
			return;
		}
	}

	// the night gate comes AFTER the AF layer, as the spec orders it
	const bool bNight = State ? State->bIsNight : true;
	if (!bNight)
	{
		return;
	}

	URestorationClock* Clock = GetWorld()->GetSubsystem<URestorationClock>();
	const bool bOnAir = Clock ? Clock->IsOnAir() : true;

	if (!bOnAir)
	{
		if (DoorFoldCheck(Now))
		{
			return;
		}
		const FVector Next = FMath::VInterpConstantTo(GetActorLocation(), Target,
		                                              DeltaSeconds, MoveSpeed * M);
		SetActorLocation(Next);
		return;
	}

	AActor* Prey = ResolveTarget();
	if (!Prey)
	{
		return;
	}
	const float D = FVector::Dist(GetActorLocation(), Prey->GetActorLocation()) / M;
	if (!bSpawnLogged)
	{
		bSpawnLogged = true;
		LogLine(FString::Printf(TEXT("DEBUG spawn me=%s prey=%s(%s) d=%.1f onair=%d"),
		                        *GetActorLocation().ToCompactString(),
		                        *Prey->GetName(), *Prey->GetActorLocation().ToCompactString(),
		                        D, bOnAir ? 1 : 0));
	}
	if (D < StrikeR && StrikeCooldown <= 0.0f)
	{
		// no-strike-thru-wall check (invariant I02): ray at +1m
		bool bThru = false;
		FHitResult Hit;
		FCollisionQueryParams Q;
		Q.AddIgnoredActor(Prey);
		Q.AddIgnoredActor(this);
		if (GetWorld()->LineTraceSingleByChannel(
		        Hit, GetActorLocation() + FVector(0, 0, M),
		        Prey->GetActorLocation() + FVector(0, 0, M), ECC_Visibility, Q))
		{
			bThru = Hit.GetActor() != Prey;
		}
		LogLine(FString::Printf(TEXT("STRIKE seg %d d=%.1f%s%s"), SegIdx, D,
		                        (StrikesNow() >= 3) ? TEXT(" savor") : TEXT(""),
		                        bThru ? TEXT(" THRU-WALL") : TEXT("")));
		if (State) { State->Strike(Prey); }
		StrikeCooldown = 3.0f;
		SetActorLocation(SegmentAnchors[SegIdx]);
		bWarned = false;
	}
	else if (D < WarnR && !bWarned)
	{
		bWarned = true;
		LogLine(FString::Printf(TEXT("WARN seg %d d=%.1f%s"), SegIdx, D,
		                        (StrikesNow() >= 3) ? TEXT(" savor") : TEXT("")));
	}
}

int32 ARundown::StrikesNow() const
{
	return State ? State->Strikes : 0;
}

void ARundown::LogLine(const FString& Text) const
{
	// the append-only decision log, exactly as the parser reads it
	const FString Path = FPaths::Combine(FPaths::ProjectSavedDir(), TEXT("decision_log.txt"));
	FFileHelper::SaveStringToFile(Text + LINE_TERMINATOR, *Path,
	                              FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM,
	                              &IFileManager::Get(), FILEWRITE_Append);
	UE_LOG(LogRundown, Log, TEXT("%s"), *Text);
}

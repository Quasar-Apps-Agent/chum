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
		if (bTestForceNight) { State->bIsNight = true; }
		if (bTestForceAF) { State->bAfActive = true; }
		if (bTestForceRecording) { State->bRecording = true; }
		if (bTestSaveRoundtrip)
		{
			State->Strikes = 7;
			State->SaveToSlot(TEXT("roundtrip_test"));
			State->Strikes = 0;
			const bool bOk = State->LoadFromSlot(TEXT("roundtrip_test"));
			LogLine(FString::Printf(TEXT("SAVE-ROUNDTRIP v16 ok=%d strikes=%d"),
			                        bOk ? 1 : 0, State->Strikes));
			State->Strikes = 0;
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
	                              FFileHelper::EEncodingOptions::AutoDetect,
	                              &IFileManager::Get(), FILEWRITE_Append);
	UE_LOG(LogRundown, Log, TEXT("%s"), *Text);
}

#include "Rundown.h"
#include "RestorationClock.h"
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
		StrikeR = (Strikes >= 3) ? 2.6f : StrikeRadius;
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
	if (!bIsNight)
	{
		return; // day behavior arrives with GameState (TODO(0.8))
	}
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
		                        (Strikes >= 3) ? TEXT(" savor") : TEXT(""),
		                        bThru ? TEXT(" THRU-WALL") : TEXT("")));
		// TODO(0.8): GameState.strike(player). For the 0.7 brain demo:
		// count it, reset to the anchor, rearm.
		++Strikes;
		StrikeCooldown = 3.0f;
		SetActorLocation(SegmentAnchors[SegIdx]);
		bWarned = false;
	}
	else if (D < WarnR && !bWarned)
	{
		bWarned = true;
		LogLine(FString::Printf(TEXT("WARN seg %d d=%.1f%s"), SegIdx, D,
		                        (Strikes >= 3) ? TEXT(" savor") : TEXT("")));
	}
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

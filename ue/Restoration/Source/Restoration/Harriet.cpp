#include "Harriet.h"
#include "RestorationClock.h"
#include "Engine/World.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"

AHarriet::AHarriet()
{
	PrimaryActorTick.bCanEverTick = true;
	RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
}

void AHarriet::BeginPlay()
{
	Super::BeginPlay();
	Clock = GetWorld()->GetSubsystem<URestorationClock>();
}

bool AHarriet::IsOnAirEffective() const
{
	if (bTestForceBreak) { return false; }
	return Clock ? Clock->IsOnAir() : true;
}

FString AHarriet::GetPrompt() const
{
	return IsOnAirEffective() ? TEXT("HARRIET · in her chair (E)")
	                          : TEXT("HARRIET · mid-motion");
}

void AHarriet::Interact(AActor* /*Player*/)
{
	// the slip-arming and H1/H2 flows land with the presentation half; the
	// freeze contract is what this unit proves
	LogLine(FString::Printf(TEXT("HARRIET interact (%s)"),
	                        IsOnAirEffective() ? TEXT("in chair") : TEXT("mid-motion")));
}

void AHarriet::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);

	if (bTestFreeze)
	{
		// t<1: ON AIR, sway. at 0.5 & 1.0 sample. at 1.0 force break.
		// 1<t<2: frozen, must hold. at 2.0 sample and report.
		TestClock += DeltaSeconds;
		if (TestPhase == 0 && TestClock >= 0.5f)
		{
			TestPhase = 1;
			SwayA = GetActorRotation().Roll;
		}
		else if (TestPhase == 1 && TestClock >= 1.0f)
		{
			TestPhase = 2;
			SwayB = GetActorRotation().Roll;
			bTestForceBreak = true; // the break comes
		}
		else if (TestPhase == 2 && TestClock >= 2.0f)
		{
			TestPhase = 3;
			const float FrozenC = GetActorRotation().Roll;
			const bool bSwaying = !FMath::IsNearlyEqual(SwayA, SwayB, 0.01f);
			const bool bHeld = FMath::IsNearlyEqual(SwayB, FrozenC, 0.001f);
			LogLine(FString::Printf(
				TEXT("HARRIET-FREEZE swayA=%.4f swayB=%.4f frozenC=%.4f swaying=%d held=%d"),
				SwayA, SwayB, FrozenC, bSwaying ? 1 : 0, bHeld ? 1 : 0));
		}
	}

	if (!IsOnAirEffective())
	{
		return; // THE FREEZE: mid-motion, until the return cue
	}
	T += DeltaSeconds;
	FRotator R = GetActorRotation();
	R.Roll = FMath::Sin(T * 0.9f) * FMath::RadiansToDegrees(0.04f);
	SetActorRotation(R);
}

void AHarriet::LogLine(const FString& Text) const
{
	const FString Path = FPaths::Combine(FPaths::ProjectSavedDir(), TEXT("decision_log.txt"));
	FFileHelper::SaveStringToFile(Text + LINE_TERMINATOR, *Path,
	                              FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM,
	                              &IFileManager::Get(), FILEWRITE_Append);
	UE_LOG(LogTemp, Log, TEXT("%s"), *Text);
}

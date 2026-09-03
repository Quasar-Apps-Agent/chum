// The schedule is real (LAW 6). Port of broadcast.gd's ON AIR / BREAK clock.
// Timings are canon: Data/Timings.csv — ON_AIR_SECONDS=50, BREAK_SECONDS=18.
// Timer-driven (tickable world subsystems do not tick in simulate worlds —
// learned 2026-09-03).
#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "TimerManager.h"
#include "Engine/World.h"
#include "RestorationClock.generated.h"

DECLARE_MULTICAST_DELEGATE_OneParam(FOnPhaseChanged, bool /*bNowOnAir*/);

UCLASS()
class RESTORATION_API URestorationClock : public UWorldSubsystem
{
	GENERATED_BODY()

public:
	static constexpr float OnAirSeconds = 50.0f;
	static constexpr float BreakSeconds = 18.0f;

	bool IsOnAir() const { return bOnAir; }
	FOnPhaseChanged OnPhaseChanged;

	virtual void OnWorldBeginPlay(UWorld& InWorld) override
	{
		Super::OnWorldBeginPlay(InWorld);
		ArmTimer();
	}

private:
	void ArmTimer()
	{
		const float Limit = bOnAir ? OnAirSeconds : BreakSeconds;
		GetWorld()->GetTimerManager().SetTimer(
			PhaseTimer,
			FTimerDelegate::CreateUObject(this, &URestorationClock::Flip),
			Limit, false);
	}
	void Flip()
	{
		bOnAir = !bOnAir;
		OnPhaseChanged.Broadcast(bOnAir);
		ArmTimer();
	}

	bool bOnAir = true;
	FTimerHandle PhaseTimer;
};

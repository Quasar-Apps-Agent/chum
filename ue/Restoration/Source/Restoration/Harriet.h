// HARRIET — she sways gently while the building is ON AIR, and freezes
// mid-motion for every break (LAW 6: the schedule is real; Harriet freezes
// inside the color change). Port of harriet.gd's freeze spine. The H1/H2
// casualty sequences are UI-heavy and land with the presentation half.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "RestorationInteractable.h"
#include "Harriet.generated.h"

UCLASS()
class RESTORATION_API AHarriet : public AActor, public IRestorationInteractable
{
	GENERATED_BODY()

public:
	AHarriet();

	// harness: self-drive a sway→freeze→hold sequence and log the proof
	UPROPERTY(EditAnywhere, Category = "Harriet|Test")
	bool bTestFreeze = false;

	virtual FString GetPrompt() const override;
	virtual void Interact(AActor* Player) override;
	virtual void Tick(float DeltaSeconds) override;

protected:
	virtual void BeginPlay() override;

private:
	bool IsOnAirEffective() const;
	void LogLine(const FString& Text) const;

	class URestorationClock* Clock = nullptr;
	float T = 0.0f;             // sway phase; frozen means this stops advancing
	bool bTestForceBreak = false;
	float TestClock = 0.0f;
	float SwayA = 0.0f, SwayB = 0.0f;
	int32 TestPhase = 0;
};

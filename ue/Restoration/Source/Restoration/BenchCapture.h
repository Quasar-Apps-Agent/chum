// THE BENCH — the game's core verb, port of capture_bench.gd. Capture runs
// in forced real time; leave the 4m tether mid-capture and the take aborts.
// No skip exists, by design.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "RestorationInteractable.h"
#include "BenchCapture.generated.h"

UCLASS()
class RESTORATION_API ABenchCapture : public AActor, public IRestorationInteractable
{
	GENERATED_BODY()

public:
	ABenchCapture();

	static constexpr float CaptureSeconds = 12.0f;
	static constexpr float Tether = 4.0f; // meters

	// harness scaffolding
	UPROPERTY(EditAnywhere, Category = "Bench|Test")
	bool bTestAutoStart = false;

	virtual FString GetPrompt() const override;
	virtual void Interact(AActor* Player) override;
	virtual void Tick(float DeltaSeconds) override;

protected:
	virtual void BeginPlay() override;

private:
	void LogLine(const FString& Text) const;

	bool bRunning = false;
	float T = 0.0f;
	UPROPERTY() AActor* Player = nullptr;
	float TestArm = 0.0f;
};

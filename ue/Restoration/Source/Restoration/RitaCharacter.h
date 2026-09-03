// RITA — first-person controller, port of scripts/player.gd. Deliberate
// weight: SPEED 3.1, ACCEL 10, REACH 2.6, crouch per gap-audit ruling c045
// (toggle, 0.55x speed, eye drops 0.6m; a body verb, useless against him
// by architecture). Constants are canon (Data/Timings.csv).
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "RitaCharacter.generated.h"

UCLASS()
class RESTORATION_API ARitaCharacter : public ACharacter
{
	GENERATED_BODY()

public:
	ARitaCharacter();

	static constexpr float WalkSpeed = 3.1f;   // m/s
	static constexpr float Accel = 10.0f;      // m/s^2
	static constexpr float Reach = 2.6f;       // interact ray
	static constexpr float CrouchMult = 0.55f; // c045
	static constexpr float CrouchDrop = 0.6f;  // camera drop, meters

	UPROPERTY(VisibleAnywhere)
	class UCameraComponent* Camera;

	// harness scaffolding: self-driving walk test (no human input needed)
	UPROPERTY(EditAnywhere, Category = "Rita|Test")
	bool bTestAutoWalk = false;

	virtual void SetupPlayerInputComponent(class UInputComponent* Input) override;
	virtual void Tick(float DeltaSeconds) override;

protected:
	virtual void BeginPlay() override;

private:
	void MoveForward(float V);
	void MoveRight(float V);
	void ToggleCrouch();
	void Interact();
	void LogLine(const FString& Text) const;

	bool bCrouched = false;
	float CamBaseZ = 0.0f;
	float TestT = 0.0f;
	int32 TestPhase = 0;
};

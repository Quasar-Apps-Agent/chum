// THE RUNDOWN — the show, performing itself through the building.
// Tick brain, NO Behavior Tree (UE5-MIGRATION-MAP: "the grammar is the
// point"). Verbatim port of scripts/rundown.gd; constants are canon
// (Data/Timings.csv). Telemetry lines append to Saved/decision_log.txt in
// the IDENTICAL format the invariant parser reads ("WARN seg ...",
// "STRIKE seg ...", "RELOCATE ..."). GameState hooks land in unit 0.8 —
// marked TODO(0.8) where they attach.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Rundown.generated.h"

UCLASS()
class RESTORATION_API ARundown : public AActor
{
	GENERATED_BODY()

public:
	ARundown();

	// canon constants (meters in the spec; converted to uu at use)
	static constexpr float MoveSpeed = 2.4f;
	static constexpr float AfApproachSpeed = 0.8f;
	static constexpr float AfLoomDist = 1.2f;
	static constexpr float AfCoolSeconds = 2.0f;
	static constexpr float AfFoldSeconds = 2.2f;
	static constexpr float AfDoorNear = 1.0f;
	static constexpr float AfCrossingSpeed = 1.6f;
	static constexpr float WarnRadius = 7.0f;
	static constexpr float StrikeRadius = 2.2f;

	// The three segments' home anchors (room centers per Data/Rooms.csv):
	// STORY CORNER -> TAPE LIBRARY, THE SONG -> STUDIO A, CRAFT TIME -> PATCH BAY
	UPROPERTY(EditAnywhere, Category = "Rundown")
	TArray<FVector> SegmentAnchors;

	UPROPERTY(EditAnywhere, Category = "Rundown")
	TArray<FString> SegmentNames;

	// filled from Data/Doors.csv at BeginPlay (fold toll positions)
	TArray<FVector> DoorPositions;

	// TODO(0.8): these become GameState reads; for the 0.7 brain demo they
	// are actor flags so the grammar can run and log
	UPROPERTY(EditAnywhere, Category = "Rundown|StateStub")
	bool bIsNight = true;

	UPROPERTY(EditAnywhere, Category = "Rundown|StateStub")
	int32 Strikes = 0;

	// the hunt target: player pawn if one exists, else any actor tagged
	// RundownTestTarget (lets the brain run under simulate/harness)
	AActor* ResolveTarget() const;

	void ReportNoise(const FVector& WorldPos); // the noise bus entry point

	virtual void Tick(float DeltaSeconds) override;

protected:
	virtual void BeginPlay() override;

private:
	void OnPhaseChanged(bool bNowOnAir);
	bool DoorFoldCheck(float Now);
	void LogLine(const FString& Text) const;

	int32 SegIdx = 0;
	FVector Target = FVector::ZeroVector;
	bool bWarned = false;
	float WarnR = WarnRadius;
	float StrikeR = StrikeRadius;
	float FoldT = 0.0f;
	TMap<int32, float> FoldCool;
	FVector HeardPos = FVector::ZeroVector;
	float HeardT = -100.0f;
	float StrikeCooldown = 0.0f;
	bool bSpawnLogged = false;
};

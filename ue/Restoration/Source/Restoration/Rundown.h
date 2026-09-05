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

	// Test scaffolding (harness sets these pre-simulate; BeginPlay pushes
	// them into URestorationState — clearly not gameplay config)
	UPROPERTY(EditAnywhere, Category = "Rundown|Test")
	bool bTestForceNight = false;

	UPROPERTY(EditAnywhere, Category = "Rundown|Test")
	bool bTestForceAF = false;

	UPROPERTY(EditAnywhere, Category = "Rundown|Test")
	bool bTestForceRecording = false;

	UPROPERTY(EditAnywhere, Category = "Rundown|Test")
	float TestRecordingOffAfter = 0.0f;

	UPROPERTY(EditAnywhere, Category = "Rundown|Test")
	bool bTestSaveRoundtrip = false;

	UPROPERTY(EditAnywhere, Category = "Rundown|Test")
	bool bTestLoopFns = false;

	// invariant harness: force night, hold the tagged target at warn range
	// (WARN), then pull it to strike range (STRIKE) — the I01/I02 scenario
	UPROPERTY(EditAnywhere, Category = "Rundown|Test")
	bool bTestInvariants = false;

	// the hunt target: player pawn if one exists, else any actor tagged
	// RundownTestTarget (lets the brain run under simulate/harness)
	AActor* ResolveTarget() const;

	// the noise bus entry point — _on_noise's four gates (rundown.gd:128-134):
	// deaf in the dead room; only at night; not during the premiere; heard
	// only within loudness*3.0 m
	void ReportNoise(const FVector& WorldPos, float Loudness = 4.0f);
	int32 StrikesNow() const;

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
	// HARNESS STAND-INS, NOT IN rundown.gd:305-322 (PORT-AUDIT-1 R6/S8): the 3s
	// cooldown and the post-strike teleport stand in for the retake
	// presentation's player respawn. Remove both when 0.8b-5 lands it.
	float StrikeCooldown = 0.0f;
	bool bSpawnLogged = false;
	// AF layer
	class URestorationState* State = nullptr;
	float AfCool = -100.0f;
	bool bAfSeenOnce = false;
	bool bDeadroomLine = false;
	float TestClock = 0.0f;
	bool bHeardFired = false; // invariant scenario: the I22 noise+break, once
};

// RESTORATION state — port of game_state.gd (the code is the spec).
// UGameInstanceSubsystem per the migration map; save is v16, field names
// mirror _save_dict 1:1 (the save's SEMANTIC fields must not change).
// This is 0.8a: the brain-relevant core + save skeleton; the paper economy,
// stations and screening attach in the following sub-boxes.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "RestorationState.generated.h"

USTRUCT()
struct FRestorationDaily
{
	GENERATED_BODY()
	UPROPERTY() int32 Id = 0;
	UPROPERTY() int32 Take = 0;
};

UCLASS()
class RESTORATION_API URestorationSaveGame : public USaveGame
{
	GENERATED_BODY()
public:
	UPROPERTY() int32 Version = 16;
	UPROPERTY() int32 Mode = 0;
	UPROPERTY() bool Tbc = false;
	UPROPERTY() int32 CurrentTape = 0;
	UPROPERTY() int32 Paper = 0;
	UPROPERTY() int32 Signatures = 0;
	UPROPERTY() int32 Captures = 0;
	UPROPERTY() int32 Strikes = 0;
	UPROPERTY() int32 ItemsLost = 0;
	UPROPERTY() int32 Day = 1;
	UPROPERTY() TArray<FString> Keys;
	UPROPERTY() TArray<FRestorationDaily> Dailies;
	UPROPERTY() int32 DailySeq = 0;
	UPROPERTY() bool FilmWatched = false;
	UPROPERTY() bool ScreeningDone = false;
	UPROPERTY() bool RunComplete = false;
	UPROPERTY() bool HasFireTape = false;
	UPROPERTY() bool FireTapeWatched = false;
	UPROPERTY() int32 SeanceWear = 0;
	UPROPERTY() int32 LelandAnswers = 0;
	UPROPERTY() bool LockdownDone = false;
	UPROPERTY() bool FinaleDone = false;
	UPROPERTY() FString EndingReached;
};

DECLARE_MULTICAST_DELEGATE_OneParam(FOnRunEnded, int32 /*Take*/);
DECLARE_MULTICAST_DELEGATE_OneParam(FOnSheetChanged, int32 /*Strikes*/);

UCLASS()
class RESTORATION_API URestorationState : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	static constexpr int32 SaveVersion = 16;

	// live state the brain reads (names mirror game_state.gd)
	bool bIsNight = false;
	bool bAfActive = false;
	bool bRecording = false;
	float RecordingLeft = 0.0f;
	bool bAfTaught = false;
	bool bPremiereLive = false;
	bool bCrossing = false;
	bool bCrossingCaught = false;
	bool bCascadeActive = false;
	bool bInRetake = false;
	int32 Strikes = 0;
	int32 ItemsLost = 0;
	int32 CurrentTape = 1;
	int32 Captures = 0;
	int32 DailySeq = 0;
	TArray<FRestorationDaily> Dailies;

	FOnRunEnded OnRunEnded;
	FOnSheetChanged OnSheetChanged;
	FOnSheetChanged OnNightChanged; // bool-as-int; dedicated type with 0.8b-3

	void SetNight(bool bOn)
	{
		if (bIsNight != bOn)
		{
			bIsNight = bOn;
			OnNightChanged.Broadcast(bOn ? 1 : 0);
		}
	}

	// the dead room rect, canon: |x-19| <= 2.2 && |z-2.5| <= 2.7 (Godot
	// meters; UE y carries Godot z per the stamping)
	bool InDeadRoom(const FVector& Pos) const
	{
		return FMath::Abs(Pos.X - 1900.0f) <= 220.0f &&
		       FMath::Abs(Pos.Y - 250.0f) <= 270.0f;
	}

	// strike(player) — the retake economy core (presentation lands with P3)
	void Strike(AActor* Player);

	bool SaveToSlot(const FString& Slot = TEXT("restoration")) const;
	bool LoadFromSlot(const FString& Slot = TEXT("restoration"));
};

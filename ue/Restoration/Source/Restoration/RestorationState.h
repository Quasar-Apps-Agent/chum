// RESTORATION state — port of game_state.gd (the code is the spec).
// UGameInstanceSubsystem per the migration map; save is v16, field names and
// TYPES mirror _save_dict 1:1 (the save's SEMANTIC fields must not change —
// see ue/PORT-NOTES-STATE.md §1). 0.8b-3 brings the SaveGame to full v16
// shape + round-trip; the gameplay functions (§6 tail) land in 0.8b-4.
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
	UPROPERTY() int32 Take = 0; // -1 = shortcut daily
};

USTRUCT()
struct FRestorationSignature
{
	GENERATED_BODY()
	UPROPERTY() FString Station;
	UPROPERTY() int32 Tape = 0;
	UPROPERTY() FString Signed;       // "TODAY" / "TOMORROW"
	UPROPERTY() bool bPresigned = false;
};

USTRUCT()
struct FRestorationCapture
{
	GENERATED_BODY()
	UPROPERTY() FString Name;
	UPROPERTY() int32 Tape = 0;
	UPROPERTY() FString At;
};

USTRUCT()
struct FRestorationCasualty
{
	GENERATED_BODY()
	UPROPERTY() FString Who;
	UPROPERTY() FString Cause;
	UPROPERTY() FString Line;
	UPROPERTY() int32 Day = 0;
};

UCLASS()
class RESTORATION_API URestorationSaveGame : public USaveGame
{
	GENERATED_BODY()
public:
	// v16 _save_dict, in dict order (55 keys). Defaults per PORT-NOTES §1.
	UPROPERTY() int32 Version = 16;                       // 1
	UPROPERTY() int32 Mode = 1;                           // 2 LATE_NIGHT
	UPROPERTY() bool Tbc = false;                         // 3
	UPROPERTY() int32 CurrentTape = 1;                    // 4
	UPROPERTY() TMap<FString, int32> Paper;               // 5 S1..S5=3
	UPROPERTY() TArray<FRestorationSignature> Signatures; // 6
	UPROPERTY() TArray<FRestorationCapture> Captures;     // 7
	UPROPERTY() int32 Strikes = 0;                        // 8
	UPROPERTY() int32 ItemsLost = 0;                      // 9
	UPROPERTY() int32 Day = 1;                            // 10
	UPROPERTY() TArray<FString> Keys;                     // 11
	UPROPERTY() int32 Pt = 0;                             // 12
	UPROPERTY() TArray<FRestorationDaily> Dailies;        // 13
	UPROPERTY() int32 DailySeq = 0;                       // 14
	UPROPERTY() int32 CarriedId = -1;                     // 15
	UPROPERTY() int32 CarriedTake = 0;                    // 16
	UPROPERTY() bool FilmWatched = false;                 // 17
	UPROPERTY() TArray<FString> SignalsKnown;             // 18
	UPROPERTY() bool ScreeningDone = false;               // 19
	UPROPERTY() bool RunComplete = false;                 // 20
	UPROPERTY() bool HasFireTape = false;                 // 21
	UPROPERTY() bool FireTapeWatched = false;             // 22
	UPROPERTY() float SeanceWear = 0.0f;                  // 23
	UPROPERTY() TArray<int32> LelandAnswers;              // 24
	UPROPERTY() bool PresignedSeen = false;               // 25
	UPROPERTY() bool DockDone = false;                    // 26
	UPROPERTY() TArray<FString> Assets;                   // 27
	UPROPERTY() FString Decision;                         // 28
	UPROPERTY() bool LockdownDone = false;                // 29
	UPROPERTY() bool FinaleDone = false;                  // 30
	UPROPERTY() FString EndingReached;                    // 31
	UPROPERTY() bool LiePending = false;                  // 32
	UPROPERTY() bool VessInsight = false;                 // 33
	UPROPERTY() bool VessCredited = false;                // 34
	UPROPERTY() FString NgRelic;                          // 35
	UPROPERTY() bool CrateOpened = false;                 // 36
	UPROPERTY() bool NightTripped = false;                // 37
	UPROPERTY() float CovMonitor = 0.0f;                  // 38
	UPROPERTY() float CovMove = 0.0f;                     // 39
	UPROPERTY() float CovStill = 0.0f;                    // 40
	UPROPERTY() bool PhotoSafe = false;                   // 41
	UPROPERTY() bool CascadeDone = false;                 // 42
	UPROPERTY() TArray<FString> ReadProps;                // 43
	UPROPERTY() bool AfActive = false;                    // 44
	UPROPERTY() bool AfTaught = false;                    // 45
	UPROPERTY() TArray<FRestorationCasualty> Casualties;  // 46
	UPROPERTY() bool MerleOffered = false;                // 47
	UPROPERTY() bool SignoffCompleted = false;            // 48
	UPROPERTY() int32 RowCasualties = 0;                  // 49
	UPROPERTY() bool H2Pending = false;                   // 50
	UPROPERTY() bool DeadroomSeen = false;                // 51
	UPROPERTY() bool RejectedSeen = false;                // 52
	UPROPERTY() bool GlimpseSeen = false;                 // 53
	UPROPERTY() bool Merle1974 = false;                   // 54
	UPROPERTY() bool FireUnsealed = false;                // 55
};

DECLARE_MULTICAST_DELEGATE_OneParam(FOnRunEnded, int32 /*Take*/);
DECLARE_MULTICAST_DELEGATE_OneParam(FOnSheetChanged, int32 /*Strikes*/);
DECLARE_MULTICAST_DELEGATE_TwoParams(FOnNoise, const FVector& /*Pos*/, float /*Radius*/);

UCLASS()
class RESTORATION_API URestorationState : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	static constexpr int32 SaveVersion = 16;

	virtual void Initialize(FSubsystemCollectionBase& Collection) override;

	// ---- LIVE, NOT SAVED (§2): reset on boot; never survive a reload ----
	bool bIsNight = false;
	bool bRecording = false;
	float RecordingLeft = 0.0f;
	bool bInRetake = false;
	bool bPremiereLive = false;
	bool bCrossing = false;
	bool bCrossingCaught = false;
	bool bCascadeActive = false;
	bool bHarrietSlip = false;             // one-shot: sign without paper
	TMap<FString, FVector> StationPoints;  // respawn anchors, world-stamped (uu)

	// ---- SAVED (mirror _save_dict; the persistent working set) ----------
	int32 Mode = 1;               // LATE_NIGHT
	bool bTbc = false;
	int32 CurrentTape = 1;
	TMap<FString, int32> Paper;
	TArray<FRestorationSignature> Signatures;
	TArray<FRestorationCapture> Captures;
	int32 Strikes = 0;
	int32 ItemsLost = 0;
	int32 Day = 1;
	TArray<FString> Keys;
	int32 Pt = 0;
	TArray<FRestorationDaily> Dailies;
	int32 DailySeq = 0;
	int32 CarriedId = -1;
	int32 CarriedTake = 0;
	bool bFilmWatched = false;
	TArray<FString> SignalsKnown;
	bool bScreeningDone = false;
	bool bRunComplete = false;
	bool bHasFireTape = false;
	bool bFireTapeWatched = false;
	float SeanceWear = 0.0f;
	TArray<int32> LelandAnswers;
	bool bPresignedSeen = false;
	bool bDockDone = false;
	TArray<FString> Assets;
	FString Decision;
	bool bLockdownDone = false;
	bool bFinaleDone = false;
	FString EndingReached;
	bool bLiePending = false;
	bool bVessInsight = false;
	bool bVessCredited = false;
	FString NgRelic;
	bool bCrateOpened = false;
	bool bNightTripped = false;
	float CovMonitor = 0.0f;
	float CovMove = 0.0f;
	float CovStill = 0.0f;
	bool bPhotoSafe = false;
	bool bCascadeDone = false;
	TArray<FString> ReadProps;
	bool bAfActive = false;
	bool bAfTaught = false;
	TArray<FRestorationCasualty> Casualties;
	bool bMerleOffered = false;
	bool bSignoffCompleted = false;
	int32 RowCasualties = 0;
	bool bH2Pending = false;
	bool bDeadroomSeen = false;
	bool bRejectedSeen = false;
	bool bGlimpseSeen = false;
	bool bMerle1974 = false;
	bool bFireUnsealed = false;

	FOnRunEnded OnRunEnded;
	FOnSheetChanged OnSheetChanged;
	FOnSheetChanged OnNightChanged;
	FOnNoise OnNoise; // noise_event → ARundown::ReportNoise (relocation)

	// set_night: the day/night driver. Morning advances the day, caps the
	// tape at 5, completes the prototype at day >= 3.
	void SetNight(bool bOn);

	// paper economy + the sign flow (paper_for / sign_log / _sign_finish)
	int32 PaperFor(const FString& Station) const;
	bool SignLog(const FString& Station);
	bool SignFinish(const FString& Station);

	// stations + respawn
	void RegisterStation(const FString& Id, const FVector& WorldPos);
	FVector RespawnPoint() const;

	// readables, keys, captures
	void MarkRead(const FString& Id);
	bool HasKey(const FString& Id) const;
	void TakeKey(const FString& Id, const FString& Display);
	void LogCapture(const FString& CaptureName);

	// canon: |x-19| <= 2.2 && |z-2.5| <= 2.7 (Godot m; UE y carries Godot z)
	bool InDeadRoom(const FVector& Pos) const
	{
		return FMath::Abs(Pos.X - 1900.0f) <= 220.0f &&
		       FMath::Abs(Pos.Y - 250.0f) <= 270.0f;
	}

	void Strike(AActor* Player);

	bool SaveToSlot(const FString& Slot = TEXT("restoration")) const;
	bool LoadFromSlot(const FString& Slot = TEXT("restoration"));

private:
	void SeedPaper();
	void LogLine(const FString& Text) const; // telemetry, parser-format
public:
	void LogLineTest(const FString& T) const { LogLine(T); }
};

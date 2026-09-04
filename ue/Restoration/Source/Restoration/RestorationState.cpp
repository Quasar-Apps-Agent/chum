#include "RestorationState.h"
#include "Kismet/GameplayStatics.h"

DEFINE_LOG_CATEGORY_STATIC(LogRestoState, Log, All);

void URestorationState::Initialize(FSubsystemCollectionBase& Collection)
{
	Super::Initialize(Collection);
	SeedPaper();
}

void URestorationState::SeedPaper()
{
	// paper = {S1:3, S2:3, S3:3, S4:3, S5:3} (DEMO strips to S1,S5 — §5)
	Paper.Reset();
	for (const TCHAR* S : { TEXT("S1"), TEXT("S2"), TEXT("S3"), TEXT("S4"), TEXT("S5") })
	{
		Paper.Add(S, 3);
	}
}

void URestorationState::Strike(AActor* Player)
{
	if (bInRetake)
	{
		return;
	}
	bInRetake = true;
	Strikes += 1;
	const int32 Take = Strikes;
	// ITEM_ORDER has 7 entries; the LOUPE (index 6) is the New Game+ relic,
	// so the clamp is 7, not 6 (§6 finding).
	if (ItemsLost < 7)
	{
		ItemsLost += 1;
	}
	const bool bFull = Strikes >= 4 || Mode == 2 /*ONE_TAKE*/;
	if (bFull)
	{
		Strikes = 0;
		SaveToSlot();
		OnSheetChanged.Broadcast(Strikes);
		OnRunEnded.Broadcast(Take);
		bInRetake = false;
		return;
	}
	DailySeq += 1;
	FRestorationDaily D;
	D.Id = DailySeq;
	D.Take = Take;
	Dailies.Add(D);
	OnSheetChanged.Broadcast(Strikes);
	UE_LOG(LogRestoState, Log, TEXT("STRIKE recorded: take %d, dailies %d, items_lost %d"),
	       Take, Dailies.Num(), ItemsLost);
	bInRetake = false;
}

bool URestorationState::SaveToSlot(const FString& Slot) const
{
	URestorationSaveGame* S = Cast<URestorationSaveGame>(
		UGameplayStatics::CreateSaveGameObject(URestorationSaveGame::StaticClass()));
	S->Version = SaveVersion;
	S->Mode = Mode;             S->Tbc = bTbc;                 S->CurrentTape = CurrentTape;
	S->Paper = Paper;           S->Signatures = Signatures;    S->Captures = Captures;
	S->Strikes = Strikes;       S->ItemsLost = ItemsLost;      S->Day = Day;
	S->Keys = Keys;             S->Pt = Pt;                    S->Dailies = Dailies;
	S->DailySeq = DailySeq;     S->CarriedId = CarriedId;      S->CarriedTake = CarriedTake;
	S->FilmWatched = bFilmWatched;    S->SignalsKnown = SignalsKnown;
	S->ScreeningDone = bScreeningDone; S->RunComplete = bRunComplete;
	S->HasFireTape = bHasFireTape;    S->FireTapeWatched = bFireTapeWatched;
	S->SeanceWear = SeanceWear;       S->LelandAnswers = LelandAnswers;
	S->PresignedSeen = bPresignedSeen; S->DockDone = bDockDone;
	S->Assets = Assets;         S->Decision = Decision;        S->LockdownDone = bLockdownDone;
	S->FinaleDone = bFinaleDone;      S->EndingReached = EndingReached;
	S->LiePending = bLiePending;      S->VessInsight = bVessInsight;
	S->VessCredited = bVessCredited;  S->NgRelic = NgRelic;
	S->CrateOpened = bCrateOpened;    S->NightTripped = bNightTripped;
	S->CovMonitor = CovMonitor;       S->CovMove = CovMove;    S->CovStill = CovStill;
	S->PhotoSafe = bPhotoSafe;        S->CascadeDone = bCascadeDone;
	S->ReadProps = ReadProps;         S->AfActive = bAfActive; S->AfTaught = bAfTaught;
	S->Casualties = Casualties;       S->MerleOffered = bMerleOffered;
	S->SignoffCompleted = bSignoffCompleted; S->RowCasualties = RowCasualties;
	S->H2Pending = bH2Pending;        S->DeadroomSeen = bDeadroomSeen;
	S->RejectedSeen = bRejectedSeen;  S->GlimpseSeen = bGlimpseSeen;
	S->Merle1974 = bMerle1974;        S->FireUnsealed = bFireUnsealed;
	const bool bOk = UGameplayStatics::SaveGameToSlot(S, Slot, 0);
	UE_LOG(LogRestoState, Log, TEXT("SAVE v%d slot=%s ok=%d"), S->Version, *Slot, bOk ? 1 : 0);
	return bOk;
}

bool URestorationState::LoadFromSlot(const FString& Slot)
{
	if (!UGameplayStatics::DoesSaveGameExist(Slot, 0))
	{
		return false;
	}
	URestorationSaveGame* S = Cast<URestorationSaveGame>(
		UGameplayStatics::LoadGameFromSlot(Slot, 0));
	if (!S)
	{
		return false;
	}
	if (S->Version < SaveVersion)
	{
		UE_LOG(LogRestoState, Log, TEXT("LOG MIGRATED format v%d to v%d"), S->Version, SaveVersion);
	}
	else if (S->Version > SaveVersion)
	{
		UE_LOG(LogRestoState, Warning, TEXT("LOG FROM A NEWER BUILD v%d read by v%d"), S->Version, SaveVersion);
	}
	Mode = S->Mode;             bTbc = S->Tbc;                 CurrentTape = S->CurrentTape;
	// paper MERGES into the seeded map (keys absent from the file survive)
	for (const TPair<FString, int32>& P : S->Paper) { Paper.Add(P.Key, P.Value); }
	Signatures = S->Signatures; Captures = S->Captures;
	Strikes = S->Strikes;       ItemsLost = S->ItemsLost;      Day = S->Day;
	Keys = S->Keys;             Pt = S->Pt;                    Dailies = S->Dailies;
	DailySeq = S->DailySeq;     CarriedId = S->CarriedId;      CarriedTake = S->CarriedTake;
	bFilmWatched = S->FilmWatched;    SignalsKnown = S->SignalsKnown;
	bScreeningDone = S->ScreeningDone; bRunComplete = S->RunComplete;
	bHasFireTape = S->HasFireTape;    bFireTapeWatched = S->FireTapeWatched;
	SeanceWear = S->SeanceWear;       LelandAnswers = S->LelandAnswers;
	bPresignedSeen = S->PresignedSeen; bDockDone = S->DockDone;
	Assets = S->Assets;         Decision = S->Decision;        bLockdownDone = S->LockdownDone;
	bFinaleDone = S->FinaleDone;      EndingReached = S->EndingReached;
	bLiePending = S->LiePending;      bVessInsight = S->VessInsight;
	bVessCredited = S->VessCredited;  NgRelic = S->NgRelic;
	bCrateOpened = S->CrateOpened;    bNightTripped = S->NightTripped;
	CovMonitor = S->CovMonitor;       CovMove = S->CovMove;    CovStill = S->CovStill;
	bPhotoSafe = S->PhotoSafe;        bCascadeDone = S->CascadeDone;
	ReadProps = S->ReadProps;         bAfActive = S->AfActive; bAfTaught = S->AfTaught;
	Casualties = S->Casualties;       bMerleOffered = S->MerleOffered;
	bSignoffCompleted = S->SignoffCompleted; RowCasualties = S->RowCasualties;
	bH2Pending = S->H2Pending;        bDeadroomSeen = S->DeadroomSeen;
	bRejectedSeen = S->RejectedSeen;  bGlimpseSeen = S->GlimpseSeen;
	bMerle1974 = S->Merle1974;        bFireUnsealed = S->FireUnsealed;
	return true;
}

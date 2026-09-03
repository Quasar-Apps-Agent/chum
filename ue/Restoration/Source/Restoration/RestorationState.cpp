#include "RestorationState.h"
#include "Kismet/GameplayStatics.h"

DEFINE_LOG_CATEGORY_STATIC(LogRestoState, Log, All);

void URestorationState::Strike(AActor* Player)
{
	// verbatim: in_retake guard, take accounting, full-sheet at 4 (ONE_TAKE
	// mode arrives with the mode port)
	if (bInRetake)
	{
		return;
	}
	bInRetake = true;
	Strikes += 1;
	const int32 Take = Strikes;
	ItemsLost = FMath::Min(ItemsLost + 1, 6); // ITEM_ORDER economy: count now, names with P3
	const bool bFull = Strikes >= 4;
	if (bFull)
	{
		Strikes = 0;
		SaveToSlot();
		OnSheetChanged.Broadcast(Strikes);
		OnRunEnded.Broadcast(Take);
		bInRetake = false; // retake presentation owns this in P3; keep the brain live
		return;
	}
	DailySeq += 1;
	FRestorationDaily D;
	D.Id = DailySeq;
	D.Take = Take;
	Dailies.Add(D);
	OnSheetChanged.Broadcast(Strikes);
	UE_LOG(LogRestoState, Log, TEXT("STRIKE recorded: take %d, dailies %d"), Take, Dailies.Num());
	bInRetake = false;
}

bool URestorationState::SaveToSlot(const FString& Slot) const
{
	URestorationSaveGame* SG = Cast<URestorationSaveGame>(
		UGameplayStatics::CreateSaveGameObject(URestorationSaveGame::StaticClass()));
	SG->Version = SaveVersion;
	SG->Strikes = Strikes;
	SG->ItemsLost = ItemsLost;
	SG->DailySeq = DailySeq;
	SG->Dailies = Dailies;
	const bool bOk = UGameplayStatics::SaveGameToSlot(SG, Slot, 0);
	UE_LOG(LogRestoState, Log, TEXT("SAVE v%d slot=%s ok=%d"), SG->Version, *Slot, bOk ? 1 : 0);
	return bOk;
}

bool URestorationState::LoadFromSlot(const FString& Slot)
{
	if (!UGameplayStatics::DoesSaveGameExist(Slot, 0))
	{
		return false;
	}
	URestorationSaveGame* SG = Cast<URestorationSaveGame>(
		UGameplayStatics::LoadGameFromSlot(Slot, 0));
	if (!SG)
	{
		return false;
	}
	if (SG->Version < SaveVersion)
	{
		// migration chain: nothing was lost (older fields default forward)
		UE_LOG(LogRestoState, Log, TEXT("LOG MIGRATED format v%d to v%d"), SG->Version, SaveVersion);
	}
	else if (SG->Version > SaveVersion)
	{
		UE_LOG(LogRestoState, Warning, TEXT("LOG FROM A NEWER BUILD v%d read by v%d"), SG->Version, SaveVersion);
	}
	Strikes = SG->Strikes;
	ItemsLost = SG->ItemsLost;
	DailySeq = SG->DailySeq;
	Dailies = SG->Dailies;
	return true;
}

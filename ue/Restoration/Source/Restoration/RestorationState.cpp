#include "RestorationState.h"
#include "Kismet/GameplayStatics.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"

DEFINE_LOG_CATEGORY_STATIC(LogRestoState, Log, All);

namespace { constexpr float M = 100.0f; } // meters -> uu

void URestorationState::LogLine(const FString& Text) const
{
	const FString Path = FPaths::Combine(FPaths::ProjectSavedDir(), TEXT("decision_log.txt"));
	FFileHelper::SaveStringToFile(Text + LINE_TERMINATOR, *Path,
	                              FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM,
	                              &IFileManager::Get(), FILEWRITE_Append);
	UE_LOG(LogRestoState, Log, TEXT("%s"), *Text);
}

void URestorationState::SetNight(bool bOn)
{
	bIsNight = bOn;
	if (!bOn)
	{
		Day += 1;
		CurrentTape = FMath::Min(Day, 5);
		LogLine(FString::Printf(TEXT("MORNING · Day %d · Tape %d"), Day, CurrentTape));
		if (Day >= 3 && !bRunComplete)
		{
			bRunComplete = true;
			LogLine(TEXT("PROTOTYPE COMPLETE"));
		}
	}
	else
	{
		LogLine(TEXT("NIGHT · the building belongs to the schedule"));
	}
	SaveToSlot();
	OnNightChanged.Broadcast(bOn ? 1 : 0);
}

int32 URestorationState::PaperFor(const FString& Station) const
{
	if (Mode == 0 /*MATINEE*/) { return 99; }
	return Paper.FindRef(Station);
}

bool URestorationState::SignLog(const FString& Station)
{
	if (Mode != 0 /*MATINEE*/)
	{
		if (PaperFor(Station) <= 0)
		{
			if (bHarrietSlip)
			{
				bHarrietSlip = false; // the slip signs once, in a hand not yours
			}
			else
			{
				LogLine(FString::Printf(TEXT("SIGN REFUSED %s (no paper)"), *Station));
				return false;
			}
		}
		else
		{
			Paper.Add(Station, PaperFor(Station) - 1);
		}
	}
	return SignFinish(Station);
}

bool URestorationState::SignFinish(const FString& Station)
{
	FRestorationSignature Sig;
	Sig.Station = Station;
	Sig.Tape = CurrentTape;
	Sig.Signed = FDateTime::Now().ToString();
	Signatures.Add(Sig);
	SaveToSlot();
	LogLine(FString::Printf(TEXT("SIGNED %s (paper left %d)"), *Station, PaperFor(Station)));
	// noise_event(respawn_point(), 4.0) — signing gives away your position;
	// the hunter relocates toward the noise (LAW: the world keeps receipts)
	OnNoise.Broadcast(RespawnPoint(), 4.0f);
	return true;
}

void URestorationState::RegisterStation(const FString& Id, const FVector& WorldPos)
{
	// Godot: pos + Vector3(0, 0.5, 1.2) — up 0.5m, forward 1.2m. Godot y(up)
	// -> UE z(up); Godot z(forward) -> UE y. So the offset is (0, 1.2, 0.5)m.
	StationPoints.Add(Id, WorldPos + FVector(0.0f, 1.2f * M, 0.5f * M));
}

FVector URestorationState::RespawnPoint() const
{
	if (Signatures.Num() > 0)
	{
		const FString Sid = Signatures.Last().Station;
		if (const FVector* P = StationPoints.Find(Sid))
		{
			return *P;
		}
	}
	// fallback (0, 1.0, 2.5) Godot -> (0, 2.5, 1.0) UE, in uu
	return FVector(0.0f, 2.5f * M, 1.0f * M);
}

void URestorationState::MarkRead(const FString& Id)
{
	if (ReadProps.Contains(Id)) { return; }
	ReadProps.Add(Id);
	SaveToSlot();
	LogLine(FString::Printf(TEXT("READ %s (%d of 10 documents)"), *Id, ReadProps.Num()));
}

bool URestorationState::HasKey(const FString& Id) const
{
	return Keys.Contains(Id);
}

void URestorationState::TakeKey(const FString& Id, const FString& Display)
{
	if (Keys.Contains(Id))
	{
		LogLine(FString::Printf(TEXT("KEY already carried: %s"), *Display));
		return;
	}
	Keys.Add(Id);
	SaveToSlot();
	LogLine(FString::Printf(TEXT("TAKEN · %s"), *Display));
}

void URestorationState::LogCapture(const FString& CaptureName)
{
	FRestorationCapture Cap;
	Cap.Name = CaptureName;
	Cap.Tape = CurrentTape;
	Cap.At = FDateTime::Now().ToString();
	Captures.Add(Cap);
	SaveToSlot();
	LogLine(FString::Printf(TEXT("CAPTURED · %s · presentation kept"), *CaptureName));
}

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

FString URestorationState::ItemOrder(int32 Index)
{
	static const TCHAR* Names[7] = { TEXT("WATCH"), TEXT("PEN"), TEXT("PHOTOGRAPH"),
	                                 TEXT("LIGHTER"), TEXT("COMPACT"), TEXT("KEYS"), TEXT("LOUPE") };
	return (Index >= 0 && Index < 7) ? FString(Names[Index]) : FString();
}

// game_state.gd:482-506, order of effects verbatim (PORT-AUDIT-1 S6/S7)
void URestorationState::Strike(AActor* Player)
{
	if (bInRetake)
	{
		return;
	}
	bInRetake = true;
	Strikes += 1;
	const int32 Take = Strikes;
	FString Lost;
	if (ItemsLost < 7)
	{
		Lost = ItemOrder(ItemsLost); // resolved BEFORE the increment (S6)
		ItemsLost += 1;
	}
	const bool bFull = Strikes >= 4 || Mode == 2 /*ONE_TAKE*/;
	if (bFull)
	{
		Strikes = 0;
		SaveToSlot();
		OnSheetChanged.Broadcast(Strikes);
		OnRunEnded.Broadcast(Take);
		bInRetake = false; // HARNESS STAND-IN (S8): Godot holds it until the retake presentation clears it
		return;
	}
	DailySeq += 1;
	FRestorationDaily D;
	D.Id = DailySeq;
	D.Take = Take;
	Dailies.Add(D);
	OnDailyAdded.Broadcast(DailySeq, Take);
	SaveToSlot(); // a strike is a save point (game_state.gd:502) — S7
	OnSheetChanged.Broadcast(Strikes);
	OnCaptured.Broadcast(Take, bFull, Lost, RespawnPoint());
	// PARSER-COLLISION GUARD: never write "STRIKE " or "WARN " to the decision
	// log from anywhere but the brain — the invariant parser counts those
	// tokens (a "STRIKE recorded" line here once doubled every strike and
	// failed I01 x4). Harness evidence uses its own token, RETAKE.
	LogLine(FString::Printf(TEXT("RETAKE take=%d lost=%s dailies=%d items_lost=%d"),
	                        Take, *Lost, Dailies.Num(), ItemsLost));
	bInRetake = false; // HARNESS STAND-IN (S8), see above
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

#include "BenchCapture.h"
#include "RestorationState.h"
#include "Rundown.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "Kismet/GameplayStatics.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"

namespace
{
	constexpr float M = 100.0f;
}

ABenchCapture::ABenchCapture()
{
	PrimaryActorTick.bCanEverTick = true;
	RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
}

void ABenchCapture::BeginPlay()
{
	Super::BeginPlay();
	if (bTestAutoStart)
	{
		TestArm = 1.0f;
	}
}

FString ABenchCapture::GetPrompt() const
{
	if (bRunning)
	{
		return TEXT("TAPE ROLLING · stay with it");
	}
	URestorationState* State = GetGameInstance()->GetSubsystem<URestorationState>();
	return FString::Printf(TEXT("THE BENCH · begin capture, Tape %d (E) · runs real time"),
	                       State ? State->CurrentTape : 1);
}

void ABenchCapture::Interact(AActor* InPlayer)
{
	if (bRunning || !InPlayer)
	{
		return;
	}
	URestorationState* State = GetGameInstance()->GetSubsystem<URestorationState>();
	bRunning = true;
	Player = InPlayer;
	T = CaptureSeconds;
	if (State)
	{
		State->bRecording = true;
		State->RecordingLeft = CaptureSeconds;
		// the teach: his first contract starts close (spec: teleport beside
		// the library when af_active and not yet taught)
		if (State->bAfActive && !State->bAfTaught)
		{
			TArray<AActor*> Rd;
			UGameplayStatics::GetAllActorsOfClass(GetWorld(), ARundown::StaticClass(), Rd);
			if (Rd.Num() > 0)
			{
				Rd[0]->SetActorLocation(FVector(-5.0f * M, -16.0f * M, 0));
			}
		}
	}
	LogLine(FString::Printf(TEXT("CAPTURE start tape %d"), State ? State->CurrentTape : 1));
}

void ABenchCapture::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	if (TestArm > 0.0f)
	{
		TestArm -= DeltaSeconds;
		if (TestArm <= 0.0f)
		{
			// harness: nearest pawn is the player
			APawn* P = Cast<APawn>(UGameplayStatics::GetActorOfClass(GetWorld(),
			                       APawn::StaticClass()));
			TArray<AActor*> Pawns;
			UGameplayStatics::GetAllActorsOfClass(GetWorld(), APawn::StaticClass(), Pawns);
			AActor* Best = nullptr;
			float BestD = TNumericLimits<float>::Max();
			for (AActor* A : Pawns)
			{
				const float D = FVector::Dist(GetActorLocation(), A->GetActorLocation());
				if (D < BestD) { BestD = D; Best = A; }
			}
			Interact(Best);
		}
	}
	if (!bRunning)
	{
		return;
	}
	URestorationState* State = GetGameInstance()->GetSubsystem<URestorationState>();
	if (Player && FVector::Dist(GetActorLocation(), Player->GetActorLocation()) / M > Tether)
	{
		bRunning = false;
		if (State)
		{
			State->bRecording = false;
			State->RecordingLeft = 0.0f;
		}
		LogLine(TEXT("CAPTURE ABORTED · the take is lost"));
		return;
	}
	T -= DeltaSeconds;
	if (T <= 0.0f)
	{
		bRunning = false;
		if (State)
		{
			State->bRecording = false;
			State->RecordingLeft = 0.0f;
			FRestorationCapture Cap;
			Cap.Name = FString::Printf(TEXT("TAPE %d · A CLEAN SIGNAL"), State->CurrentTape);
			Cap.Tape = State->CurrentTape;
			Cap.At = TEXT("BENCH");
			State->Captures.Add(Cap);
			LogLine(FString::Printf(TEXT("TAPE %d · A CLEAN SIGNAL"), State->CurrentTape));
		}
	}
	else if (State)
	{
		State->RecordingLeft = T;
	}
}

void ABenchCapture::LogLine(const FString& Text) const
{
	const FString Path = FPaths::Combine(FPaths::ProjectSavedDir(), TEXT("decision_log.txt"));
	FFileHelper::SaveStringToFile(Text + LINE_TERMINATOR, *Path,
	                              FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM,
	                              &IFileManager::Get(), FILEWRITE_Append);
	UE_LOG(LogTemp, Log, TEXT("%s"), *Text);
}

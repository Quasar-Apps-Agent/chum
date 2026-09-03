#include "RitaCharacter.h"
#include "RestorationInteractable.h"
#include "AIController.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"

namespace
{
	constexpr float M = 100.0f;
}

ARitaCharacter::ARitaCharacter()
{
	PrimaryActorTick.bCanEverTick = true;
	GetCapsuleComponent()->InitCapsuleSize(35.0f, 88.0f);

	UCharacterMovementComponent* Move = GetCharacterMovement();
	Move->MaxWalkSpeed = WalkSpeed * M;                 // 310
	Move->MaxAcceleration = Accel * M;                  // 1000 (deliberate weight)
	Move->BrakingDecelerationWalking = Accel * M;
	Move->MaxWalkSpeedCrouched = WalkSpeed * CrouchMult * M; // 170.5
	Move->SetCrouchedHalfHeight(88.0f - CrouchDrop * M * 0.5f);
	Move->NavAgentProps.bCanCrouch = true;
	Move->bCanWalkOffLedges = true;

	Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
	Camera->SetupAttachment(RootComponent);
	Camera->SetRelativeLocation(FVector(0, 0, 60.0f)); // eye ~1.48m above ground
	Camera->bUsePawnControlRotation = true;
}

void ARitaCharacter::BeginPlay()
{
	Super::BeginPlay();
	CamBaseZ = Camera->GetRelativeLocation().Z;
	if (bTestAutoWalk && !GetController())
	{
		// possess with an AI controller so AddMovementInput is consumed
		if (AAIController* AI = GetWorld()->SpawnActor<AAIController>())
		{
			AI->Possess(this);
		}
	}
}

void ARitaCharacter::SetupPlayerInputComponent(UInputComponent* Input)
{
	Super::SetupPlayerInputComponent(Input);
	Input->BindAxis("MoveForward", this, &ARitaCharacter::MoveForward);
	Input->BindAxis("MoveRight", this, &ARitaCharacter::MoveRight);
	Input->BindAxis("Turn", this, &APawn::AddControllerYawInput);
	Input->BindAxis("LookUp", this, &APawn::AddControllerPitchInput);
	Input->BindAction("Crouch", IE_Pressed, this, &ARitaCharacter::ToggleCrouch);
	Input->BindAction("Interact", IE_Pressed, this, &ARitaCharacter::Interact);
}

void ARitaCharacter::MoveForward(float V)
{
	if (V != 0.0f)
	{
		AddMovementInput(GetActorForwardVector(), V);
	}
}

void ARitaCharacter::MoveRight(float V)
{
	if (V != 0.0f)
	{
		AddMovementInput(GetActorRightVector(), V);
	}
}

void ARitaCharacter::ToggleCrouch()
{
	bCrouched = !bCrouched;
	if (bCrouched)
	{
		Crouch();
	}
	else
	{
		UnCrouch();
	}
}

void ARitaCharacter::Interact()
{
	// the reach ray; interactables land with the bench loop (0.8b next boxes)
	FHitResult Hit;
	const FVector Start = Camera->GetComponentLocation();
	const FVector End = Start + Camera->GetForwardVector() * Reach * M;
	FCollisionQueryParams Q;
	Q.AddIgnoredActor(this);
	if (GetWorld()->LineTraceSingleByChannel(Hit, Start, End, ECC_Visibility, Q))
	{
		if (IRestorationInteractable* I = Cast<IRestorationInteractable>(Hit.GetActor()))
		{
			LogLine(FString::Printf(TEXT("INTERACT %s :: %s"),
			                        *GetNameSafe(Hit.GetActor()), *I->GetPrompt()));
			I->Interact(this);
		}
		else
		{
			LogLine(FString::Printf(TEXT("INTERACT hit %s"), *GetNameSafe(Hit.GetActor())));
		}
	}
}

void ARitaCharacter::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	// camera eases toward crouch height, as player.gd lerps it (12.0 * delta)
	const float TargetZ = CamBaseZ - (bCrouched ? CrouchDrop * M : 0.0f);
	FVector CamLoc = Camera->GetRelativeLocation();
	CamLoc.Z = FMath::FInterpTo(CamLoc.Z, TargetZ, DeltaSeconds, 12.0f);
	Camera->SetRelativeLocation(CamLoc);

	if (!bTestAutoWalk)
	{
		return;
	}
	// self-driving feel test: 3s flat walk (expect ~3.1), crouch, 3s more
	// (expect ~1.7), then report
	TestT += DeltaSeconds;
	AddMovementInput(GetActorForwardVector(), 1.0f);
	if (TestPhase == 0 && TestT >= 3.0f)
	{
		TestPhase = 1;
		LogLine(FString::Printf(TEXT("RITA walk speed=%.2f m/s (max=%.0f)"),
		                        GetVelocity().Size2D() / M,
		                        GetCharacterMovement()->MaxWalkSpeed));
		ToggleCrouch();
	}
	else if (TestPhase == 1 && TestT >= 6.0f)
	{
		TestPhase = 2;
		LogLine(FString::Printf(TEXT("RITA crouch speed=%.2f m/s camdrop=%.2f"),
		                        GetVelocity().Size2D() / M,
		                        (CamBaseZ - Camera->GetRelativeLocation().Z) / M));
	}
}

void ARitaCharacter::LogLine(const FString& Text) const
{
	const FString Path = FPaths::Combine(FPaths::ProjectSavedDir(), TEXT("decision_log.txt"));
	FFileHelper::SaveStringToFile(Text + LINE_TERMINATOR, *Path,
	                              FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM,
	                              &IFileManager::Get(), FILEWRITE_Append);
	UE_LOG(LogTemp, Log, TEXT("%s"), *Text);
}

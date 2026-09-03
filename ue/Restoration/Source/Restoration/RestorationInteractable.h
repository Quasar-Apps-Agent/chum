// The prompt is the tier boundary (object taxonomy): if it prompts, it is
// a promise. Interactables carry verbs, never drift, never lie.
#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "RestorationInteractable.generated.h"

UINTERFACE(MinimalAPI)
class URestorationInteractable : public UInterface
{
	GENERATED_BODY()
};

class RESTORATION_API IRestorationInteractable
{
	GENERATED_BODY()
public:
	virtual FString GetPrompt() const = 0;
	virtual void Interact(AActor* Player) = 0;
};

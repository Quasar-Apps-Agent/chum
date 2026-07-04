# RESTORATION · STEAM RICH PRESENCE SPEC v1
Doctrine: a friends list is a broadcast. The schedule may appear on it; the secrets may not. Presence strings are diegetic, spoiler-null, and localized through Steam's richpresence.vdf alongside the game's own waves.

## STATES AND STRINGS (english masters)
#Day            "Day %day% at WGLD"                    · default daytime
#OnAir          "ON AIR · do not knock"                · Broadcast.on_air true
#Bench          "At the bench · Tape %tape%"           · capture running
#Night          "After sign-off"                       · any night, INCLUDING every late-game state without exception
#Premiere       "THE GLADHOUSE RETURNS (LIVE)"         · premiere_live true (the Steam page already says this much)
#Credits        "Signing off"                          · credits scene
#Menu           "At the title card"

## SPOILER RULES (meta-silence, third surface)
Never: any ending name, DEAD AIR, the seance, the quiet room, the dock's contents, the once-ever moment, day numbers past 5. Nights are all one string on purpose: a friend watching a presence feed learns the schedule exists and nothing else. Chum's name appears in no presence string, same reason as ever.

## HOOKS (for the GodotSteam pass)
GameState already emits everything needed: day changes, Broadcast.on_air, capture status, premiere_live, plus the credits scene's _ready. One bridge script subscribes and calls Steam.setRichPresence("steam_display", key) with substitutions; the bridge ships alongside the achievements bridge and, like it, is absent under DEMO.

# RESTORATION · ACHIEVEMENTS DESIGN v1

## DOCTRINE
Achievements are extradiegetic and therefore dangerous here: a popup is an unscheduled broadcast. Three laws govern them.
1 · THE DEFERRAL RULE. No achievement may surface during a protected beat. Unlocks fire silently into a queue and flush only at two moments: the next morning toast, or the title screen. The glimpse, the fire tape, the premiere, every ending sequence, and the demo card are popup-free zones by construction, not by hope. (Engine shape: an achievements autoload with unlock(id) and a flush gate on night_changed(false) and title _ready.)
2 · THE META-SILENCE LEDGER. The in-game scarcity contracts extend to meta. The glimpse has NO achievement, ever: any ping confirms the moment, teaches hunting, and spends the scarcity twice. The warm unit is acknowledged only through the dock-completion achievement, whose text never mentions warmth. The seance grants one achievement for reaching the final answer, never per-answer pings that turn a wake into a checklist. Chum's name appears in no achievement title.
3 · THE VOICE. Titles and descriptions read in the accession ledger's register: short, procedural, slightly too calm. Hidden achievements (Steam-hidden) cover every ending and every secret; their pre-unlock face is the standard WGLD card.
Demo parity: the demo build ships with achievements disabled entirely, matching the save whitelist's spirit; nothing meta leaks forward either.

## THE LIST (name · description · trigger, mapped to existing state · hidden?)
A01 FIRST SIGNATURE · "The paper takes your name." · first sign_log success · no
A02 CAREFUL HANDS · "A capture, start to bars, in real time." · first clean capture · no
A03 THE SCOPE READS MASTER · "You turned the knob. The label did not care." · first gen knob use · no
A04 ON THE BEAT · "You answered with the room." · on-beat respond in a screening · no
A05 STILLNESS, HELD WHOLE · "The cup did not move." · QUIET stance success · no
A06 MID-MOTION · "You spoke to her during a break. She will resume." · interact with frozen Harriet · no
A07 HOLD YOUR APPLAUSE · "The seventh was a gift." · Harriet's note read (signals_known gains 7th) · no
A08 YOU WERE NOT QUIET · "It changed direction." · first heard-noise relocation · no
A09 TOMORROW'S DATE · "The loops of the R are yours." · presigned_seen · hidden
A10 THE ROWS KEEP THEIR ORDER · "Six units. Filed." · dock_done · no
A11 PER V. CARDONA · "Somebody's name is on something." · vess_credited · no
A12 NO SEARCHER SINGS · "You heard 1974, complete." · merle_1974 · hidden
A13 THE UNFINISHED LINE · "You watched the fire tape to the cut." · fire_tape_watched · hidden
A14 I'VE READ THE ENDING · "You stepped to the last answer." · leland_answers reaches 5 · hidden
A15 ORDER MATTERS · "B before C, the way the panel is labeled." · cascade_done · no
A16 THE LONG WAY AROUND · "The felt door has a key after all." · QUIET ROOM key gained · hidden
A17 INK · "Three entries were possible. One stands." · decision committed · no
A18 NEXT WEEK'S EPISODE · "Starring you." · first run_ended (sheet full or One Take) · no
A19 EMPTY DRAWER · "The loupe was last." · items_lost reaches 7 · hidden
A20 SEALED FOR BROADCAST · "Lock-in's just till air." · lockdown_done · no
A21 THERE'S COBBLER · ending THE BURN · hidden
A22 WELCOME HOME · ending THE NEW PRODUCER · hidden
A23 FILE UNDER: SAINTS · ending SIGN-OFF, Rita closes · hidden
A24 IT'S OKAY. NOBODY'S WATCHING. · ending SIGN-OFF, Leland closes · hidden
A25 SIGNED OFF · ending DEAD AIR · hidden, and its Steam art is the only all-black icon in the set
A26 FULL ACCESSION · "Every document in the building, read." · all D01 to D10 props inspected (needs a read-flags set; small engine delta) · no

## RARITY INTENT AND SHAPE
A01 to A05 are the first hour and should sit near 90 percent. A18 will out-earn several endings and that is correct: dying politely is part of the show. A25 targets low single digits and is never hinted. No grind meters, no percentage bars, no achievement for repetition: the game's verbs are careful, not numerous, and the meta must not teach farming a building that notices behavior.

## ENGINE DELTA (Commit 030 candidate)
achievements.gd autoload: unlock(id) idempotent, user://achievements.cfg, deferral queue with the two flush gates, a plain signal for the eventual GodotSteam setAchievement bridge (id table above is the API names), disabled under DEMO. Prop read-flags for A26. Estimated one commit, no new systems.

## ADDENDUM (c043)
A27 EVERYONE GOES HOME · "The reading was silence." · any ending, empty ledger, zero rows · hidden. A28 A ONE-WOMAN SHOW · "Every part, one performer." · ending 0 · hidden, and its icon is the only card in the set with a name on it. Ruling: ending 4c carries no achievement by design; peace is not a trophy. Ruling: A26 FULL ACCESSION remains at ten documents; the Peak dossier (D11) is extra credit, because completionism should not require waking him.

# RESTORATION · DEMO CUT PLAN v1 · TAPE 1, FREE
Per the release model: the trust arc is one arc, so the demo is its first act whole: Day 1, no startle until the last ninety seconds, ending on the in-tape lunge and the lit RESPOND sign. Target length 25 to 40 minutes; speedrun floor about 12. The demo save is the full game's save (schema v15); CONTINUE in the full program imports it, ledger and all, which is the promise printed on the end card.

## 1 · THE DEMO'S SHAPE (Day 1 only, reordered for the button)
Arrive → dresser and welcome packet → sign S1 (the save-costs-paper lesson, softened: demo paper is S1 and S5 only, three sheets each) → the mini-screening (the signs, the beat, the three stances, judged gently on Matinee defaults) → the bench: capture Tape 1 in real time → the lunge, the game's one startle, bars → smash cut to the rec room where the RESPOND sign lights one final time, alone, unasked → hold two seconds → END CARD. Night never falls in the demo. The schedule is a rumor the full game keeps.

## 2 · BOUNDARY SPEC
IN: Entry, Rec Room, Kitchen, Dorms, Library, Bench, and the corridor between; the binder, the map, TBC and photo-safe, the gen knob, the coat pegs at Day 1 state, Merle at the kettle with her Day 1 line, Harriet in her chair.
LOCKED, with in-fiction demo reasons written on the doors: everything past the library. Standard string: "SEALED · the club opens the rest when the contract is signed." The transmitter corridor adds: "You can hear it from here. That is enough for today."
OUT ENTIRELY: the Rundown, nights, dailies and the burn loop, the Floor Manager, the presigned page, the dock, the crate, the seance, all four assets, the ledger's decision, every ending word.
TEASED, deliberately: the casting sheet visible with zero lines; the dresser's seven items counted; the sealed doors themselves.

## 3 · THE ENDING MOMENT (exact)
Capture completes → bars hold 1.6 s → cut to rec room camera position (authored) → RESPOND sign lights, hum only, 2.0 s → END CARD on black, phosphor type:
"TAPE 1 OF 5. THE PROGRAM CONTINUES. Your ledger, your signatures, and your paper carry into the full game. WISHLIST RESTORATION."
Below, small: "The 58 Club thanks you for careful hands."
No input during the card for 3 s (protect the beat), then any key to title.

## 4 · SAVE CARRY AND ANTI-SPOILER GUARANTEES
Same save file, same schema; a demo_complete flag set at the card. The demo build must be INCAPABLE of writing: decision, assets, leland_answers, lockdown, finale, or any ending field: not merely gated, absent from its write path, so no demo save can arrive pre-spoiled or pre-progressed. Full game on first CONTINUE from a demo save: Merle acknowledges it, one line: "You came back. I told them you would."

## 5 · ENGINEERING DELTA (implementable as one commit against v0.9)
E1 const DEMO in game_state (build-time flag). E2 world_builder: demo door-reason override table; skip spawning Rundown, FM, dock, crate, seance, cascade, assets, ledger, fire pickup. E3 bed_prop: demo branch, "The club insists you sleep at home until the contract is signed." E4 objective_text: demo branch ending at "capture Tape 1." E5 capture_bench: on demo completion, trigger the end sequence instead of the daily mint. E6 end card scene (reuses title scene styling). E7 title: demo build shows TAPE 1 · FREE DEMO under the logo. E8 save writer: demo field whitelist. E9 demo funnel telemetry, local file only (started, S1, screening, capture, lunge, card, minutes), no network, disclosed in the readme. E10 Steam: separate demo app id per the plan; depot shares the project.

## 6 · DEMO QA PROBES
DP1 all sealed doors state the demo reason; DP2 the whitelist: hand-inspect a completed demo save for absent fields; DP3 the ending sequence uninterruptible by movement or pause; DP4 paper exhaustion at S1 still leaves S5 (no softlock); DP5 carry test: demo save into full build, Merle's line fires once.

## 7 · WHAT THE DEMO SELLS (so the cut never drifts)
Care as gameplay, one contradiction (the slate versus the scope, present on the bench), one warmth (Merle, the kettle), one law demonstrated (the beat, the stances), and exactly one scare, positioned as a promise of restraint. The demo's last playable input is answering a children's show politely. That is the game, miniaturized, and the reason the sign lighting alone at the end works: the player has already learned what it means, and now it is asking them, and the card interrupts the answer.

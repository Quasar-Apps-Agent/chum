# RESTORATION: THE BUILD PLAN
## From Master Document to Shipped Game

**Version 1.0** | Assumes the full canon stack: rubrics, concepts, plotline, design doc (with Part IV-B), walkthrough (Revision 2), routing doc, and the game master document. This plan turns those into a shippable product.

---

# PART I: ASSUMPTIONS AND THE THREE GATE-ZERO DECISIONS

## Scope Tiers (pick one; the plan flexes to it)

| Tier | Team model | Timeline | Budget band |
|---|---|---|---|
| **A: Solo-core** | One designer-director (you) plus fractional engineering support and contractors (audio, puppet, VO, ports) | 24 to 32 months | $60k to $180k cash out |
| **B: Small studio (baseline for this plan)** | 4 to 6 core (director/design, 2 engineers, environment artist, tech artist, producer-QA hybrid) plus the same contractor set | 18 to 20 months | $700k to $1.4M |
| **C: Funded** | 10 to 15, dedicated audio and animation in-house | 22 to 26 months | $2.5M to $4.5M |

All month numbers below are Tier B; Tier A multiplies content phases by roughly 1.5 and serializes them; Tier C compresses by parallelizing content waves, not systems.

## Gate 0 Decisions (week 1, before anything else)

**1. Engine.** Weighted criteria: media playback and frame-accurate scrubbing (the séance lives or dies here), render-target camera feeds at budget (Frame Discipline is dozens of live feeds), dynamic light control for the plunge and beacon work, team familiarity. Recommendation: Unreal 5 if hiring experienced 3D contractors (Lumen sells the compound, MediaFramework handles playback); Unity 6 if the core is programmer-designer hybrids (faster systems iteration, simpler video texture pipeline). Godot only at Tier A with a stylization tradeoff. Decide once, in writing, with the spike results from M0.

**2. Release model.** Boxed release with Tape 1 as the free demo, recommended. The trust arc (no-startle first act, armed escalation) is one arc; shipping Tape 1 alone as a paid chapter is marketing death, but shipping it free as a demo that ends on the in-tape lunge and the RESPOND sign is a conversion machine. The chaptered Poppy-cadence variant remains viable only as Tapes 1+2 bundled per drop; if chosen, add 3 months and a live-ops seat.

**3. The show footage.** The Gladhouse must exist as footage: episodes, the fire tape, the impossible tapes, four Chum era variants. Two paths: in-engine rendered "footage" with an artifact pass, or a real puppet shoot. **Recommendation, and it is the plan's one unsafe choice: build Chum for real.** One fabricated puppet (with variant dressings), a micro set or greenscreen, two to three weekend shoots against the master document's tape scripts. Authenticity is load-bearing (the plot's inciting anomaly is a physically impossible dub, which only reads if the physics are honest), the puppet doubles as the trailer, the merch prototype, and the photo-mode of the entire marketing campaign, and the cost (fabrication plus shoots, $25k to $60k) undercuts the tech-art time of faking it convincingly.

---

# PART II: PRODUCTION PHILOSOPHY

**The six sacred pillars (never descoped):** the four pillars from the design doc (craft is courtship, mediation is safety, format is law, the comfort is real), plus the one-lie rule and the earned-trigger scare discipline. Every cut proposal is tested against these first.

**Rubric-gated milestones.** This project owns two scoring instruments; the plan uses them as gates. Every written scene passes a Dark Ledger scored read before recording or implementation (floor law: nothing below 3 in load-bearing criteria ships to VO). Every milestone build gets a Dread Ledger pass with target bands: Vertical Slice at 3.7+ on Domains 1, 2, and 6; Alpha at 4.0 weighted; Ship gate at 4.2 weighted with at least two domain 5s argued in writing. The review is a scheduled ritual, calendar-blocked, evidence-cited per the instruments' own protocols.

**Fairness as CI.** The game's laws become automated invariants that run on every build (Part VI). If the Understudy ever harms on camera in a nightly test, the build is red. The fiction's rules are the test suite.

**The descope ladder (what dies first, in order):** mic input features → blocking C variants (ship A/B) → One Take mode (post-launch) → the NG+ nod (post-launch) → poltergeist prop staging density → exterior night sequence compression. **Never on the ladder:** any ending (all four ship or the game slips), the seventh signal, the dock contract, the bell, Merle's monologue, the burn-in rule.

---

# PART III: M0, PREPRODUCTION (Months 1 to 3)

## Workstream 1: Technical Risk Spikes (each 1 to 2 weeks, pass/fail criteria in writing)

1. **Tape-world pipeline.** Per-generation artifact simulation (tracking, dot crawl, chroma bleed, head-switch noise) as a controllable shader stack responding to player tool settings (TBC, tracking). Pass: one clip, four generation states, artifacts diegetic and tool-reactive, photosensitivity-safe mode verified.
2. **Frame Discipline rendering.** N live camera feeds as render targets with tally logic and the mediated-safety ruleset at 60fps on target hardware. Pass: 12 simultaneous feeds, one patchbay re-route, safety state provably correct in a test scene.
3. **The séance.** Frame-accurate jog/shuttle over video with a compositing layer (Leland moving between frames) and persistent wear state. Pass: step, jump-cue, wear write-through to save, reload persistence.
4. **Rundown AI v0.** Segment-based patrol with audio localization, camera-kill behavior, one unscripted seek. Pass: a bot survives a night using only audio cues; the AI never violates a grammar invariant in a 4-hour soak.
5. **Coverage Director v0.** Profile tracking (checker/sprinter/hider/averter) selecting between two blockings of one scare. Pass: deterministic profile from logged inputs; blocking selection explainable in the log.
6. **Power and patchbay sim.** Amperage budget, breaker trips, corridor liveness. Pass: the Night 4 sequence greyboxed end to end.
7. **Live-production finale loop.** Cue sequencing, switcher input mapping, sabotage events, retake checkpointing per cue. Pass: Phase 2 skeleton playable with placeholder everything.

## Workstream 2: Content Foundations
Greybox the full compound from the routing document (zones, stations, sightlines, the compactus, catwalks); art bible (compound naturalism vs tape-world spec, the show palette system, casting-drift wardrobe rules); audio bible (the Yamaoka-standard brief: hum floors, silence tells, segment themes, the bell's single sample); UI kit v0 (binder, ledger, cue signs, CG face licensing or commission).

## Workstream 3: The Show Production Setup
Puppet fabrication contract (Chum base plus 1971/1974/post-fire/4K dressing variants per the master doc tell-table); shoot planning against the master document's on-tape scripts (T1.5, T2.8, T3.4 fire tape, T4 impossibles, T5 live-composite plates); degradation pipeline design (shoot clean, degrade per generation in the tape-world shader, never bake artifacts into masters).

## Workstream 4: Casting and Writing Lock
Dark Ledger scored pass on every master-document scene (revision list from the floor); casting breakdowns out early, **Merle first and flagged as the project's hardest read** (warm-genuine, never warm-sinister; the ending-3 line reading is the audition scene); Chum's voice (live puppeteer-performer preferred over VO booth, for the finale's live scenes); Leland is text-only (no VO cost); the Floor Manager is a counting voice, one session.

## M0 Exit Criteria
All seven spikes passed or mitigated in writing; engine and release-model decisions signed; greybox walkable Tape 1 route; puppet contract signed; Merle shortlist of three.

---

# PART IV: THE MILESTONE PLAN (Tier B months)

## M1: Core Loop Playable (Months 4 to 6)
**Goal: the bench is a game.** Full restoration suite (bake, splice, capture with forced real time, audio bench and spectrogram, quality grading), the accession ledger with GEN field and conduct entries, log-station saves with the paper economy, burn-in persistence layer, Tape 1 content implemented rough with placeholder show footage, the response system with cue signs.
**Show production:** puppet shoot 1 (Tape 1 and Tape 2 episode material, the Quiet Game, the closing song).
**Exit:** a tester can play Tape 1 start to finish, ugly but true, and the T1.5 capture already produces dread with placeholder artifacts.

## M2: Vertical Slice (Months 7 to 9)
**Goal: prove both halves at shippable quality.** Tape 1 at final quality (art, audio, the shot show footage, the in-tape lunge) plus one Tape 3 night out of sequence: the compactus chase with Frame Discipline, power routing, the you're-on, and a real capture-to-take flow with the casting sheet.
**The VS answers the four flagged playtest questions early:** does forced real-time capture hold attention; does the casting sheet draw pilgrimages; does the take/retake flow read as threat; does the blooper-reel tell land as dread or demoralization.
**Gate:** Dread Ledger scored review, 3.7+ on Domains 1, 2, 6; Dark Ledger floor holds on all implemented text. Publisher/funding conversations, if any, happen off this build.
**Exit:** the slice terrifies a cold tester who owns none of our context.

## M3: Systems Complete (Months 10 to 13)
**Goal: every mechanic exists.** Rundown v1 full (patrols, camera-kills, unscripted seeks), Coverage Director with profile plus mood law (savoring mode), Grammar engine complete (windows, signals, formal-correctness protections), the séance full with the five-question thread and wear math, Burn Your Dailies loop, Approaches and Generations plumbing (GEN-tagged facts, the authored-gap table as data), power sim final.
**Content wave:** Tapes 2 and 3 implemented to alpha art; puppet shoot 2 (fire tape, era-variant pickups).
**Exit:** Tapes 1 through 3 playable in sequence; nightly invariant suite green for two consecutive weeks.

## M4: Content Complete Alpha (Months 14 to 16)
**Goal: the whole game exists.** Tapes 4 and 5 in (the set reveal, the dock, the glimpse, lockdown, all three finale phases with sabotage AI and the Vess variants), all four endings functional to script including Dead Air's divert and erase sequence, all twelve scares with A/B blockings (C per descope status), the solutions matrix implemented obstacle by obstacle, VO recorded and cut in, the interface lie built and access-controlled to ending 2's post-credits only.
**Gate:** Dread Ledger at 4.0 weighted; ending-thread bots run all four routes nightly.
**Exit:** anyone can play arrival to any ending without a developer in the room.

## M5: Beta and Tuning (Months 17 to 18)
**Goal: the numbers become feelings.** Tuning passes on every marked tunable (sheet lines, paper economy, wear rates, PT weights, grace windows, sabotage pressure) driven by cohort playtests (Matinee and Late Night cohorts separated); the tonal verification list (Merle's ending-3 read, the unison scene, the bell's mix level, savoring-mode pacing); accessibility certification pass (photosensitivity audit on every tape-world asset, caption completeness including directional captions, full remap, mic-free parity verified); localization if scoped; the buried-stratum assets finalized and verified minable (spectrogram content in the shipping audio files, the future-dated schedule frames, legal review on any real phone numbers); performance and platform cert prep.
**Gate:** Ship-gate Dread Ledger review at 4.2 weighted with the two argued 5s; the Peak Law memo written (what this game will be cited for in a jury room).

## M6: Ship (Months 19 to 20)
Cert, day-one patch discipline, launch. Post-launch backlog seeded from the descope ladder (One Take mode, blocking Cs, NG+ nod) plus community-response reserve for the ARG layer.

---

# PART V: TEAM AND EXTERNAL PLAN

**Core (Tier B):** Director/design (owner of canon and both ledgers), systems engineer (Rundown, Coverage Director, grammar, saves), gameplay/UI engineer (bench, séance, patchbay, binder), environment artist (the compound), tech artist (tape-world pipeline, Frame Discipline rendering, lighting), producer-QA hybrid (invariant suite ownership, playtest ops).
**Contract:** composer and sound designer engaged from M0 (audio is the genre's first pillar and cannot be a post-pass; the segment themes are level design), puppet fabricator and shoot crew, VO cast (Merle, Vess, Harriet, Chum performer, Floor Manager, Craik archival), 4K Chum groom specialist for ending 2's uncanny render, accessibility auditor, platform cert/porting house, key art.
**Tier A translation:** director absorbs design plus UI engineering with AI-assisted implementation; systems engineering is the fractional hire that cannot be skipped; everything else stays contract; content waves serialize.

---

# PART VI: TESTING AND VERIFICATION (the invariant suite)

The project's fairness laws run as automated tests on every build, nightly soaks, and pre-milestone certs. Red build blocks merge. The canonical invariants:

1. The Understudy never harms while on any live, respected camera.
2. It never enters the dock, the dead room, or the catwalks.
3. Monitor deception fires at most once per run, only via the Coverage Director's poisoned-well path, only with the static telegraph.
4. Every scripted startle is preceded by its 1.5 to 3 second silence window.
5. Every capture logs a readable trigger state (which fail condition, which system reads were available).
6. Grammar transitions occur only in valid windows; the Floor Manager's signal log matches world events.
7. Leland wear and all burn-in survive retake, reload, and crash recovery.
8. The casting sheet count, dailies canisters, and item-loss ledger reconcile after any sequence of captures and burns.
9. The four ending threads complete via scripted bots nightly, including the audition clause and the drilled-door hum variant.
10. The interface lie is unreachable outside ending 2's post-credit context, verified by attempted-access tests.

**Human verification cadence:** weekly cold-tester sessions from M2 (one person who has never seen the project, every week, forever); telemetry proxies for fear (avert frequency, save-station visits, casting-sheet approaches, headphone-removal moments self-reported); the standing question list from the docs tracked to answers with dates.

---

# PART VII: THE DOMAIN 8 WORKSTREAM (parallel, from M2)

Runs beside production, never ahead of canon. Trailer law: the capture scare is the trailer scare; never show the glimpse, never the bell, never the sheet filling. Demo equals Tape 1, free, ending on the lunge and the sign. Content-creator kit at beta (streamer-safe music toggle, mic-mode showcase, spoiler embargo map by scene code). Community seeds shipped inside the game, not around it: the spectrogram layer, the timecode-gap schedule, the era-variant tell table as discoverable, one real phone number if legal clears it. The ARG's future-dated episodes align to the post-launch content calendar so the fiction's fuse and the roadmap are the same document. Steam page live at M2 with the slice's assets; wishlist beats at puppet-reveal, demo, and date announce.

---

# PART VIII: RISK REGISTER (top ten, with owners)

1. **Tape pipeline underperforms** (authenticity is load-bearing): spike 1 gates the project; fallback is licensed hardware-emulation middleware. Owner: tech art.
2. **Coverage Director scope creep toward ML:** it is authored variant selection, never learned behavior; the profile is four booleans and a corridor histogram. Owner: systems.
3. **Sabotage AI soft-locks the finale:** fail-forward retake structure certified by bot soak; a cue can always be re-entered. Owner: systems.
4. **Merle casting misses warm-genuine:** audition scene is the ending-3 read; do not cast without it. Owner: director.
5. **Forced real-time capture bores:** content editing budget reserved in M4; the mitigation is cutting tape runtime, never adding a skip. Owner: director.
6. **Photosensitivity noncompliance in tape-world assets:** auditor engaged at M2, every asset passes the TBC-on mode. Owner: producer.
7. **Show footage reads as fake:** the puppet decision exists to kill this risk; if in-engine fallback is forced, budget doubles for tech-art time. Owner: tech art.
8. **Burn-in rule generates launch-week backlash:** pre-brief in UI copy, Matinee relief valve, and a director's note in the binder itself. Owner: director.
9. **Buried stratum leaks pre-launch:** asset encryption until day one; the community layer is a launch feature, not a build artifact. Owner: producer.
10. **Scope tier mismatch discovered late:** the descope ladder is pre-agreed in writing at Gate 0, so cutting is execution, not debate. Owner: producer.

---

# PART IX: THE FIRST 30 DAYS (do these now)

Week 1: Gate 0 decisions drafted; spike briefs 1 through 7 written with pass/fail lines; puppet fabricator quotes requested with the tell-table attached; Merle casting breakdown out.
Week 2: engine spike 1 and 2 running; compound greybox begun from the routing doc's schematic; Dark Ledger scored pass on the master document's ten dialogue scenes, revision list produced.
Week 3: spikes 3 and 4; audio bible drafted with the composer conversation started; invariant suite designed as a document (each law, its test, its telemetry).
Week 4: spikes 5 through 7; Gate 0 signed; M0 exit checklist owned; the Steam page's private draft started so marketing debt never accrues.

**The plan's one-line thesis:** systems are built once, content flows through them in tapes, both ledgers gate every milestone, and the fiction's laws are the test suite. The game about restoring something carefully gets built the same way.

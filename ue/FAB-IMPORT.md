# FAB / MEGASCANS IMPORT PATH (unit 0.4 · the pivot's payoff)

Account: owner's Epic account, signed in on this Mac (launcher + fab.com).
Plugin: Fab, enabled in Restoration.uproject (engine ships Fab + legacy
Bridge + MegascansPlugin; use FAB — Bridge is the deprecated path).

## THE PULL (owner or any hands at the editor, ~5 min per batch)
1. Open ue/Restoration/Restoration.uproject in the UE 5.8 editor.
2. Window → Fab. Sign-in inherits the machine's Epic session.
3. Search each item below → price filter FREE → "Quixel Megascans" filter.
4. Add to My Library → Download → drag into Content/Megascans/<Category>.
   Choose quality MEDIUM (2K) — the texture budget law (2K default,
   4K only Chum + readables) applies to scans too.

## THE STARTER SET (per the Room Bible's twenty rooms)
Surfaces: worn parquet wood floor · industrial concrete floor · office
carpet (short pile, 70s tone) · plaster wall (painted, aged) · acoustic
ceiling tile · brick (painted-over) · linoleum/checker · steel plate ·
riveted/painted metal panel · stage floorboards (dark).
Decals: coffee stains · scuffs/tire marks · water damage · soot/burn
edges (FIRE CORRIDOR's shadowline) · tape residue.
Props (if free tier has them): cardboard boxes · metal shelving · wooden
crates · cable coils · fire extinguisher · folding chairs.

## AFTER EVERY PULL (non-negotiable, per plan §2)
- Log each asset id + name in ue/CREDITS-FAB.md (Fab license, this UE game).
- The WEAR PASS: nothing ships showroom-new — material instance with
  grime/desat parameters, or run it under tools/sodium_check.py --subject
  via a Blender round-trip if it's a mesh.
- Naming law on placement: MI_<Room>_<Surface> instances; masters stay in
  Content/Megascans as imported.

## WHY NOT HEADLESS
Fab has no scripted-download API; the plugin is editor-UI only. The pull
is the one manual step in the pipeline; everything after it (placement,
instancing, wear) is scripted per room in Phase 3.

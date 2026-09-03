# RESTORATION · BLENDER TO UE5 PIPELINE v1
Ruling recorded: the production build is UNREAL ENGINE 5, assets authored in BLENDER, per the author. The Godot build stands as the executable specification (it runs; see docs/telemetry/first-boot). Spike 2 is no longer a veto, only a routine perf validation on target hardware.

## DIVISION OF LABOR
BLENDER: modeling, UVs, rigging (Chum's jaw lever, sockets), scan cleanup and retopo, fixture meshes with true bulb geometry. UE5: materials, lighting, assembly, gameplay, sequencing. SCAN-FIRST stands from the art bible: the fabricated stage Chum is photographed and photogrammetried; Blender cleans and retopos; the material library is born from his wool and travels outward. The after-fire body is a digital kitbash of the scanned materials plus a hardware library; no second hero fabrication.

## STANDARDS (so nothing is renegotiated per asset)
Units: Blender scene in meters, FBX export with the UE preset so 1 m lands as 100 uu; UE is X-forward, Z-up; verify once on a 1 m cube and write the result on the wall. Naming: SM_ static, SK_ skeletal, M_ or MI_ materials, T_ textures with _BC _N _ORM suffixes; collision as UCX_ children in Blender so import is automatic; sockets SOCKET_JawLever, SOCKET_EyeTally, SOCKET_Bell (clapperless). Textures: ORM packed; 2K default, 4K only for Chum and the readables. LODs: crafted-world polycounts are modest by doctrine; LOD1 for set dressing only, hero props none.

## MATERIAL MASTERS (parents in UE, parameters named per the art bible)
M_Wool (subsurface, sodium-honest), M_TapeStock, M_Phosphor (emissive hybrid for monitors), M_Paper (the readables' stocks), M_Enamel (panels; where the pin fuses), M_Practical (fixture glass). The SODIUM CHECK is a permanent Blender lookdev scene: one sodium-spectrum lamp, neutral floor; every material passes through before export. If it lies under sodium it does not ship: the same gate as always, now with a fixed address.

## VERSIONING AND FLOW
Binary .uasset means the repo gains git LFS for Content (or the project moves to Perforce at Tier B; decide at Gate 0 signing). The port kit's Data CSVs remain the single source for rooms, doors, and timings: the level is BUILT FROM DATA in UE exactly as in Godot; build_greybox.py already proves the pattern and grows into the real constructor. Import automation extends that script: batch FBX import with the naming rules enforced, so the pipeline complains instead of the artist remembering.

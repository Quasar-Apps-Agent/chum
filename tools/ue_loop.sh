#!/bin/zsh
## The Blender→Unreal automation loop, one command (plan §4, unit 0.2).
##   tools/ue_loop.sh                      — calibration cube end-to-end
##   tools/ue_loop.sh <blend> <objects> <SM_Name>
##       exports <objects> (comma-sep) from <blend> as ue/exports/<SM_Name>.fbx,
##       imports into /Game/Imported, stages the look-dev level, captures to
##       renders/ue_<SM_Name>.png
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UE="/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac"
BLENDER="/Applications/Blender.app/Contents/MacOS/Blender"
PROJ="$ROOT/ue/Restoration/Restoration.uproject"

if [ $# -eq 0 ]; then
  NAME="SM_UnitCube"
  "$BLENDER" --background --python "$ROOT/tools/export_ue.py" -- --cube | grep UE-EXPORTED
else
  BLEND="$1"; OBJS="$2"; NAME="$3"
  "$BLENDER" --background "$BLEND" --python "$ROOT/tools/export_ue.py" -- \
    --objects "$OBJS" --out "ue/exports/$NAME.fbx" | grep UE-EXPORTED
fi

export UE_IMPORT_FILES="$ROOT/ue/exports/$NAME.fbx"
"$UE/UnrealEditor-Cmd" "$PROJ" -run=pythonscript \
  -script="$ROOT/ue/pyscripts/import_fbx.py" -unattended -nop4 -nosplash 2>&1 \
  | grep -oE "IMPORT-(OK|FAIL|DONE).*" | sort -u

export UE_AUTOCAPTURE=1
export UE_CAPTURE_ASSET="/Game/Imported/$NAME"
export UE_CAPTURE_OUT="$ROOT/renders/ue_${NAME}.png"
## init_unreal.py (Content/Python) picks up the env gate — survives paths
## with spaces where -ExecCmds="py ..." cannot
"$UE/UnrealEditor" "$PROJ" -unattended -nop4 -nosplash -RenderOffscreen \
  > /dev/null 2>&1
ls -la "$UE_CAPTURE_OUT" 2>/dev/null && echo "LOOP-COMPLETE $NAME"

#!/bin/zsh
# LOCAL Mac runner for the RESTORATION build routine — the on-Mac
# replacement for the cloud schedule. Each pass runs ONE unit headlessly
# in a fresh Claude Code session (the plan is self-orienting, so no context
# is needed), then sleeps. Runs in YOUR logged-in session, so Blender and
# Unreal headless rendering work exactly as they do interactively.
#
# Start:  open Terminal, then:  ./tools/run-mac-loop.sh
# Stop:   Ctrl-C.
#
# --dangerously-skip-permissions lets it build, commit and push unattended.
# That is the point of a routine; know that it acts on the repo on its own.

set -e
cd "/Users/christianabowen/Desktop/restoration-godot 3" || exit 1

PROMPT='Follow AAA_BUILD_PLAN.md session protocol exactly. Confirm the repo is green, take the FIRST unchecked box in PROGRESS.md that this Mac can run, complete that ONE unit, run the full verification loop and look at every render/capture with your own eyes, then tick the box, append the README ledger entry, copy current renders to the Desktop, git commit and git push. One unit per pass. Never leave the repo red. If the only remaining work needs input the owner must give, stop and say so instead of guessing.'

fails=0
while true; do
  echo "======== $(date '+%Y-%m-%d %H:%M:%S') · starting a unit ========"
  if claude -p "$PROMPT" --dangerously-skip-permissions; then
    fails=0
  else
    fails=$((fails + 1))
    echo "(pass exited non-zero · consecutive failures: $fails)"
    if [ "$fails" -ge 3 ]; then
      echo ""
      echo "!! Three passes failed in a row. Most likely the CLI is not logged in."
      echo "!! Fix:  claude login    (authenticate once), then re-run this script."
      exit 1
    fi
  fi
  echo "======== $(date '+%Y-%m-%d %H:%M:%S') · pass complete · sleeping 90s (Ctrl-C to stop) ========"
  sleep 90
done

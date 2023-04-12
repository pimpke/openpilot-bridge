#!/bin/bash
tmux new -d -s carla-sim
if [[ "${SHOULD_RUN_OPENPILOT_SIM}" == "1" ]]; then
  tmux send-keys "cd /openpilot/tools/sim && ./launch_openpilot.sh" ENTER
  tmux neww
  tmux send-keys "cd /openpilot/tools/sim && ./bridge.py $*" ENTER
  tmux neww
fi
tmux send-keys "set -x" ENTER
tmux send-keys "python --version" ENTER
tmux send-keys 'echo $PYTHONPATH' ENTER
tmux send-keys 'PYTHONPATH=/openpilot:/openpilot_bridge python -u main.py' ENTER
tmux a -t carla-sim
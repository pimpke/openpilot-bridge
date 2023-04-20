#!/bin/bash
if [ "${SHOULD_BUILD_OPENPILOT}" == 1 ]; then
  cd /openpilot
  scons -u -j$(nproc)
  exit 0
fi

tmux new -d -s default
if [[ "${SHOULD_RUN_OPENPILOT_SIM}" == 1 ]]; then
  tmux send-keys "cd /openpilot/tools/sim && ./launch_openpilot.sh" ENTER
  tmux neww
  tmux send-keys "cd /openpilot/tools/sim && ./bridge.py $*" ENTER
  tmux neww
fi
if [[ "${SHOULD_RUN_FAKE_CAN}" == 1 ]]; then
  tmux send-keys 'PYTHONPATH=/openpilot:/openpilot-bridge python -u fake_can.py' ENTER
  tmux neww
fi
tmux send-keys 'PYTHONPATH=/openpilot:/openpilot-bridge python -u main.py' ENTER
tmux a -t default

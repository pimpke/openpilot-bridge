#!/bin/bash

export DEBUG=1

if [ "${SHOULD_BUILD_OPENPILOT}" == 1 ]; then
  cd /openpilot || exit

  if [[ "${SHOULD_CLEAN_OPENPILOT}" == 1 ]]; then
    scons --clean
  fi

  rm -rf /tmp/scons_cache
  mkdir /tmp/scons_cache
  scons -u "-j$(nproc)"
  exit 0
fi

echo 'set -g prefix C-b' >> ~/.tmux.conf
tmux new -d -s default
if [[ "${SHOULD_RUN_OPENPILOT_SIM}" == 1 ]]; then
  tmux send-keys "cd /openpilot/tools/sim && ./launch_openpilot.sh" ENTER
  tmux neww

  tmux send-keys "cd /openpilot/tools/sim && ./bridge.py $*" ENTER
  tmux neww
fi
if [[ "${SHOULD_RUN_FAKE_CAN}" == 1 ]]; then
  tmux send-keys 'python -u fake_can.py' ENTER
  tmux neww
fi
if [[ "${SHOULD_RUN_BOARDD}" == 1 ]]; then
  tmux send-keys "./launch_boardd.sh" ENTER
  tmux neww
fi

if [[ "${SHOULD_RUN_TEST_PROCESSES}" == 1 ]]; then
  tmux send-keys "cd /openpilot/selfdrive/test/process_replay && ./test_processes.py" ENTER
  tmux neww
fi

tmux send-keys 'python -u control_bridge.py' ENTER
tmux neww

tmux send-keys 'python -u main.py' ENTER
tmux a -t default

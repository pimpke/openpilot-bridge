#!/bin/bash

tmux new -d -s default

tmux send-keys "cd ${HOME}; ./CarlaUE4.sh -nosound -benchmark -RenderOffScreen -fps=20 -quality-level=Low" ENTER
tmux neww

tmux send-keys "python3 carla_watchdog.py" ENTER

tmux a -t default

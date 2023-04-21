#!/bin/bash

export PASSIVE="0"
#export NOBOARD="1"
#export SIMULATION="1"
#export FINGERPRINT="HONDA CIVIC 2016"

export BLOCK="camerad,loggerd,navd,ui,soundd,deleter,logmessaged,thermald,statsd"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd /openpilot/selfdrive/manager && ./manager.py

#!/bin/bash

scr='ps_bot'
command='./run.sh'

if screen -list | grep -q $scr; then
    echo "Already running '$scr'."
else
    echo "Starting screen session: '$scr'"
    screen -dmS $scr sh -c $command
fi


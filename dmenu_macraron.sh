#!/bin/bash
if [ "$1" == "" ]; then
    python macraron.py -l | dmenu | xargs python macraron.py -x
else
    python macraron.py -x $@
fi

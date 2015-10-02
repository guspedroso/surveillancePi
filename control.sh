#!/bin/bash
args=("$@") ;

if [ "${args[0]}" = 'start' ]; then
        echo "[`date`] Starting motion.." ;
        sudo service motion start ;
elif [ "${args[0]}" = 'stop' ]; then
        echo "[`date`] Stopping motion.. " ;
        sudo service motion stop ;
fi

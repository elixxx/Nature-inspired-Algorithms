#!/bin/bash
for i in `seq 1 30`;
do
    echo $i
    PYTHONPATH=./ python experiment_de.py
    echo "DONE"
done
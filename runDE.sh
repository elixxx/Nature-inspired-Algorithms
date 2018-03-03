#!/bin/bash
if [ -d miniconda ]
then
    source miniconda/bin/activate nia
    export PYTHONPATH=../../.
    echo "Executing DE"
    echo "Problem 1"
    python experiment_de.py
    echo "Problem 2"    
    python experiment_de_problem2.py
    echo "Problem 3"    
    python experiment_de_problem3.py
else
    echo "miniconda not found,"
    echo "you probably have to install it by running:"
    echo "./makeEnv.sh"
fi



if [ -d miniconda ]
then
    source miniconda/bin/activate nia
    export PYTHONPATH=.
    echo "Executing Genetic Algorithm"
    python experiment_ga.py
else
    echo "miniconda not found,"
    echo "you probably have to install it by running:"
    echo "./makeEnv.sh"
fi



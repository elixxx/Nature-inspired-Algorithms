if [ -d miniconda ]
then
    source miniconda/bin/activate nia
    cd problems/travelling_salesman/
    export PYTHONPATH=../../.
    echo "Executing ACO"
    python main_parallel.py
else
    echo "miniconda not found,"
    echo "you probably have to install it by running:"
    echo "./makeEnv.sh"
fi



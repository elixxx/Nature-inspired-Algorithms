echo "Getting latest Miniconda version"
wget -q https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

echo "Installing Miniconda"
bash Miniconda3-latest-Linux-x86_64.sh -b -p "miniconda"
rm Miniconda3-latest-Linux-x86_64.sh

echo "Create and activate eviroment nia"
source miniconda/bin/activate
conda create -y -q --name nia python=3
source activate nia

echo "Install requirements"
conda info --envs | grep '*'
pip install --upgrade -r requirements.txt

echo "Miniconda enviroment nia (Natural inspired Algorithms) created, activate by:"
echo "source miniconda/bin/activate nia"


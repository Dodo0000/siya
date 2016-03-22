#!/usr/bin/env bash


echo "Removing old versions of ALMS..."

if [ -d "alms" ];then
  rm -R alms  ## if an old version of alms exists, then remove it
fi

rm -f alms.zip

echo "Removed old version of ALMS in the current directory"

echo "Downloading the latest version of ALMS..."

wget https://github.com/ayys/alms/archive/master.tar.gz -O alms.tar.gz

echo "Done Downloading the latest version of ALMS"

echo "Extracting alms.zip into the alms in the current directory..."

mkdir alms
cd alms
tar -xvf alms.tar.gz

echo "Done extracting alms"

echo "installing dependencies through pip..."

pip install --user -r install_requirements.txt

echo "Done installing dependencies"

echo "creating a global script for everyone to use"
mkdir -p $HOME/bin

echo PATH="$PATH:$HOME/bin" > $HOME/.custom_bins
echo "source $HOME/.custom_bins" > $HOME/.bashrc

echo "please restart bash"

echo "Installation Complete"
echo
echo "You can now run ALMS by running start-alms"

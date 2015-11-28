#!/usr/bin/env bash

## download from github
sudo apt-get install git
sudo apt-get install nginx
pip install --user -r install_requirements.txt

cd ~
if [ -d "alms" ];then
  rm -R alms
fi
git clone https://github.com/ayys/alms
cd alms
./start.sh

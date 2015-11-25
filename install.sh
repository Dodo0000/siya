#!/usr/bin/env bash

## download from github
sudo apt-get install git

cd ~
if [ -d "alms" ];then
  rm -R alms
fi
git clone https://github.com/ayys/alms
cd alms
./start.sh

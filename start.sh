#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
  pip install -r $HOME/alms-env/alms/requirements.txt
  ./manage.py makemigrations
  ./manage.py migrate
  ip=ifconfig|grep "inet addr"|awk -F':' '{print $2}'|awk -F" " '{ print $1 }'
  echo "The server has been started at the following addresses http://$ip"
  ./manage.py runserver_plus 0.0.0.0:8000
  echo
else
  echo "Root is for the dirt! Take me somewhere higher!"
fi

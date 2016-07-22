#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
  $HOME/alms/manage.py makemigrations
  $HOME/alms/manage.py migrate
  ifconfig $1 | grep "inet addr" | awk -F: '{print $2}' | awk -F" " '{print $1}'
  echo "The server has been started at the following addresses http://$ip"
  gksudo $HOME/alms/manage.py runserver_plus 0.0.0.0
  echo
else
  echo "Root is for the dirt! Take me somewhere higher!"
fi

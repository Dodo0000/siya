#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
  pip install --user -r requirements.txt
  ./manage.py makemigrations
  ./manage.py migrate
  ./manage.py runserver_plus &>> serverlog
  sleep 10
  if which xdg-open > /dev/null;then
    xdg-open http://localhost:8000 &> browserlog
  elif which gnome-open > /dev/null; then
    gnome-open http://localhost:8000 &> browserlog
  fi
else
  echo "Root is for the dirt! Take me somewhere higher!"
fi

#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
  pip install --user -r requirements.txt
  ./manage.py makemigrations
  ./manage.py migrate
  ./manage.py runserver_plus
else
  echo "Root is for the dirt! Take me somewhere higher!"
fi

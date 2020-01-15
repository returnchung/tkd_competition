#!/bin/sh

if [ "$1" == "dev" ]
then 
    FLASK_ENV=development \
    python index.py
else
    python index.py
fi

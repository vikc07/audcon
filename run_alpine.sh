#!/usr/bin/env bash

ROOT=/audcon
CONFIG=/config

if [[ ! -z "$1" ]]
    then
        ROOT=$1
fi
 
if [[ ! -e "$ROOT" ]]
    then
        echo "$ROOT dir does not exist"
        exit 1
fi

if [[ -e "$CONFIG" ]]
    then
        cp -f "$ROOT/audcon/cfg/default.json" "$CONFIG/default.json"
        rm -rf "$ROOT/audcon/cfg"
        ln -s "$CONFIG" "$ROOT/audcon/cfg"
fi

cd $ROOT
FLASK_APP=app.py FLASK_DEBUG=1 flask run -h 0.0.0.0
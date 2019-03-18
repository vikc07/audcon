#!/usr/bin/env bash

if [[ -e /config ]]
    then
        cp -f /audcon/audcon/cfg/default.json /config/default.json
        rm -rf /audcon/audcon/cfg
        ln -s /config /audcon/audcon/cfg
fi

cd /audcon
FLASK_APP=app.py FLASK_DEBUG=1 flask run -h 0.0.0.0
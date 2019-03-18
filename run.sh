#!/usr/bin/env bash
cd /audcon
FLASK_APP=app.py FLASK_DEBUG=1 flask run -h 0.0.0.0
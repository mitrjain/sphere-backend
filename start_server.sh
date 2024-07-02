#!/bin/bash

fuser -k 8000/tcp
source sphere-env/bin/activate
python3 create_tables.py
python3 manage.py runserver 0.0.0.0:8000
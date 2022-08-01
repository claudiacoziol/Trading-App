#!/usr/bin/env bash

python -m flask db migrate
python -m flask db upgrade
python -m flask run --host=0.0.0.0 --port=5000
#!/bin/sh
mkdir cal_coach_app
cd cal_coach_app

python3.11 -m venv my_env
source my_env/bin/activate

pip3 install -r ../requirements.txt

touch app.py
mkdir templates
cd templates
touch index.html
cd ..
mkdir static
cd static
touch style.css
cd ..

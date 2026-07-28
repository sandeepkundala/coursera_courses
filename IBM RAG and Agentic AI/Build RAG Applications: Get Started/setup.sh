#!/bin/sh
pip install virtualenv 
virtualenv my_env # create a virtual environment named my_env
# source my_env/bin/activate # activate my_env

# installing necessary pacakges in my_env
python3.11 -m pip install -r requirements.txt
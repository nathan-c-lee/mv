#!/bin/bash

sudo motion
echo "motion camera stream started"

source MVenv/bin/activate
echo "virtual environment activated"

source envconfig
echo "environment variables set"

echo "starting MORSEVIEW"
python run.py

echo "cleaning up GPIO"
python gpiocu.py

exit

#!/bin/bash

dos2unix lora-7010.py
dos2unix lora-7020.py

docker-compose -f "lora-docker-compose.yml" up -d --build

python lora-7010.py &

python lora-7020.py &
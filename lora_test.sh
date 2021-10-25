#!/bin/bash

 docker-compose -f "lora-docker-compose.yml" up -d --build

 python lora-txrx-6010.py

  python lora-txrx-6020.py
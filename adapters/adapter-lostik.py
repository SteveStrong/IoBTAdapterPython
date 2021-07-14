# adapter-lostik.py
# MQTT pub/sub that routes data to/from the code required to transport data with lostik
# lostik is a USB dongle LoRa radio
# https://ronoth.com/products/lostik?variant=31480579162244
#
# Topics
# /me/lora/lostik/rx
# /me/lora/lostik/tx
#
# Usage
# Run this script and it will automatically use the Lostik for transport based on MQTT on message events
# Another script is responsible for writing to/from MQTT



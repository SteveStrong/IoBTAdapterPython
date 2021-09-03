# iot-client

Handling IoT clients... sensors, assets (person, vehicle, etc), things (devices)

MQTT as message bus

Controllers/pan = person area network coordination

Adapters/adapter-lostik = comms using LoRa radio using the LoStik device

Documentation for eclipse-mosquitto:
https://mosquitto.org/documentation/

Specific documentation for mosquitto.conf configuration file authentication:
https://mosquitto.org/documentation/authentication-methods/

Usage:
In the parent directory of the mqttToIoBTListener.py script

python3 -m IoBTAdapterPython.mqttToIoBTListener.py


# Docker build and push to Azure
docker build -t iobt-adapter-python -f mqtt.Dockerfile  .

docker tag iobt-adapter-python iobtassets.azurecr.io/iobt-adapter-python
docker push iobtassets.azurecr.io/iobt-adapter-python

FROM eclipse-mosquitto:1.6
#
#
# https://hub.docker.com/_/eclipse-mosquitto
#
# From IoBTAdapterPython folder:
# docker build -t mqttbroker -f mqttbroker.Dockerfile  .
# docker run -it -p 1883:1883 --name mqttbroker mqttbroker
# az login
# az acr login --name iobtassets
# docker tag mqttbroker iobtassets.azurecr.io/mqttbroker:latest
# docker push iobtassets.azurecr.io/mqttbroker:latest
#
# From the IoBT docker compose git repository, use docker-compose.mqttbroker.yml

FROM eclipse-mosquitto
#
#  docker run -it -p 1883:1883 -p 9001:9001 -v mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
#
#  https://hub.docker.com/_/eclipse-mosquitto


COPY ./mosquitto/config/mosquitto.conf ./mosquitto/config/mosquitto.conf

# docker build -t mgttbroker -f mqttBroker.Dockerfile  .
# docker run -it -p 1883:1883 -p 9001:9001  mgttbroker
# docker run -dit -p 1883:1883 -p 9001:9001  mgttbroker /bin/bash
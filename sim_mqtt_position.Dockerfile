FROM python:3.8-slim-buster
#
# https://docs.docker.com/language/python/build-images/
#

WORKDIR /app
EXPOSE 8080
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Run the application:
RUN mkdir IoBTAdapterPython
COPY . ./IoBTAdapterPython

CMD python3 -m IoBTAdapterPython.sim_mqtt_position.py

# From IoBTAdapterPython folder:
# docker build -t sim_mqtt_position -f sim_mqtt_position.Dockerfile  .
# docker run -it sim_mqtt_position /bin/bash
# docker-compose up -d
# docker-compose down

# docker run -dit sim_mqtt_position

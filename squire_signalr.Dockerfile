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

CMD python3 -m IoBTAdapterPython.squire_signalr_bridge.py

# From IoBTAdapterPython folder:
# docker build -t signalr_bridge -f squire_signalr.Dockerfile  .
# docker run -it signalr_bridge /bin/bash
# docker-compose up -d
# docker-compose down

# docker run -dit sim_mqtt_position

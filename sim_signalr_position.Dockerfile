FROM python:3.8-slim-buster
#
# https://docs.docker.com/language/python/build-images/
#

WORKDIR /app
EXPOSE 8080
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Run the application:Ad    
RUN mkdir IoBTAdapterPython
COPY . ./IoBTAdapterPython

CMD python3 -m IoBTAdapterPython.sim_signalr_position.py

# From IoBTAdapterPython folder:
# docker build -t simsignalrposition -f sim_signalr_position.Dockerfile  .
# docker run -it simsignalrposition /bin/bash
# docker tag simsignalrposition iobtassets.azurecr.io/simsignalrposition:v4.6.3
# docker push iobtassets.azurecr.io/simsignalrposition:v4.6.3
# docker-compose up -d
# docker-compose down

# docker run -dit sim_mqtt_position

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

CMD python3 -m IoBTAdapterPython.mqttToIoBTListener.py

# From IoBTAdapterPython folder:
# docker build -t iobtbridge -f mqtt_test.Dockerfile  .
# docker run -it iobtbridge /bin/bash
# az login
# az acr login --name iobtassets
# docker tag iobtbridge iobtassets.azurecr.io/iobtbridge:v4.6.4
# docker push iobtassets.azurecr.io/iobtbridge:v4.6.4
#
# From the IoBT docker compose git repository, use docker-compose.iobtbridge.yml

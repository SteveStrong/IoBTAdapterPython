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
# docker build -t iobt-adapter-python -f mqtt.Dockerfile  .
# docker run -it iobt-adapter-python /bin/bash
# az login
# az acr login --name iobtassets
# docker tag iobt-adapter-python iobtassets.azurecr.io/iobt-adapter-python
# docker push iobtassets.azurecr.io/iobt-adapter-python
# docker-compose up -d
# docker-compose down

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

CMD python3 -m IoBTAdapterPython.sim_signalr_position.py

# From IoBTAdapterPython folder:
# docker build -t simsignalrposition -f sim_signalr_position.Dockerfile .
# docker run -it simsignalrposition /bin/bash
# az login
# az acr login --name iobtassets
# docker tag simsignalrposition iobtassets.azurecr.io/simsignalrposition:latest
# docker push iobtassets.azurecr.io/simsignalrposition:latest
#
# From the IoBT docker compose git repository, use docker-compose.simsignalrposition.yml

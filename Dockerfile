FROM python:3.8-slim-buster
#
# https://docs.docker.com/language/python/build-images/
#

#$ cd /path/to/python-docker
#$ pip3 install Flask
#$ pip3 freeze > requirements.txt
#$ touch app.py


# syntax=docker/dockerfile:1

WORKDIR /app
EXPOSE 8080
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Run the application:
# COPY . ./app/IoBTAdapterPython
RUN mkdir IoBTAdapterPython
COPY . ./IoBTAdapterPython

# CMD python3 ./IoBTAdapterPython/hello_world.py
CMD python3 -m IoBTAdapterPython.signalr_test.py

# docker run -it iobt-adapter-python /bin/bash


# docker build -t iobt-adapter-python -f Dockerfile  .
# docker run -d -p 8000:8000  -p 9200:9200 --name lasearch lasearchapi
# docker run -d -p 8000:8000   --name lasearch lasearchapi


# https://pythonspeed.com/articles/activate-conda-dockerfile/


# this conntainer need to connect to elastic.
# that shoud also be in a container
# https://markheath.net/post/exploring-elasticsearch-with-docker
FROM debian:jessie
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python python-pip

RUN pip install --upgrade requests pytest simplejson flask elasticsearch
WORKDIR /code
ADD . /code
EXPOSE 18013

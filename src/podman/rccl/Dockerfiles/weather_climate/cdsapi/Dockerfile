FROM ubuntu:bionic

RUN apt-get update && apt-get install -y python3.8-dev python3.8-distutils wget
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 2
WORKDIR /tmp
RUN wget  https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    pip install cdsapi

WORKDIR /
RUN rm -rf /tmp/*

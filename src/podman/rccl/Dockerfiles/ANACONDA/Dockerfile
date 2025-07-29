FROM ubuntu:18.04
RUN apt-get update

# Building GCC
RUN apt-get install --yes wget vim sudo build-essential gfortran

# Building MPICH3
WORKDIR /tmp
RUN wget http://www.mpich.org/static/downloads/3.2.1/mpich-3.2.1.tar.gz
RUN tar xvf mpich-3.2.1.tar.gz
WORKDIR mpich-3.2.1
RUN bash ./configure
RUN make -j4 VERBOSE=1
RUN make install
WORKDIR /
RUN rm -rf /tmp/*

# Building ACACONDA
WORKDIR /tmp
RUN wget https://repo.anaconda.com/archive/Anaconda3-5.3.0-Linux-x86_64.sh
RUN bash Anaconda3-5.3.0-Linux-x86_64.sh -b -p /usr/local/anaconda
WORKDIR /
RUN rm -rf /tmp/*
# So that the anaconda packages including Python3 is on PATH
ENV PATH="/usr/local/anaconda/bin:${PATH}"



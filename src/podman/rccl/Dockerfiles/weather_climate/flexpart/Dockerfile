FROM ubuntu
LABEL maintainer="Kadir Akbudak (kadir.akbudak@kaust.edu.sa)"
LABEL version="0.1.0"

RUN apt-get update && \
    apt-get install -y git gfortran libeccodes-dev libnetcdff-dev build-essential

ENV PATH /software/flexpart/src:$PATH
ENV CPATH=/usr/include:/usr/include/x86_64-linux-gnu/:/usr/lib/x86_64-linux-gnu/fortran/gfortran-mod-15/:$CPATH
ENV LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/:$LIBRARY_PATH
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/:$LD_LIBRARY_PATH

WORKDIR /software
RUN git clone --single-branch --branch master https://gitlab.phaidra.org/flexpart/flexpart.git && \
    cd flexpart/src && \
    make -f makefile_gfortran
WORKDIR /software/flexpart/src



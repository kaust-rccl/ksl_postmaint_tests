FROM debian:9.6
RUN apt-get update

# Building GCC
RUN apt-get install --yes wget vim sudo build-essential gfortran

# Building MPICH3
RUN mkdir /software /build
WORKDIR /build
RUN wget http://www.mpich.org/static/downloads/3.1.4/mpich-3.1.4.tar.gz
RUN tar xvf mpich-3.1.4.tar.gz
WORKDIR mpich-3.1.4
RUN bash ./configure 
RUN make -j 8 VERBOSE=1
RUN make install
WORKDIR /
RUN rm -rf /build 
RUN ldconfig 
ENV LD_LIBRARY_PATH="/usr/lib:/usr/local/lib:${LD_LIBRARY_PATH}"


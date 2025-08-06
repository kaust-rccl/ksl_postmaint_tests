FROM krccl/mpich_base:332
RUN apt-get update && apt-get install -y autoconf libudunits2-dev libnetcdf-dev wget flex
WORKDIR /tmp
RUN wget https://github.com/nco/nco/archive/refs/tags/4.8.1.tar.gz -O nco-4.8.1.tar.gz && tar xvf nco-4.8.1.tar.gz
WORKDIR /tmp/nco-4.8.1
RUN ./configure --enable-udunits --enable-ncap2 --enable-openmp && make VERBOSE=1 && make install
WORKDIR /
RUN rm -rf /tmp/*


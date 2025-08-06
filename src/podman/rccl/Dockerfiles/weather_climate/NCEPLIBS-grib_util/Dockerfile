FROM krccl/mpich_base:332_gcc10

RUN apt-get update
ENV DEBIAN_FRONTEND noninteractive
ENV PATH /software/bin:$PATH
ENV LD_LIBRARY_PATH /software/lib/:$LD_LIBRARY_PATH
RUN apt-get install -y git cmake wget gfortran libpng-dev zlib1g-dev libnetcdf-dev libnetcdff-dev
WORKDIR /tmp

RUN wget https://github.com/jasper-software/jasper/archive/refs/tags/version-2.0.25.tar.gz \
&& tar xvf version-2.0.25.tar.gz \
&& cd jasper-version-2.0.25 \
&& mkdir build2 && cd build2 \
&& cmake .. -DJAS_ENABLE_LATEX=OFF -DCMAKE_INSTALL_PREFIX=/software -DJAS_ENABLE_LIBJPEG=false \
&& make -j install \
&& cd ../../

RUN git clone https://github.com/NOAA-EMC/NCEPLIBS \
&& mkdir -p build && cd build \
&& cmake -DCMAKE_INSTALL_PREFIX=/software ../NCEPLIBS \
&& make -j -k

RUN git clone https://github.com/NOAA-EMC/NCEPLIBS-grib_util.git \
&& cd NCEPLIBS-grib_util/ \
&& git checkout v1.2.3 \
&& mkdir build && cd build \
&& export PKG_CONFIG_PATH=/software/lib/pkgconfig/:$PKG_CONFIG_PATH \
&& cmake .. -DCMAKE_software_PREFIX=/software -DJASPER_INCLUDE_DIR=/software/include/ -DJASPER_LIBRARIES=/software/lib/ -DJPEG_LIBRARIES=/usr/lib/x86_64-linux-gnu/ -Dbacio_DIR=/software/bacio-2.4.1/lib/cmake/bacio/ -Dip_DIR=/software/ip-3.3.3/lib/cmake/ip -Dsp_DIR=/software/sp-2.3.3/lib/cmake/sp \
&& make -j -k install

WORKDIR /
RUN rm -rf /tmp/*

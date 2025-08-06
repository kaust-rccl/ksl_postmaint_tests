FROM openmpi_403
RUN apt-get update && \ 
    apt-get install -y python3.8 swig git && \
    ln -s /usr/bin/python3.8 /usr/bin/python && \
    apt-get install -y scons libfftw3-dev
WORKDIR /opt/software
RUN git clone -b madagascar-3.1.1 https://github.com/ahay/src.git madagascar311 && \
    git clone https://github.com/DIG-Kaust/Mada_mrava_codes.git && \
    mv Mada_mrava_codes/mrava madagascar311/user && \ 
WORKDIR /opt/software/madagascar311




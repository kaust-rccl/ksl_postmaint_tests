FROM krccl/miniforge:latest
LABEL maintainer="Kadir Akbudak (kadir.akbudak@kaust.edu.sa)"
LABEL version="0.1.0"

RUN apt-get update && \
    apt install -y gfortran

RUN mamba create -n atmospheric-sciences -y -c conda-forge wgrib2 eccodes ncl nceplibs-bufr && \
    mamba clean --all --yes

RUN cd /software && \
    mkdir src && \
    cd src && \
    git clone https://github.com/NCAR/rda-prepbufr-decode.git && \
    cd rda-prepbufr-decode && \
    patch -p0 --ignore-whitespace <<'EOF'
--- install/install.sh
+++ install/install.sh
@@ -16,11 +16,11 @@
 #    https://emc.ncep.noaa.gov/emc/pages/infrastructure/bufrlib.php
 #
 # Replace LIB path with the path to BUFRLIB on your local system
-LIB=/path/to/bufrlib/lib/directory
+LIB=/software/envs/atmospheric-sciences/lib/

 # Path to fortran compiler
 fflag=""
-FC=/path/to/fortran/compiler/ifort
+FC=gfortran

 #  Compile the decode program
 #  ---------------------------------------
@@ -32,7 +32,7 @@
 #  -----------------------------

 echo "Linking ..."
-$FC $fflag -o $EXE/readpb_config.x readpb_config.o $LIB/libbufr_4.a
+$FC $fflag -o $EXE/readpb_config.x readpb_config.o $LIB/libbufr_4.so

 #  clean up
 #  --------
EOF

RUN cd /software/src/rda-prepbufr-decode/install && \
    ./install.sh

ENV LD_LIBRARY_PATH=""
ENV LD_LIBRARY_PATH="/software/envs/atmospheric-sciences/lib/:$LD_LIBRARY_PATH"
ENV PATH="/software/src/rda-prepbufr-decode/exe:$PATH"

WORKDIR /workdir
COPY entrypoint.sh /software/entrypoint.sh
RUN chmod +x /software/entrypoint.sh
ENTRYPOINT ["/software/entrypoint.sh"]

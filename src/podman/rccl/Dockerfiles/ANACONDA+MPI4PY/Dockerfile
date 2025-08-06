FROM debian:9.2
RUN apt-get update

# Building GCC
RUN apt-get install --yes wget vim sudo build-essential gfortran
RUN adduser default
RUN adduser default sudo

# Building MPICH3
RUN mkdir -p /software /build /workspace
WORKDIR /build
RUN wget http://www.mpich.org/static/downloads/3.1.4/mpich-3.1.4.tar.gz
RUN tar xvf mpich-3.1.4.tar.gz
WORKDIR mpich-3.1.4
RUN bash ./configure 
RUN make -j 4 VERBOSE=1
RUN make install
RUN ldconfig
RUN rm -rf /build
WORKDIR /

# Building ACACONDA
ENV HOME="/software"
RUN wget https://repo.anaconda.com/archive/Anaconda3-5.3.0-Linux-x86_64.sh
RUN bash Anaconda3-5.3.0-Linux-x86_64.sh -b -p /software/anaconda

# So that the anaconda packages including Python3 is on PATH
ENV PATH="/software/anaconda/bin:${PATH}"

# Building MPI4PY linked to container's own MPICH3
RUN env MPICC=/usr/local/bin/mpicc pip install mpi4py

# Install newer version of matplotlib in Anaconda as the default verison fails to import matplotlib.pyplot
RUN conda install -c conda-forge -y matplotlib=3.0.2
RUN conda install -c conda-forge  rebound
RUN pip install reboundx

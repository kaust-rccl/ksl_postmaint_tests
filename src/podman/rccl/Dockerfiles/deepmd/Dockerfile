FROM krccl/mpich_base:332
RUN apt-get update && \
    apt-get install -y python3.7-dev python3.7-distutils git vim wget cmake
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2

WORKDIR /tmp
RUN wget  https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py 
WORKDIR /software
RUN curl -L https://github.com/Kitware/CMake/releases/download/v3.24.0/cmake-3.24.0-linux-x86_64.sh -o /tmp/cmake-3.24.0-linux-x86_64.sh  && \
       sh /tmp/cmake-3.24.0-linux-x86_64.sh --prefix=/software --skip-license && \
       rm -rf /tmp/*

ENV PATH=/software/bin:${PATH}
ENV deepmd_source_dir=/software/deepmd-kit
ENV DP_VARIANT=cpu
RUN git clone --recursive https://github.com/deepmodeling/deepmd-kit.git deepmd-kit && \
    curl -L  https://storage.googleapis.com/tensorflow/libtensorflow/libtensorflow-cpu-linux-x86_64-2.11.0.tar.gz -o /tmp/libtensorflow-cpu-linux-x86_64-2.11.0.tar.gz && \
    tar xvf /tmp/libtensorflow-cpu-linux-x86_64-2.11.0.tar.gz && \
    pip install --upgrade --prefix=/software tensorflow-cpu && \
    cd ${deepmd_source_dir} && \
    pip install --prefix=/software .
RUN env MPICC=/usr/local/bin/mpicc HOROVOD_WITHOUT_GLOO=1 HOROVOD_WITH_TENSORFLOW=1 pip install horovod mpi4py
RUN cd ${deepmd_source_dir}/source && \
    mkdir build && cd build && \
    cmake -DTENSORFLOW_ROOT=/usr/local/lib/python3.7/dist-packages/tensorflow -DCMAKE_INSTALL_PREFIX=/software/deepmp_install ..







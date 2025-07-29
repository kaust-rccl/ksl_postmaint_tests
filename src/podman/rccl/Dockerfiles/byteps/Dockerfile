FROM krccl/horovod_gpu:0192
RUN apt-get install -y wget
ARG https_proxy
ARG http_proxy

ARG BYTEPS_BASE_PATH=/opt
ARG BYTEPS_PATH=$BYTEPS_BASE_PATH/byteps
ARG BYTEPS_GIT_LINK=https://github.com/bytedance/byteps
ARG BYTEPS_BRANCH=master
RUN cd $BYTEPS_BASE_PATH &&\
    git clone --recursive -b $BYTEPS_BRANCH $BYTEPS_GIT_LINK
WORKDIR $BYTEPS_PATH
RUN pip install -vvv --prefix=/usr/local .
WORKDIR /


FROM ubuntu:20.04
RUN apt-get update && apt-get install -y python3.8-dev python3.8-distutils wget git
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 2 

RUN wget  https://bootstrap.pypa.io/get-pip.py && \ 
          python get-pip.py 
RUN pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu116 
RUN pip install cloudml-hypertune

WORKDIR /opt/workload
COPY mnist.py . 
RUN chmod o+rx mnist.py


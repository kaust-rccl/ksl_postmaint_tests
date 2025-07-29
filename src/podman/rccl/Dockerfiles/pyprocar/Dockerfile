FROM ubuntu:18.04
RUN apt-get update && apt-get install -y \
    build-essential curl \
    libsm6 libx11-dev libxext-dev libgl-dev \
    python3 python3-distutils libpython3.6-dev 
WORKDIR /tmp
RUN mkdir /software
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py
ENV PYTHONPATH=/software/lib/python3.6/site-packages:/software/lib64/python3.6/site-packages
ENV PATH=$PATH:/software/bin
ENV LD_LIBRARY_PATH=/software/lib:/software/lib64:$LD_LIBRARY_PATH
RUN printenv
RUN pip install --prefix=/software vtk
RUN pip install --prefix=/software PyQt5
RUN pip install --prefix=/software numpy==1.17
RUN pip install --prefix=/software pyprocar

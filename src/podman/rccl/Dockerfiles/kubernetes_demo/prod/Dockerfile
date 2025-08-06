FROM ubuntu:21.04
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y wget
RUN useradd --create-home --shell /bin/bash jupyter_server
USER jupyter_server
ARG CONDA_HOME=/home/jupyter_server/miniconda
ARG TMP_DIR=/home/jupyter_server/tmpdir
WORKDIR ${TMP_DIR}
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -f -p ${CONDA_HOME}
ENV PATH=$PATH:${CONDA_HOME}/condabin:${CONDA_HOME}/bin
COPY environment.yml environment.yml
RUN conda env create -f environment.yml
WORKDIR /home/jupyter_server
RUN rm -rf ${TMP_DIR}
SHELL ["/bin/bash","-c"]
RUN conda init
RUN echo 'conda activate demo' >> ~/.bashrc
ENV PATH=$PATH:${CONDA_HOME}/envs/demo/bin
ENV HOME=/home/jupyter_server
COPY mnist.py /home/jupyter_server
EXPOSE 8888


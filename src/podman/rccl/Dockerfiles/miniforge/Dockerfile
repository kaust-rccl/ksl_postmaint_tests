FROM ubuntu:22.04
RUN apt-get update && apt-get install -y git wget vim
WORKDIR /tmp
RUN wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh && \
    bash Mambaforge-$(uname)-$(uname -m).sh -bsu -p /software
WORKDIR /workdir
ENV PATH=/software/bin:${PATH}
COPY entrypoint.sh /software/entrypoint.sh
RUN chmod +x /software/entrypoint.sh
ENTRYPOINT ["/software/entrypoint.sh"]


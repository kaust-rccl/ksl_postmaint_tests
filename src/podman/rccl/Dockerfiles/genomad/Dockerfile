FROM krccl/miniforge:latest
LABEL maintainer="Mohsin Ahmed Shaikh (mohsin.shaikh@kaust.edu.sa)"
LABEL version="1.5.0"

RUN mamba create -n genomad -y -c conda-forge -c bioconda genomad==1.5.0 && \
    mamba clean --all --yes

WORKDIR /workdir
COPY entrypoint.sh /software/entrypoint.sh
RUN chmod +x /software/entrypoint.sh
ENTRYPOINT ["/software/entrypoint.sh"]



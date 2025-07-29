# Use the respective Makefile to pass the appropriate BASE_IMG and build the image correctly
ARG BASE_IMG=<jupyter>
FROM $BASE_IMG

# nvidia configs
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

# install - requirements.txt
COPY --chown=jovyan:users cuda-requirements.txt /opt/requirements.txt
RUN python3 -m pip install -r /opt/requirements.txt --quiet --no-cache-dir 
#RUN rm /opt/requirements.txt

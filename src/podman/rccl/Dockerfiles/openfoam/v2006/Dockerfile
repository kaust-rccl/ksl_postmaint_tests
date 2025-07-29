FROM mshaikh/mpich332_ksl:latest
RUN apt-get update && \
	apt-get install -y build-essential flex bison cmake zlib1g-dev \
	libboost-system-dev libboost-thread-dev \
	gnuplot libreadline-dev libncurses-dev libxt-dev \
        qt4-dev-tools libqt4-dev libqt4-opengl-dev freeglut3-dev libqtwebkit-dev

WORKDIR /app
ENV OF_HOME="/app/OpenFOAM-v2006"
ENV OF_BASHRC="${OF_HOME}/etc/bashrc"

RUN wget https://sourceforge.net/projects/openfoam/files/v2006/OpenFOAM-v2006.tgz && \
    wget https://sourceforge.net/projects/openfoam/files/v2006/ThirdParty-v2006.tgz && \
    tar xvf OpenFOAM-v2006.tgz && tar xvf ThirdParty-v2006.tgz

RUN echo 'export FOAM_INST_DIR="/app/OpenFOAM-v2006" \nexport WM_MPLIB=USERMPI \nexport WM_COMPILER_TYPE=system \nexport WM_COMPILER=Gcc75* \nexport WM_LABEL_SIZE=64 \n' >> $OF_HOME/etc/prefs.sh 
WORKDIR $OF_HOME
SHELL ["/bin/bash", "-c"]
RUN source /app/OpenFOAM-v2006/etc/bashrc && wmake -j 8 all




    

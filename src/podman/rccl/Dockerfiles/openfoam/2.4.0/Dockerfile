FROM ubuntu:18.04
# General system updates

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc-5 g++-5 gfortran-5 curl make libnuma-dev libnl-3-200 autoconf vim python3.6
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 7 \
&&  update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 7  \
&&  update-alternatives --install /usr/bin/gfortran gfortran /usr/bin/gfortran-5 7 \
&&  update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2



WORKDIR /software
RUN curl -L https://www.mpich.org/static/downloads/3.3.2/mpich-3.3.2.tar.gz -o mpich-3.3.2.tar.gz \
&&  tar xvf mpich-3.3.2.tar.gz \
&&  cd /software/mpich-3.3.2 \
&&  ./configure --prefix=/software \
&&  make -j 8 VERBOSE=1 \
&&  make install
RUN rm -rf /software/mpich-3.3.2.tar.gz /software/mpich-3.3.2

ENV PATH=/software/bin:${PATH}
ENV LD_LIBRARY_PATH=/software/lib:${LD_LIBRARY_PATH}
RUN ldconfig


# Update OpenFOAM specific system libraries
RUN apt-get install -y \
    git flex bison cmake zlib1g-dev libboost-system-dev libboost-thread-dev libcgal-dev \
    gnuplot libreadline-dev libncurses-dev libxt-dev \
    qt4-dev-tools libqt4-dev libqt4-opengl-dev freeglut3-dev libqtwebkit-dev libglu1-mesa-dev \
    python python-dev wget 
    
    
RUN mkdir /app
ARG OFINSTDIR=/app/OpenFOAM
ARG OFVERSION=2.4.x
WORKDIR $OFINSTDIR

SHELL ["/bin/bash","-c"]
# get source
RUN git clone https://github.com/OpenFOAM/OpenFOAM-2.4.x.git \
&&  git clone https://github.com/OpenFOAM/ThirdParty-2.4.x.git

# definitions for the pref.sh and bashrc files. perf.sh, if exists, is sourced by bashrc

ARG OFPREFS=${OFINSTDIR}/OpenFOAM-${OFVERSION}/etc/prefs.sh
ARG OFBASHRC=${OFINSTDIR}/OpenFOAM-${OFVERSION}/etc/bashrc

RUN head -23 ${OFINSTDIR}/OpenFOAM-${OFVERSION}/etc/config/example/prefs.sh > $OFPREFS \
	&& echo '#---------------------------#' >> ${OFPREFS} \
        && echo 'WM_PROJECT_USER_DIR=/workdir/$WM_PROJECT/OpenFOAM-$WM_PROJECT_VERSION' \
	&& echo 'export WM_MPLIB=SYSTEMMPI' >> ${OFPREFS} \
	&& echo 'export MPI_ROOT="/software"' >> ${OFPREFS} \
	&& echo 'export MPI_ARCH_FLAGS="-DMPICH_SKIP_MPICXX"' >> ${OFPREFS} \
	&& echo 'export MPI_ARCH_INC="-I${MPI_ROOT}/include"' >> ${OFPREFS} \
	&& echo 'export MPI_ARCH_LIBS="-L${MPI_ROOT}/lib${WM_COMPILER_LIB_ARCH} -L${MPI_ROOT}/lib -lmpich -lrt"' >> ${OFPREFS} 
 
 # modify bashrc
 RUN 	sed -i '/^foamInstall=$HOME.*/afoamInstall='"${OFINSTDIR}" ${OFBASHRC} \
 	 && sed -i '0,/^foamInstall=$HOME/s//# foamInstall=$HOME/' ${OFBASHRC} \
	# && sed -i 's;export WM_PROJECT_USER_DIR=\$HOME/\$WM_PROJECT/\$USER-\$WM_PROJECT_VERSION;export WM_PROJECT_USER_DIR=/workdir/\$WM_PROJECT/ofuser-\$WM_PROJECT_VERSION;g' ${OFBASHRC} \ 
 	 && echo ''	
# Download paraview (taken from wiki instructions)
 RUN . ${OFBASHRC} \
	&& cd $WM_THIRD_PARTY_DIR \
	&& mkdir download \
	&& wget --no-check-certificate -P download http://www.paraview.org/files/v4.1/ParaView-v4.1.0-source.tar.gz \
	&& tar -xzf download/ParaView-v4.1.0-source.tar.gz \
	&& mv ParaView-v4.1.0 ParaView-4.1.0 \
	&& rm -rf download
 	
# Paraview compilation (Adapted alternative instructions from OpenFoamWiki)
 RUN . ${OFBASHRC} \
	 && cd $WM_THIRD_PARTY_DIR \
	 && export QT_SELECT=qt4 \
	 && sed -i -e 's=//#define GLX_GLXEXT_LEGACY=#define GLX_GLXEXT_LEGACY=' ParaView-4.1.0/VTK/Rendering/OpenGL/vtkXOpenGLRenderWindow.cxx \
	 && cd ParaView-4.1.0 \
	 && wget --no-check-certificate http://www.paraview.org/pipermail/paraview/attachments/20140210/464496cc/attachment.bin -O Fix.patch \
	 && patch -p1 < Fix.patch \
	 && cd VTK \
	 && wget --no-check-certificate https://github.com/gladk/VTK/commit/ef22d3d69421581b33bc0cd94b647da73b61ba96.patch -O Fix2.patch \
	 && patch -p1 < Fix2.patch \
	 && cd $WM_THIRD_PARTY_DIR \
	 && ./makeParaView4 -python -mpi -python-lib /usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0 2>&1 | tee log.makePV
	 
# Install Third Party tools
 RUN . ${OFBASHRC} \
	 && cd $WM_THIRD_PARTY_DIR \
	 && mkdir download \
	 && wget --no-check-certificate -P download https://gforge.inria.fr/frs/download.php/file/34099/scotch_6.0.3.tar.gz \
	 && tar -xzf download/scotch_6.0.3.tar.gz \
	 && rm -rf download

 ARG OFCGAL=${OFINSTDIR}/OpenFOAM-${OFVERSION}/etc/config/CGAL.sh
 RUN . ${OFBASHRC} \
	 && cp ${OFCGAL} ${OFCGAL}.original \
	 && sed -i '/^cgal_version=.*/acgal_version=cgal-system' ${OFCGAL} \
	 && sed -i '0,/^cgal_version/s//# cgal_version/' ${OFCGAL} \ 
	 && sed -i 's,export BOOST_ARCH_PATH,# export BOOST_ARCH_PATH,' ${OFCGAL} \
	 && sed -i 's,export CGAL_ARCH_PATH,# export CGAL_ARCH_PATH,' ${OFCGAL} \
	 && echo ''

 RUN . ${OFBASHRC} \
	&& cd $WM_THIRD_PARTY_DIR \
	&& ./Allwmake 2>&1 | tee log.Allwmake
	
# Fix for the flex version check 
 RUN . ${OFBASHRC} \
	&& cd $WM_PROJECT_DIR \
	&& find src applications -name "*.L" -type f -exec cp \{} \{}.original \; \
	&& find src applications -name "*.L" -type f | xargs sed -i -e \
	    's=\(YY\_FLEX\_SUBMINOR\_VERSION\)=YY_FLEX_MINOR_VERSION < 6 \&\& \1='

# OpenFOAM compilation 
 ENV WM_NCOMPPROCS=8
 RUN . ${OFBASHRC} \
	&& cd $WM_PROJECT_DIR \
	&& export QT_SELECT=qt4 \
	&& ./Allwmake 2>&1 | tee log.Allwmake

# Obtaining a summary
 RUN . ${OFBASHRC} \
	&& cd $WM_PROJECT_DIR \
	&& export QT_SELECT=qt4 \
	&& ./Allwmake 2>&1 | tee log.AllwmakeSummary

WORKDIR /workdir

ENV FOAM_TUTORIALS=/app/OpenFOAM/OpenFOAM-2.4.x/tutorials
ENV LD_LIBRARY_PATH=/app/OpenFOAM/ThirdParty-2.4.x/platforms/linux64Gcc/gperftools-svn/lib:/app/OpenFOAM/ThirdParty-2.4.x/platforms/linux64Gcc/ParaView-4.1.0/lib/paraview-4.1:/app/OpenFOAM/OpenFOAM-2.4.x/platforms/linux64GccDPOpt/lib/mpi-system:/app/OpenFOAM/ThirdParty-2.4.x/platforms/linux64GccDPOpt/lib/mpi-system:/workdir/OpenFOAM/OpenFOAM-2.4.x/platforms/linux64GccDPOpt/lib:/app/OpenFOAM/site/2.4.x/platforms/linux64GccDPOpt/lib:/app/OpenFOAM/OpenFOAM-2.4.x/platforms/linux64GccDPOpt/lib:/app/OpenFOAM/ThirdParty-2.4.x/platforms/linux64GccDPOpt/lib:/app/OpenFOAM/OpenFOAM-2.4.x/platforms/linux64GccDPOpt/lib/dummy:/software/lib
ENV MPI_BUFFER_SIZE=20000000
ENV WM_PROJECT_INST_DIR=/app/OpenFOAM
ENV FOAM_RUN=/workdir/OpenFOAM/OpenFOAM-2.4.x/run
ENV ParaView_MAJOR=4.1
ENV WM_THIRD_PARTY_DIR=/app/OpenFOAM/ThirdParty-2.4.x
ENV WM_LDFLAGS=-m64
ENV FOAM_APP=/app/OpenFOAM/OpenFOAM-2.4.x/applications
ENV WM_CXXFLAGS='-m64 -fPIC'
ENV FOAM_UTILITIES=/app/OpenFOAM/OpenFOAM-2.4.x/applications/utilities
ENV FOAM_APPBIN=/app/OpenFOAM/OpenFOAM-2.4.x/platforms/linux64GccDPOpt/bin
ENV ParaView_DIR=/app/OpenFOAM/ThirdParty-2.4.x/platforms/linux64Gcc/ParaView-4.1.0
ENV WM_PRECISION_OPTION=DP
ENV FOAM_SOLVERS=/app/OpenFOAM/OpenFOAM-2.4.x/applications/solvers
ENV FOAM_EXT_LIBBIN=/app/OpenFOAM/ThirdParty-2.4.x/platforms/linux64GccDPOpt/lib
ENV MPI_ARCH_LIBS='-L/software/lib -L/software/lib -lmpich -lrt'
ENV WM_CC=gcc
ENV FOAM_USER_APPBIN=/workdir/OpenFOAM/OpenFOAM-2.4.x/platforms/linux64GccDPOpt/bin
ENV FOAM_SIGFPE=
ENV WM_PROJECT_USER_DIR=/workdir/OpenFOAM/OpenFOAM-2.4.x
ENV WM_OPTIONS=linux64GccDPOpt
ENV WM_LINK_LANGUAGE=c++
ENV WM_OSTYPE=POSIX
ENV WM_PROJECT=OpenFOAM
ENV ParaView_INCLUDE_DIR=/app/OpenFOAM/ThirdParty-2.4.x/platforms/linux64Gcc/ParaView-4.1.0/include/paraview-4.1
ENV FOAM_LIBBIN=/app/OpenFOAM/OpenFOAM-2.4.x/platforms/linux64GccDPOpt/lib
ENV MPI_ARCH_PATH=/software
ENV WM_CFLAGS='-m64 -fPIC'
ENV MPI_ARCH_FLAGS=-DMPICH_SKIP_MPICXX
ENV WM_ARCH=linux64
ENV FOAM_SRC=/app/OpenFOAM/OpenFOAM-2.4.x/src
ENV FOAM_ETC=/app/OpenFOAM/OpenFOAM-2.4.x/etc
ENV FOAM_SETTINGS=
ENV FOAM_SITE_APPBIN=/app/OpenFOAM/site/2.4.x/platforms/linux64GccDPOpt/bin
ENV FOAM_SITE_LIBBIN=/app/OpenFOAM/site/2.4.x/platforms/linux64GccDPOpt/lib
ENV WM_COMPILER_LIB_ARCH=64
ENV WM_COMPILER=Gcc
ENV ParaView_VERSION=4.1.0
ENV WM_DIR=/app/OpenFOAM/OpenFOAM-2.4.x/wmake
ENV WM_ARCH_OPTION=64
ENV WM_PROJECT_VERSION=2.4.x
ENV WM_MPLIB=SYSTEMMPI
ENV FOAM_INST_DIR=/app/OpenFOAM
ENV WM_COMPILE_OPTION=Opt
ENV MPI_ARCH_INC=-I/software/include
ENV WM_CXX=g++
ENV FOAM_USER_LIBBIN=/workdir/OpenFOAM/OpenFOAM-2.4.x/platforms/linux64GccDPOpt/lib
ENV PV_PLUGIN_PATH=/app/OpenFOAM/OpenFOAM-2.4.x/platforms/linux64GccDPOpt/lib/paraview-4.1
ENV FOAM_MPI=mpi-system
ENV FOAM_JOB_DIR=/app/OpenFOAM/jobControl
ENV WM_PROJECT_DIR=/app/OpenFOAM/OpenFOAM-2.4.x
ENV PATH=/app/OpenFOAM/ThirdParty-2.4.x/platforms/linux64Gcc/gperftools-svn/bin:/app/OpenFOAM/ThirdParty-2.4.x/platforms/linux64Gcc/ParaView-4.1.0/bin:/workdir/OpenFOAM/OpenFOAM-2.4.x/platforms/linux64GccDPOpt/bin:/app/OpenFOAM/site/2.4.x/platforms/linux64GccDPOpt/bin:/app/OpenFOAM/OpenFOAM-2.4.x/platforms/linux64GccDPOpt/bin:/app/OpenFOAM/OpenFOAM-2.4.x/bin:/app/OpenFOAM/OpenFOAM-2.4.x/wmake:/software/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV MPI_ROOT=/software

#COPY en*.sh /software/
#RUN chmod +x /software/entrypoint.sh
#ENTRYPOINT ["/software/entrypoint.sh"]

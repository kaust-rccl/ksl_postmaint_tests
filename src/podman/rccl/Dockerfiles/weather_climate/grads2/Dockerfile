FROM centos:centos7.4.1708
RUN yum update -y && \
    yum install -y wget gcc gcc-c++ gcc-gfortran make libtool
RUN yum install -y curl-devel freetype-devel fontconfig-devel libtiff-devel compat-libtiff3 pixman-devel readline-devel.x86_64 libjpeg-turbo-devel.x86_64 cairo-devel
RUN rpm -Uvh https://download-ib01.fedoraproject.org/pub/epel/7/x86_64/Packages/p/proj-4.8.0-4.el7.x86_64.rpm && \
    rpm -Uvh https://download-ib01.fedoraproject.org/pub/epel/7/x86_64/Packages/l/libgeotiff-1.2.5-14.el7.x86_64.rpm && \
    rpm -Uvh https://download-ib01.fedoraproject.org/pub/epel/7/x86_64/Packages/l/libgeotiff-devel-1.2.5-14.el7.x86_64.rpm

ENV PATH="/usr/local/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/lib:/usr/lib64:${LD_LIBRARY_PATH}"
ENV PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:/usr/lib64/pkgconfig:${PKG_CONFIG_PATH}"
WORKDIR /software
RUN wget http://download.osgeo.org/shapelib/shapelib-1.5.0.tar.gz && \
    tar xvf shapelib-1.5.0.tar.gz && cd shapelib-1.5.0 && \
    ./autogen.sh && ./configure --prefix=/usr/local && make && make install
WORKDIR /software
RUN wget https://github.com/libgd/libgd/archive/refs/tags/gd-2.3.3.tar.gz && \
     tar xvf gd-2.3.3.tar.gz && \
    cd libgd-gd-2.3.3 && ./bootstrap.sh && ./configure --prefix=/usr/local && make && make install 
WORKDIR /software
RUN wget ftp://cola.gmu.edu/grads/Supplibs/2.2/src/hdf5-1.8.11.tar.gz && \
    tar xvf hdf5-1.8.11.tar.gz && \
    cd hdf5-1.8.11 && \
    yum install -y which && ./configure --prefix=/usr/local && make && make install
WORKDIR /software
RUN wget ftp://cola.gmu.edu/grads/Supplibs/2.2/src/netcdf-4.3.3.tar.gz && \
    tar xvf netcdf-4.3.3.tar.gz && \
    cd netcdf-4.3.3 && \
    yum install -y which && ./configure --prefix=/usr/local && make && make install
WORKDIR /software
RUN rm -rf *
RUN wget ftp://cola.gmu.edu/grads/2.2/grads-2.2.1-bin-centos7.4-x86_64.tar.gz && \
    tar xvf grads-2.2.1-bin-centos7.4-x86_64.tar.gz && rm grads-2.2.1-bin-centos7.4-x86_64.tar.gz
RUN yum install -y libSM
ENV PATH="/software/grads-2.2.1/bin:${PATH}"
ENV LD_LIBRARY_PATH="/software/grads-2.2.1/lib:${LD_LIBRARY_PATH}"


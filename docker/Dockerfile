# Copyright 2022 Balacoon

FROM python:3.8-slim

ARG build_pg

ENV DEBIAN_FRONTEND="noninteractive" TZ="Europe/Berlin"

# get ubuntu essentials to build packages
RUN apt-get update
RUN apt-get install -y openssh-client git vim autoconf automake libtool m4 gfortran autoconf-archive build-essential

RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

RUN echo "alias python=python3" > /root/.bash_aliases
RUN echo "export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH" >> /root/.bashrc
    
# download dependencies
RUN --mount=type=ssh cd /opt/ && \
    git clone -b 1.8.0 git@github.com:balacoon/openfst.git && \
    git clone git@github.com:balacoon/mitlm.git && \
    git clone git@github.com:balacoon/phonetisaurus.git

# build dependencies
# build and install OpenFST
RUN cd /opt/openfst && \
    ./configure --enable-python --enable-mpdt --enable-far --enable-pdt \
        --enable-shared --enable-ngram-fsts --enable-grm && \
    make -j $(nproc) && \
    make install

# build and install MITLM
RUN cd /opt/mitlm && \
    ./autogen.sh && \
    make -j $(nproc) && \
    make install

# build and install phonetisaurus
RUN cd /opt/phonetisaurus && \
    autoreconf && \
    automake && \
    ./configure && \
    make -j $(nproc) all && \
    make install

# install pronunciation_generation package,
# which utilizes pronunciation addons
RUN --mount=type=ssh if [ "$build_pg" = "true" ]; then \
    echo "Building pronunciation_generation from sources" && \
    cd /opt/ && \
    git clone git@github.com:balacoon/pronunciation_generation && \
    pip install ./pronunciation_generation ; \
else \
    echo "Installing pronunciation_generation from pip" && \
    pip install pronunciation_generation ; fi

# install package itself
COPY ./ /opt/learn_to_pronounce
RUN pip install /opt/learn_to_pronounce

WORKDIR /home/
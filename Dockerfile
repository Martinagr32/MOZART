# Base image
FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y build-essential cmake zlib1g-dev libcppunit-dev git subversion wget && rm -rf /var/lib/apt/lists/*
RUN wget https://www.openssl.org/source/openssl-1.1.1d.tar.gz -O - | tar -xz
WORKDIR /openssl-1.1.1d
RUN ./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl && make && make install
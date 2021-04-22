# Base image
FROM ubuntu:16.04

RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get purge firefox
RUN apt-cache showpkg firefox
RUN apt-get install -y build-essential cmake zlib1g-dev libcppunit-dev git subversion wget && rm -rf /var/lib/apt/lists/*
RUN wget https://ftp.mozilla.org/pub/firefox/releases/45.0/linux-x86_64/en-US/firefox-45.0.tar.bz2
RUN tar -xjf firefox-45.0.tar.bz2
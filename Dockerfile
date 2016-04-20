FROM ubuntu:latest

RUN echo Y | sudo apt-get install software-properties-common
RUN sudo dpkg --add-architecture i386
RUN sudo add-apt-repository -y ppa:ubuntu-wine

RUN apt-get -y update && apt-get install -y python
RUN apt-get -y install wget
RUN apt-get install -y python-pip && apt-get install -y python-setuptools && apt-get install -y python-dev && apt-get install -y build-essential && echo y | apt-get install python-dialog 
RUN echo y | pip install requests && echo y | pip install termcolor && echo y | pip install pycrypto
RUN mkdir /tmp/CLI/

COPY CLI/ /tmp/CLI/

RUN chmod +x /tmp/CLI/SteamGameInstaller/steamcmd_setup.sh
RUN /tmp/CLI/SteamGameInstaller/steamcmd_setup.sh
CMD python ./tmp/CLI/steam_connect_cli.py

FROM base/archlinux

MAINTAINER Victor Santos <victor.ssouza@hotmail.com.br>

ENV TERM=xterm-256color
ENV LANG=en_US.UTF-8

RUN set -x \
&& pacman -Syy \
&& pacman -S --noconfirm python-pip \
&& pacman -S --noconfirm openssl \
&& pacman -S --noconfirm git \
&& pacman -S --noconfirm gcc \
&& pacman -S --noconfirm dialog \
&& pacman -S --noconfirm ncurses \
&& ln -s /usr/lib/libncursesw.so.6  /usr/lib/libncursesw.so.5

RUN cd /opt \
&& git clone https://bitbucket.org/chimeraos/steamconnectcli.git \
&& pip3 install -r /opt/steamconnectcli/requirements.txt \
&& ln -s /opt/steamconnectcli/CLI/steam_connect_cli.py /usr/local/bin/scli \
&& cd - \
&& clear

ENTRYPOINT python /usr/local/bin/scli

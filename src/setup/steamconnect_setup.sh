#!/bin/bash
# Description: Setup which will allow arch linux distro for executing our games

function validating_distro(){
    if [[ $(cat /etc/issue) == 'Arch Linux \r (\l)' ]]; then
        echo "[INFO] Setting up pre-requisites for Arch Linux"
    else
        echo "[ERROR]: Distro not supported"
        exit 1
    fi
}

function setup_packages(){
    set -x \
    && pacman -Syy \
    && pacman -S --noconfirm python-pip \
    && pacman -S --noconfirm openssl \
    && pacman -S --noconfirm git \
    && pacman -S --noconfirm gcc \
    && pacman -S --noconfirm dialog \
    && pacman -S --noconfirm ncurses \
    && pacman -S --noconfirm wget \
    && pacman -S --noconfirm vim \
    && pacman -S --noconfirm net-tools \
    && ln -s /usr/lib/libncursesw.so.6  /usr/lib/libncursesw.so.5

    # Uncomment multilib for installing wine
    sed -i '92,93 s/#//' /etc/pacman.conf
    pacman -Syy && pacman -S --noconfirm wine-staging winetricks wine_gecko wine-mono \
        lib32-libpulse lib32-alsa-plugins lib32-mpg123 lib32-sdl

    # Installing our app
    cd /opt \
    && git clone https://bitbucket.org/chimeraos/steamconnectcli.git \
    && pip3 install -r /opt/steamconnectcli/requirements.txt \
    && ln -s /opt/steamconnectcli/CLI/steam_connect_cli.py /usr/local/bin/scli \
    && cd -
}

function setup_steamcmd(){
    mkdir ~/steamcmd
    cd ~/steamcmd
    wget https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz
    tar -xvzf steamcmd_linux.tar.gz
    rm steamcmd_linux.tar.gz

    # Be sure to run after 'setup_packages'
    pacman -S --noconfirm lib32-gcc-libs
}

function setup_steam_app(){
    cd /tmp
    wget https://steamcdn-a.akamaihd.net/client/installer/SteamSetup.exe
    wine SteamSetup.exe /S

    #We have to disable 'dwrite' library for text renderer purposes
    wine reg add 'HKCU\Software\Valve\Steam' /v DWriteEnable /t REG_DWORD /d 00000000
    #creating an alias to just "steam-wine" on terminal :3
    alias steam-wine='WINEDEBUG=-all wine ~/.wine/drive_c/Program\ Files\ \(x86\)/Steam/Steam.exe >/dev/null 2>&1 &'
    wine ~/.wine/drive_c/"Program Files (x86)"/Steam/Steam.exe -no-dwrite 2>&1 &

    #We have to remove the desktop symbolic link and create a new one due Steam issues
    rm ~/Desktop/Steam.desktop

    # Executing for the first time SteamCMD
    chmod +x ~/steamcmd/steamcmd.sh
    ~/steamcmd/steamcmd.sh
}

function run(){
    validating_distro
    setup_packages
    setup_steam_app
    setup_steamcmd
}

run

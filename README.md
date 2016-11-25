## **What is it?**

This repo contains a python’s library and CLI to connect with your steam’s account and very shortly downloading your steam games with it!

## **How far is it?**

This app is still under development and can contain several bugs! :(  

## **Requirements**
* Python 3
* pip3 requirements
* Arch Linux

## **Getting started**
0) [Optional]: Create a virtual environment for Python3 if you are just testing the app, no need to mess with your own system  
1) Install python’s modules as a requirement using the following syntax:  
`pip3 install -r requirements.txt`

** Testing with CLI **  
2) `python3 CLI/steam_connect_cli.py`

## **How safe is it?**

This app will not persist your password in any circunstances, but you have to be aware that the future requests made will be based on a local cookie, which will work only in your machine. :]

## **Support for Docker**

If you do not want to mess with your own environment even with a virtual one, you can test the application
using our docker image (800MB ~).  

1. Build a docker image for SteamConnect CLI  
`docker build --force-rm --no-cache -t scli_arch_base .`  


2. Just run it! :D  
`docker run -it --hostname chimera-os-scli --name chimera-os-scli scli_arch_base`

## **Contribution**

Wanna help? Fork our project and create a merge request with your suggestion in a new branch. We will see it (:

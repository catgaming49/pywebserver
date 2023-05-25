#!/bin/sh
echo starting
mkdir /etc/py-http-serv
cp ./mypyton-server /etc/systemd/system
cp ../* /etc/py-http-serv
#!/bin/sh

service_path=/etc/systemd/system

server_files_path=/etc/py-http-serv

mkdir $server_files_path && cp -r ../* $server_files_path
echo Created dir at $server_files_path and copied files. Status code = $?

cp ./my-python-server.service $service_path
echo created service at $service_path. Status code = $?

systemctl daemon-reload
echo reloaded daemons. Status code = $?

echo Installed!
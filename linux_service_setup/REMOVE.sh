#!/bin/sh

service_path=/etc/systemd/system

server_files_path=/etc/py-http-serv

rm -r $server_files_path
echo Removed $server_files_path. Status code = $?

rm $service_path/my-python-server.service
echo removed service at $service_path/my-python-server.service. Status code = $?

systemctl daemon-reload
echo reloaded daemons. Status code = $?

echo Uninstalled
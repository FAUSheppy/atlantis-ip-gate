#!/bin/bash

while true; do
    sleep 1
    inotifywait -e close_write /data/blockmap.conf
    nginx -s reload
done

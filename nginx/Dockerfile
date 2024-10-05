FROM alpine:latest

# install nginx
RUN apk update
RUN apk upgrade
RUN apk add nginx

# copy config #
COPY nginx.conf /etc/nginx/
RUN mkdir /data/

# install inotifywatch & copy script #
RUN apk add inotify-tools
RUN apk add bash
COPY wait_for_map_change.sh /wait_for_map_change.sh
RUN chmod +x /wait_for_map_change.sh
RUN ls -l /wait_for_map_change.sh

# run inotify scrip & nginx #
CMD echo "Waiting for 3s.."; sleep 3; nohup /wait_for_map_change.sh & nginx && sleep 100000d

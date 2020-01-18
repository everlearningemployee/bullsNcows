#!/bin/bash
BOT=bullsncows_bot
IMG=bullsncows
cd /home/ubuntu/bullsNcows
git pull
sudo docker build --tag $IMG:${1:-"latest"} .
docker stop $BOT
docker rm $BOT
sudo docker run -d --name=$BOT $IMG

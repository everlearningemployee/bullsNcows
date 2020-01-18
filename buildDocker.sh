#!/bin/bash
sudo docker build --tag bullsncows:${1:-"latest"} .

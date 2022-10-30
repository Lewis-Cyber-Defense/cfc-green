#!/bin/bash
docker rm -f websolar
docker build --tag=websolar .
docker run -p 80:80 --rm --name=websolar websolar
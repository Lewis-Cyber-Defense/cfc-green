#!/bin/bash
docker rm -f websolar
docker build --tag=websolar .
docker run -p 1337:1337 --rm --name=websolar websolar
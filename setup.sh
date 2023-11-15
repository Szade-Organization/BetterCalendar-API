#!/bin/bash

# Colors
RED='\033[0;31m'
COLOR_OFF='\033[0m'
GREEN='\033[0;32m'

if [ "$1" == "--help" ]; then
    echo "Usage: ./setup.sh"
    echo "This script will build and run the docker container for the better-calendar-api."
    echo "You must have docker and docker buildx installed for this script to work."
    echo "You must have a .env file in the same directory as this script"
    echo "The .env file must contain a SECRET_KEY variable"
    echo ".env file should look like this:"
    echo "cat .env"
    echo "SECRET_KEY=your_secret_key"
    exit 0
fi

if [ ! -f .env ]; then
    echo -e "${RED}ERROR:"
    echo -e ".env file not found!${COLOR_OFF}"
    if [ -f env ]; then
        echo "env file found - did you forget to rename it to .env?"
    fi
    exit 1
fi
if SECRET_KEY=`cat .env | grep SECRET_KEY | cut -b 12-` ; then
    :
else
    echo -e "${RED}ERROR:"
    echo -e "SECRET_KEY not found in .env file${COLOR_OFF}"
    exit 1
fi

if docker buildx build -t better-calendar-api . ; then
    :
else
    echo -e "${RED}Docker build failed!${COLOR_OFF}"
    exit 1
fi
if docker run -itd -e SECRET_KEY=$SECRET_KEY -p 8000:8000 --name better-calendar-api better-calendar-api ; then
    :
else
    echo -e "${RED}Docker run failed!${COLOR_OFF}"
    if  docker ps -a | grep -q better-calendar-api  ; then
        echo "Container already exists! If you want to reinstall, run 'docker stop better-calendar-api && docker rm better-calendar-api' and then rerun this script"
    fi
    exit 1
fi
if docker start better-calendar-api ; then
    echo 
    echo -e "${GREEN}better-calendar-api installed and started successfully!${COLOR_OFF}"
    echo
    echo "To operate the container use:"
    echo "To stop the container, run 'docker stop better-calendar-api'"
    echo "To start the container, run 'docker start better-calendar-api'"
    echo "To restart the container, run 'docker restart better-calendar-api'"
    echo "To view the logs, run 'docker logs better-calendar-api'"
    echo 'To uninstall the container, run "docker stop better-calendar-api && docker rm better-calendar-api"'
else
    echo -e "${RED}Docker start failed!${COLOR_OFF}"
    exit 1
fi
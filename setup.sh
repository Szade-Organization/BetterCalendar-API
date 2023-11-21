#!/bin/bash

RED='\033[0;31m'
COLOR_OFF='\033[0m'
GREEN='\033[0;32m'

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
if BC_DB_CONNECTION_STRING=`cat .env | grep BC_DB_CONNECTION_STRING | cut -b 25-` ; then
    :
else
    echo -e "${RED}ERROR:"
    echo -e "BC_DB_CONNECTION_STRING not found in .env file${COLOR_OFF}"
    exit 1
fi

if docker pull ghcr.io/szade-organization/bettercalendar-api:latest ; then
    :
else
    echo -e "${RED}ERROR:"
    echo -e "Docker pull failed!${COLOR_OFF}"
    echo "Have you logged in to the GitHub Container Registry?"
    echo "Run 'docker login ghcr.io' to log in."
    exit 1
fi

docker rm better-calendar-api

if docker run -itd -e SECRET_KEY=$SECRET_KEY -e BC_DB_CONNECTION_STRING=$BC_DB_CONNECTION_STRING -p 8000:8000 --name better-calendar-api ghcr.io/szade-organization/bettercalendar-api ; then
    :
else
    echo -e "${RED}Docker run failed!${COLOR_OFF}"
    exit 1
fi
sleep 2
if curl -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/api/info ; then
    :
else
    echo -e "${RED}Docker start succeeded, but the API has not responded correctly!${COLOR_OFF}"
    echo "Check the logs with 'docker logs better-calendar-api'"
    echo "Test the API with 'curl -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/api/info'"
    exit 1
fi
echo
docker logs better-calendar-api
echo 
echo -e "${GREEN}better-calendar-api installed and started successfully!${COLOR_OFF}"
echo
echo "To operate the container use:"
echo "To stop the container, run 'docker stop better-calendar-api'"
echo "To start the container, run 'docker start better-calendar-api'"
echo "To restart the container, run 'docker restart better-calendar-api'"
echo "To view the logs, run 'docker logs better-calendar-api'"
echo 'To uninstall the container, run "docker stop better-calendar-api && docker rm better-calendar-api"'
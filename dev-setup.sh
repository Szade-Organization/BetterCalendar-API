#!/bin/bash

RED='\033[0;31m'
COLOR_OFF='\033[0m'
GREEN='\033[0;32m'

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


export SECRET_KEY=$SECRET_KEY
export BC_DB_CONNECTION_STRING=$BC_DB_CONNECTION_STRING
echo "SECRET_KEY and BC_DB_CONNECTION_STRING exported successfully"

if docker ps | grep better-calendar-db ; then
    echo "better-calendar-db container is already running."
else
    if docker run -itd -p 27017:27017 -e "MONGO_INITDB_ROOT_USERNAME=user" -e "MONGO_INITDB_ROOT_PASSWORD=password" --name better-calendar-db ghcr.io/szade-organization/bettercalendar-database:latest ; then
        echo "better-calendar-db container started successfully"
    else
        echo -e "${RED}ERROR:"
        echo -e "better-calendar-db container start failed!${COLOR_OFF}"
        exit 1
    fi
fi

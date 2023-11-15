#!/bin/bash

RED='\033[0;31m'
COLOR_OFF='\033[0m'
GREEN='\033[0;32m'

POSITIONAL_ARGS=()
REBUILD=false
HELP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--rebuild)
            REBUILD=true
            shift
            ;;
        -h|--help)
            HELP=true
            shift
            ;;
        -*|--*)
            echo -e "${RED}ERROR:"
            echo -e "Unknown option $1${COLOR_OFF}"
            exit 1
            ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

set -- "${POSITIONAL_ARGS[@]}"

if [ "$HELP" = true ] ; then
    echo "Usage: ./setup.sh"
    echo "This script will build and run the docker container for the better-calendar-api."
    echo "You must have docker and docker buildx installed for this script to work."
    echo "You must have a .env file in the same directory as this script."
    echo "The .env file must contain a SECRET_KEY variable."
    echo ".env file should look like this:"
    echo "cat .env"
    echo "SECRET_KEY=your_secret_key"
    echo "Options:"
    echo "-r/--rebuild: stops and removes the docker image before rubuilding it again. Doesn't check if the containers actually exists,"
    echo "-h/--help: display this help message,"
    echo "To test the API, run 'curl -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/api/info'"
    echo "To operate the container use:"
    echo "To stop the container, run 'docker stop better-calendar-api'"
    echo "To start the container, run 'docker start better-calendar-api'"
    echo "To restart the container, run 'docker restart better-calendar-api'"
    echo "To view the logs, run 'docker logs better-calendar-api'"
    echo 'To uninstall the container, run "docker stop better-calendar-api && docker rm better-calendar-api"'
    
    exit 0
fi

if [ "$REBUILD" = true ] ; then
    docker stop better-calendar-api
    docker rm better-calendar-api
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

if [ "$REBUILD"  = false ] && docker ps -a | grep -q better-calendar-api  ; then
    echo -e "${RED}ERROR:"
    echo -e "Container already exists! If you want to reinstall, run this script with the -r/--rebuild option${COLOR_OFF}"
    exit 1
fi

if  docker buildx build -t better-calendar-api . ; then
    :
else
    echo -e "${RED}Docker build failed!${COLOR_OFF}"
    exit 1
fi
if docker run -itd -e SECRET_KEY=$SECRET_KEY -p 8000:8000 --name better-calendar-api better-calendar-api ; then
    :
else
    echo -e "${RED}Docker run failed!${COLOR_OFF}"
    if docker ps -a | grep -q better-calendar-api  ; then
        echo "Container already exists! If you want to reinstall, run this script with the -r/--rebuild option"
    fi
    exit 1
fi
if docker start better-calendar-api ; then
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
else
    echo -e "${RED}Docker start failed!${COLOR_OFF}"
    exit 1
fi
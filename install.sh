#!/bin/bash

echo '   _____            __        __  _______ __      ____             __    __                         __
  / ___/____  _____/ /_____  / /_/ ____(_) /_    / __ \____ ______/ /_  / /_  ____  ____ __________/ /
  \__ \/ __ \/ ___/ //_/ _ \/ __/ /_  / / __/   / / / / __ `/ ___/ __ \/ __ \/ __ \/ __ `/ ___/ __  / 
 ___/ / /_/ / /__/ ,< /  __/ /_/ __/ / / /_    / /_/ / /_/ (__  ) / / / /_/ / /_/ / /_/ / /  / /_/ /  
/____/\____/\___/_/|_|\___/\__/_/   /_/\__/   /_____/\__,_/____/_/ /_/_.___/\____/\__,_/_/   \__,_/   '

echo "Welcome to the SocketFit Dashboard installation script!" 

if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "SocketFit Dashboard installation script only supports GNU/Linux, exiting."
    exit
fi

if  [[! -v docker &> /dev/null ]]; then
    echo "Docker is not installed, exiting."
    exit
fi

if [[ -e ".env" ]]; then
    echo ".env already exists, exiting."
    exit
fi

declare -A env

HOST="database"
MYSQL_USER="socketfit"
MYSQL_PASSWORD=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 12)
MYSQL_ROOT_PASSWORD=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 12)
MYSQL_DATABASE="socketfit"
MYSQL_PORT=3306
STORAGE_SECRET=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 20)

PS3='Please enter your choice: '
options=("Normal Installation" "Advanced Installation" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Normal Installation")
            touch .testenv
            echo "Creating .env file"
            echo "HOST="${HOST} >> .env
            echo "MYSQL_USER="${MYSQL_USER} >> .env
            echo "MYSQL_PASSWORD="${MYSQL_PASSWORD} >> .env
            echo "MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD} >> .env
            echo "MYSQL_DATABASE="${MYSQL_DATABASE} >> .env
            echo "MYSQL_PORT="${MYSQL_PORT} >> .env
            echo "STORAGE_SECRET="${STORAGE_SECRET} >> .env
            echo ".env successfully created."
            echo "Creating Dockerfile image"
            sudo docker build -t socketfit .
            echo "Dockerfile image successfully created!"
            echo "Run the application with sudo docker compose up"
            break
            ;;
        "Manual Installation")
            echo "you chose choice 2"
            break
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done
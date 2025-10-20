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

declare -A env

HOST="database"
MYSQL_USER="socketfit"
MYSQL_PASSWORD=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 12)
MYSQL_ROOT_PASSWORD=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 12)
MYSQL_DATABASE="database"
MYSQL_PORT=3306
STORAGE_SECRET=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 20)

echo "${RANDOM_STRING}"

PS3='Please enter your choice: '
options=("Normal Installation" "Advanced Installation" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Normal Installation")
            echo "you chose choice 1"
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
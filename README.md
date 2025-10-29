# SocketFit Dashboard
![Socketfit Dashboard Logo.](/src/assets/dashboard.png "Socketfit Dashboard Logo.")

The SocketFit Dashboard is a clinician dashboard designed to help assist clinicians in viewing patient's prosthesis data in a user friendly way.
This dashboard is designed to link with the SocketFit mobile application, and can be updated in future for this capability.

## Installation
Simply run the installation script and follow the instructions.
```
./install.sh
```
After installation, you can simply run 
``` 
sudo docker compose up 
```
or use Docker Desktop to run the containers.

You can also just build the docker image yourself, just make sure to set the .env accordingly (see below)
```
sudo docker build -t sockerfit .
```

Alternatively, you can host it locally:
```
sudo apt update && sudo apt upgrade
sudo apt install mysql-server python3 python3-pip python3-venv
sudo mysql -u root
CREATE DATABASE socketfit;
// Note, you can create a user here opposed to altering root.
ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'password';
// If you made a new user, make sure to give them appropriate permissions
GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost';
FLUSH PRIVILEGES;
use socketfit;
SOURCE /src/sql/create.sql;
SOURCE /src/sql/populate.sql;
exit
python3 -m venv .venv
source .venv/bin/activate
pip install -r ./requirements.txt
python3 ./src/main.py
```
This process is for Ubuntu, but you follow the logical steps for each operating system: Install MySQL and Python3.12, fill out the database with the test data, and run the ./src/main.py file in a virtual environment after installing dependencies.
Please note if you host it locally you need to create a .env file and fill it out with the details you used in setup, for example:
(Note, if you're using docker, the MYSQL_HOST should be database)
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_ROOT_PASSWORD=password
MYSQL_DATABASE=socketfit
MYSQL_PORT=3306
STORAGE_SECRET=somerandomsecret
```

## Design
This web application is built off of NiceGUI and FastAPI. We utilize FastAPI for our endpoints and token handling, and all our webpages are made in NiceGUI. Additionally, the installation script builds a Dockerfile and runs a docker compose with MySQL and the Dockerfile.

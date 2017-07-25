#!/bin/bash
    
# Perform all necessary steps to setup grader: 
# 0. Clones repo from github
# 1. Installs requirements - system and pip 
# 2. Builds docker image
# 3. Does sanity checks
# 4. Sets up django project:
#   4.1. Runs migrations
#   4.2. Creates superuser
#   4.3. Creates API user
#   4.4. Puts them in test client settings file
#   4.5. Provisions the initial data
#   4.6. Runs Django and celery
#   4.7. Runs tests

# if ssh setup
git clone git@github.com:HackSoftware/HackGrader.git ~/HackGrader
 
# Docker 17.06.0-ce
version=`uname -mrs`
if [[ $version == *"ARCH"* ]]; then
    sudo pacman -S docker
else 
    sudo apt-get update
    sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
    sudo apt-get update
    sudo apt-get install docker-ce
fi

# docker permissions
sudo groupadd docker
sudo usermod -aG docker $USER

sudo systemctl stop docker
sudo systemctl start docker

if [[ $version == *"ARCH"* ]]; then
    sudo pacman -S rabbitmq
else
    sudo apt-get install rabbitmq-server
fi

sudo rabbitmq-server &

cd ~/HackGrader/hacktester/docker
docker build -t grader .

docker run grader /bin/bash --login -c "python3.5 --version"
docker run grader /bin/bash --login -c "ruby --version"
docker run grader /bin/bash --login -c "java -version"

cd ../../
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements/local.txt

sudo systemctl start postgresql

# requires postgres installed and setup
if [[ -z `psql -l | grep hacktester` ]]; then
    sudo -u postgres createdb hacktester
else
    sudo -u postgres dropdb hacktester 
    sudo -u postgres createdb hacktester
fi

python manage.py migrate

python manage.py createsuperuser

python manage.py create_api_user localhost:8000 >> api_keys
key=`cat api_keys | grep Key | awk -F": " '{print $2}'`
secret=`cat api_keys | grep Secret | awk -F": " '{print $2}'`

python manage.py provision_initial_data

cd ~/code/grader_e2e 
echo GRADER_API_KEY = "\"$key\"" >> grader_e2e/settings/local.py 
echo GRADER_SECRET_KEY = "\"$secret\"" >> grader_e2e/settings/local.py 
echo {} >> nonce.json

cd ~/HackGrader
python manage.py runserver &
celery -A hacktester worker -B -E --loglevel=info &

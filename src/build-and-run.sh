#!/usr/bin/env sh

name=`cat shodan/bot/.env | grep DB_NAME | cut -d '=' -f2`
user=`cat shodan/bot/.env | grep DB_USER | cut -d '=' -f2`
password=`cat shodan/bot/.env | grep DB_PASS | cut -d '=' -f2`

[ -z $name ] && echo 'DB name required' && exit 1
[ -z $user ] && echo 'DB user required' && exit 1
[ -z $password ] && echo 'DB password required' && exit 1

cp -n docker-compose.yml docker-compose.yml.bak

sed -i "s/<DB_NAME_HERE>/$name/g" docker-compose.yml
sed -i "s/<DB_USER_HERE>/$user/g" docker-compose.yml
sed -i "s/<DB_PASSWORD_HERE>/$password/g" docker-compose.yml
sed -i "s/<DB_ROOT_PASSWORD_HERE>/`./shodan/pwgen.sh`/g" docker-compose.yml

docker-compose up --build

#!/usr/bin/env sh

SHODAN_DIR='./shodan/bot'
CHECKPOINT_DIR='./checkpoint-bot/app'

shodan_name=`cat $SHODAN_DIR/.env | grep DB_NAME | cut -d '=' -f2`
shodan_user=`cat $SHODAN_DIR/.env | grep DB_USER | cut -d '=' -f2`
shodan_password=`cat $SHODAN_DIR/.env | grep DB_PASS | cut -d '=' -f2`

checkpoint_name=`cat $CHECKPOINT_DIR/.env | grep DB_NAME | cut -d '=' -f2`
checkpoint_user=`cat $CHECKPOINT_DIR/.env | grep DB_USER | cut -d '=' -f2`
checkpoint_password=`cat $CHECKPOINT_DIR/.env | grep DB_PASS | cut -d '=' -f2`

[ -z $shodan_name ] && echo 'DB name required' && exit 1
[ -z $shodan_user ] && echo 'DB user required' && exit 1
[ -z $shodan_password ] && echo 'DB password required' && exit 1

[ -z $checkpoint_name ] && echo 'DB name required' && exit 1
[ -z $checkpoint_user ] && echo 'DB user required' && exit 1
[ -z $checkpoint_password ] && echo 'DB password required' && exit 1

cp -n docker-compose.yml docker-compose.yml.bak

sed -i "s/<DB_NAME_HERE>/$shodan_name/g" docker-compose.yml
sed -i "s/<DB_USER_HERE>/$shodan_user/g" docker-compose.yml
sed -i "s/<DB_PASSWORD_HERE>/$shodan_password/g" docker-compose.yml

sed -i "s/<CHECKPOINT_BOT_DB_NAME_HERE>/$checkpoint_name/g" docker-compose.yml
sed -i "s/<CHECKPOINT_BOT_DB_USER_HERE>/$checkpoint_user/g" docker-compose.yml
sed -i "s/<CHECKPOINT_BOT_DB_PASSWORD_HERE>/$checkpoint_password/g" docker-compose.yml

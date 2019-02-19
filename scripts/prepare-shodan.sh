#!/usr/bin/env sh

# Do NOT run from this directory
# Use /prepare.sh

SHODAN_DIR='shodan/bot'
SHORT_OPTIONS='ghv'
LONG_OPTIONS='generate,help,verbose'

USAGE="USAGE: $0 -ghv
Arguments:
\t-h               Print this
\t-g --generate    Generate new .env file
\t-v --verbose     Adds nothing (for now that is)"

usage() {
	echo "$USAGE"
	exit 0
}

getopt --test
status=$?
if [ $status -ne 4 ]; then
	echo 'WARNING: getopt is not working. No argument is parsed'
else
	PARSED_OPTIONS=`getopt -o $SHORT_OPTIONS -l $LONG_OPTIONS -n "$0" -- "$@"`
	status=$?
	[ $status -ne 0 ] && usage
	eval set -- "$PARSED_OPTIONS"
fi

verbose=0
if [ -n "$PARSED_OPTIONS" ]; then
	while true; do
		case "$1" in
			-h|--help)
				usage
				;;
			-g|--generate) # generate .env file for shodan
				env_path="$SHODAN_DIR/.env"

				# options to specify if you want to generate a .env file
				# WARNING: this will overwrite the existing .env file
				DB_NAME="shodan"
				DB_HOST="shodan_db"
				DB_USER="shodan_bot"
				DB_PASS="`sh scripts/pwgen.sh`"

				echo 'DB_NAME='$DB_NAME > $env_path
				echo 'DB_HOST='$DB_HOST >> $env_path
				echo 'DB_USER='$DB_USER >> $env_path
				echo 'DB_PASS='$DB_PASS >> $env_path
				shift
				;;
			-v|--verbose)
				verbose=1
				shift
				;;
			--)
				shift
				break
				;;
			*)
				echo "Code shouldn't be here"
				exit 1
				;;
		esac
	done
fi

# parse .env file
shodan_name=`cat $SHODAN_DIR/.env | grep DB_NAME | cut -d '=' -f2`
shodan_user=`cat $SHODAN_DIR/.env | grep DB_USER | cut -d '=' -f2`
shodan_password=`cat $SHODAN_DIR/.env | grep DB_PASS | cut -d '=' -f2`

# .env file validation
[ -z $shodan_name ] && echo 'DB name required' && exit 1
[ -z $shodan_user ] && echo 'DB user required' && exit 1
[ -z $shodan_password ] && echo 'DB password required' && exit 1

# replacement
sed -i "s/<SHODAN_DB_NAME_HERE>/$shodan_name/g" docker-compose.yml
sed -i "s/<SHODAN_DB_USER_HERE>/$shodan_user/g" docker-compose.yml
sed -i "s/<SHODAN_DB_PASSWORD_HERE>/$shodan_password/g" docker-compose.yml

echo "Remember to add Shodan API_KEY to $SHODAN_DIR/.env"

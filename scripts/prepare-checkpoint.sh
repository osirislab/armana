#!/usr/bin/env sh

# Do NOT run from this directory
# Use /prepare.sh

CHECKPOINT_DIR='checkpoint/app'
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
			-g|--generate) # generate .env file for checkpoint
				env_path="$CHECKPOINT_DIR/.env"

				# options to specify if you want to generate a .env file
				# WARNING: this will overwrite the existing .env file
				DB_NAME="checkpoint"
				DB_HOST="checkpoint_db"
				DB_USER="checkpoint_bot"
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
				echo "You shouldn't be here"
				exit 1
				;;
		esac
	done
fi

# parse .env file
checkpoint_name=`cat $CHECKPOINT_DIR/.env | grep DB_NAME | cut -d '=' -f2`
checkpoint_user=`cat $CHECKPOINT_DIR/.env | grep DB_USER | cut -d '=' -f2`
checkpoint_password=`cat $CHECKPOINT_DIR/.env | grep DB_PASS | cut -d '=' -f2`

# .env file validation
[ -z $checkpoint_name ] && echo 'DB name required' && exit 1
[ -z $checkpoint_user ] && echo 'DB user required' && exit 1
[ -z $checkpoint_password ] && echo 'DB password required' && exit 1

# replacement
sed -i "s/<CHECKPOINT_DB_NAME_HERE>/$checkpoint_name/g" docker-compose.yml
sed -i "s/<CHECKPOINT_DB_USER_HERE>/$checkpoint_user/g" docker-compose.yml
sed -i "s/<CHECKPOINT_DB_PASSWORD_HERE>/$checkpoint_password/g" docker-compose.yml

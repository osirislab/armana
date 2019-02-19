#!/usr/bin/env sh

# either nothing or -g
GENERATE_ENV_CHECKPOINT='-g'
GENERATE_ENV_SHODAN='-g'

# options
SHORT_OPTIONS='scfha'
LONG_OPTIONS='shodan,checkpoint,fortiguard,help,all'

usage() {
	echo "USAGE: $0 -$SHORT_OPTIONS"
	echo "Arguments:"
	echo "\t-h                  Print this"
	echo "\t-a --all            Prepare for launching all services"
	echo "\t                    Do not use with the rest"
	echo "\t-s --shodan         Prepare for launching Shodan"
	echo "\t-c --checkpoint     Prepare for launching Check Point bot"
	echo "\t-f --fortiguard     Do nothing (for now that is)"
	echo "Examples:"
	echo "\tprepare.sh --all    # Prepare everything"
	echo "\tprepare.sh -s -c    # Prepare checkpoint and shodan bot"
	echo "\tprepare.sh --shodan # Prepare shodan bot"
	exit 0
}

[ -z $1 ] && usage

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

# back up just because
cp -n docker-compose.yml docker-compose.yml.bak

conflict=0
if [ -n "$PARSED_OPTIONS" ]; then
	while true; do
		case "$1" in
			-h|--help)
				usage
				;;
			-a|--all)
				if [ $conflict -eq 0 ]; then
					sh scripts/prepare-shodan.sh $GENERATE_ENV_SHODAN
					sh scripts/prepare-checkpoint.sh $GENERATE_ENV_CHECKPOINT
					break
				fi
				shift
				;;
			-c|--checkpoint)
				sh scripts/prepare-checkpoint.sh $GENERATE_ENV_CHECKPOINT
				conflict=1
				shift
				;;
			-s|--shodan)
				sh scripts/prepare-shodan.sh $GENERATE_ENV_SHODAN
				conflict=1
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


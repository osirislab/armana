#!/usr/bin/env sh

# options
SHORT_OPTIONS='schag'
LONG_OPTIONS='shodan,checkpoint,help,all,generate-env'

USAGE="USAGE: $0 -$SHORT_OPTIONS
Arguments:
\t-h                  Print this
\t-a --all            Prepare for launching all services
\t                    Do not use with the rest
\t-s --shodan         Prepare for launching Shodan
\t-c --checkpoint     Prepare for launching Check Point bot
\t-g --generate-env   Generate .env files
\t                    WANRING: This will overwrite existing .env files
Examples:
\tprepare.sh --all    # Prepare everything
\tprepare.sh -s -c    # Prepare checkpoint and shodan bot
\tprepare.sh --shodan # Prepare shodan bot"

usage() {
	echo "$USAGE"
	exit 0
}

[ -z $1 ] && usage

getopt --test
status=$?
if [ $status -ne 4 ]; then
	echo 'ERROR: getopt is not working. No argument is parsed'
else
	PARSED_OPTIONS=`getopt -o $SHORT_OPTIONS -l $LONG_OPTIONS -n "$0" -- "$@"`
	status=$?
	[ $status -ne 0 ] && usage
	eval set -- "$PARSED_OPTIONS"
fi

if [ -n "$PARSED_OPTIONS" ]; then
	run_shodan=0
	run_checkpoint=0
	generate_env_shodan=''
	generate_env_checkpoint=''

	while true; do
		case "$1" in
			-h|--help)
				usage
				;;
			-g|--generate-env)
				echo 'Environmental variables generated'
				generate_env_checkpoint='-g'
				generate_env_shodan='-g'
				shift
				;;
			-a|--all)
				run_shodan=1
				run_checkpoint=1
				shift
				;;
			-c|--checkpoint)
				run_checkpoint=1
				shift
				;;
			-s|--shodan)
				run_shodan=1
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

	[ $run_shodan -eq 0 ] && [ $run_checkpoint -eq 0 ] && \
		echo 'No service started' && exit 1

	# back up just because
	cp -n docker-compose.yml docker-compose.yml.bak

	[ $run_shodan -eq 1 ] && \
		sh scripts/prepare-shodan.sh $generate_env_shodan
	[ $run_checkpoint -eq 1 ] && \
		sh scripts/prepare-checkpoint.sh $generate_env_checkpoint

else
	echo 'ERROR: Arguments not parsed'
fi

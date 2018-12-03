from python:3-alpine
maintainer Liyun Li <liyun@nyu.edu>

env SHODAN_DIR /shodan

run mkdir -p $SHODAN_DIR

copy ./r.txt /tmp
copy ./streamer.py $SHODAN_DIR
run pip install -r /tmp/r.txt

workdir $SHODAN_DIR
cmd python streamer.py

from python:3-alpine
maintainer Liyun Li <liyun@nyu.edu>

run apk add postgresql-dev alpine-sdk

run mkdir -p /shodan

copy ./r.txt /tmp
run pip install -r /tmp/r.txt

workdir /shodan

from python:3-alpine
maintainer Liyun Li <liyun@nyu.edu>

run apk add postgresql-dev alpine-sdk

run mkdir -p /bot

copy ./r.txt /tmp
run pip install -r /tmp/r.txt

workdir /bot

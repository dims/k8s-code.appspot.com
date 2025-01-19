#!/bin/sh

cd /root/go/src/github.com/dims/k8s-code.appspot.com/codesearch.k8s.io/
cp config.json config.json.bak
git reset --hard HEAD
git pull origin master
cp config.json.bak config.json
python3 fetch-repos.py > config.json.tmp && cp config.json.tmp config.json

ps -ef | grep -e hound -e git | grep -v grep | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1

nohup bash -c '\
  ulimit -f unlimited && \
  ulimit -t unlimited && \
  ulimit -v unlimited && \
  ulimit -n 64000 && \
  ulimit -m unlimited && \
  ulimit -u 64000 && \
  ulimit -l unlimited && \
  /root/go/bin/houndd -conf /root/go/src/github.com/dims/k8s-code.appspot.com/codesearch.k8s.io/config.json -addr "0.0.0.0:8080"' 2>&1 > k8s-code.log &

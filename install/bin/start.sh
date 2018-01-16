#!/usr/bin/env bash
#####################
# version: 0.1
# name: xuebk
# time: 2017-01-09
# help: 启动noah
#####################
# 程序执行目录
BIN_DIR=$(cd "$(dirname "$0")"; pwd)
# 部署路径
DEPLOY_DIR=$(cd "$(dirname "$0")";cd ..;cd ..; pwd)
source ~/.bash_profile && workon DevOps_ProjectAdmin
PYTHON=`which python`

PIDS=`ps aux |grep $DEPLOY_DIR/manage.py |grep -v grep |awk '{print $2}'`
if [ -n "$PIDS" ]; then
    echo "ERROR: The manage.py already started!"
    echo "PID: $PIDS"
    exit 1
fi

nohup $PYTHON $DEPLOY_DIR/manage.py runserver 0.0.0.0:8000 &
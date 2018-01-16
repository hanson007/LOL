#!/usr/bin/env bash
#####################
# version: 0.1
# name: xuebk
# time: 2017-01-09
# help: 更新 noah 版本
#####################
# 程序执行目录
BIN_DIR=$(cd "$(dirname "$0")"; pwd)
# 部署路径
DEPLOY_DIR=$(cd "$(dirname "$0")";cd ..;cd ..; pwd)
ps aux |grep $DEPLOY_DIR/manage.py |grep -v grep |awk '{print $2}'|xargs kill -9
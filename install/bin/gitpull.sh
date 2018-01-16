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
echo "BIN_DIR:${BIN_DIR} DEPLOY_DIR:${DEPLOY_DIR}"
cd $DEPLOY_DIR
git pull
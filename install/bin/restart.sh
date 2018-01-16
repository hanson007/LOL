#!/usr/bin/env bash
#####################
# version: 0.1
# name: xuebk
# time: 2017-01-11
# help: 重启 noah 客户端
#####################
# 程序执行目录
BIN_DIR=$(cd "$(dirname "$0")"; pwd)
# 部署路径
DEPLOY_DIR=$(cd "$(dirname "$0")";cd ..;cd ..; pwd)
cd $DEPLOY_DIR

/bin/bash ${DEPLOY_DIR}/install/bin/stop.sh
/bin/bash ${DEPLOY_DIR}/install/bin/start.sh
#!/usr/bin/env bash
#####################
# version: 0.1
# name: xuebk
# time: 2017-01-09
# help: 更新 noah 版本
#####################
# 程序执行目录
source ~/env/DevOps_ProjectAdmin/bin/activate
BIN_DIR=$(cd "$(dirname "$0")"; pwd)
# 部署路径
DEPLOY_DIR=$(cd "$(dirname "$0")";cd ..;cd ..; pwd)
DATE=`date +%F` # 类似 2017-08-08
echo "[INFO][${DATE}] BIN_DIR:${BIN_DIR} "
echo "[INFO][${DATE}] DEPLOY_DIR:${DEPLOY_DIR}"
pip freeze > ${DEPLOY_DIR}/install/requirement/commd.txt 2>/dev/null
echo "[INFO][${DATE}] 完成 pip_freeze"
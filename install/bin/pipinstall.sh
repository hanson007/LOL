#!/usr/bin/env bash
# version: 0.1
# name: xuebk
# time: 2017-02-08
# help: 安装 pip 插件后.并进行保存.
#####################
# 程序执行目录
BIN_DIR=$(cd "$(dirname "$0")"; pwd)
# 部署路径
DEPLOY_DIR=$(cd "$(dirname "$0")"; cd ../..; pwd)
# requirements file
ReqFile="${DEPLOY_DIR}/install/requirements/comm.txt"
echo "BIN_DIR:${BIN_DIR} \nDEPLOY_DIR:${DEPLOY_DIR}"
echo "args:'$*'"
# 运行 传入全部内容
pip install $*
# 判断是否运行成功.成功执行
JG=$?
[ ${JG} != 0 ]&& exit ${JG}
# 写入正常内容
pip freeze |sed 's#==#>=#g' > ${ReqFile}

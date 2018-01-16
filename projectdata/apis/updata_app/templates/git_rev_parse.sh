#!/usr/bin/env bash
#####################
# version: 0.1
# name: xuebk
# time: 2017-05-30
# help: 系统更新程序.
#####################
# 加载系统层变量
source ~/.bash_profile
# 基础变量
cd `dirname $0`
# 本程序执行目录
BIN_DIR=$(cd "$(dirname "$0")"; pwd)
# #### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# 基础
function CheckUser(){
    # 检测当前用户是否 为tomcat 用户.
    check_user=`whoami`
    if [ "$check_user" != "tomcat" ]
    then
        echo "You are '$check_user' is not tomcat" | tee -a ${STDOUT_FILE}
        exit 2
    fi
}
# #### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
CheckUser
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
Name="{{ App }}"
BIN_DIR="{{ data.BIN_DIR }}"
CODE_DIR="{{ data.CODE_DIR }}"
Bin_Start="{{ data.Bin_Start }}"
Bin_Stop="{{ data.Bin_Stop }}"
Bin_Config="{{ data.Bin_Config }}"
giturl="{{ data.giturl }}"
commitid="{{ commit_id }}"
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
source /home/tomcat/.bash_profile && cd ${BIN_DIR} && ${Bin_Stop}
source /home/tomcat/.bash_profile && [ -d '${BIN_DIR}/${CODE_DIR}/' ] && rm -rf ${BIN_DIR}/${CODE_DIR}/*
source /home/tomcat/.bash_profile && [[  -d '${BIN_DIR}/.git-${Name}'  ]] && mv ${BIN_DIR}/.git-${Name} ${BIN_DIR}/${CODE_DIR}/.git
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
source /home/tomcat/.bash_profile && mkdir -p ${BIN_DIR}/${CODE_DIR}/
source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git rev-parse --is-inside-work-tree # timeout=10
source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git init ${BIN_DIR}/${CODE_DIR} # timeout=10
source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git --version # timeout=10
source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git fetch --tags --progress ${giturl} +refs/heads/*:refs/remotes/origin/*
source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git config remote.origin.url ${giturl} # timeout=10
source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git config --add remote.origin.fetch +refs/heads/*:refs/remotes/origin/* # timeout=10
source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git config remote.origin.url ${giturl} # timeout=10
source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git fetch --tags --progress ${giturl} +refs/heads/*:refs/remotes/origin/*
source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git rev-parse ${commitid} # timeout=10
source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git config core.sparsecheckout # timeout=10
source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git checkout -f ${commitid}
source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git rev-list ${commitid} # timeout=10
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
source /home/tomcat/.bash_profile && [[  -d '${BIN_DIR}/${CODE_DIR}/.git'  ]] && mv ${BIN_DIR}/${CODE_DIR}/.git ${BIN_DIR}/.git-${Name}
source /home/tomcat/.bash_profile && cd ${BIN_DIR} && ${Bin_Config} 1>/dev/null
source /home/tomcat/.bash_profile && cd ${BIN_DIR} && ${Bin_Start}
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
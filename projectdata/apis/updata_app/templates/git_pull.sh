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
{% if data.Bin_Config %}
Bin_Config="{{ data.Bin_Config }}"
{% else %}
Bin_Config="echo ok"
{% endif %}
giturl="{{ data.giturl }}"
commitid="{{ commit_id }}"
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
echo "source /home/tomcat/.bash_profile && cd ${BIN_DIR} && ${Bin_Stop}"
# source /home/tomcat/.bash_profile && cd ${BIN_DIR} && ${Bin_Stop}
echo "source /home/tomcat/.bash_profile && [ -d '${BIN_DIR}/${CODE_DIR}/' ] && rm -rf ${BIN_DIR}/${CODE_DIR}/*"
# source /home/tomcat/.bash_profile && [ -d '${BIN_DIR}/${CODE_DIR}/' ] && rm -rf ${BIN_DIR}/${CODE_DIR}/*
echo "source /home/tomcat/.bash_profile && [[  -d '${BIN_DIR}/.git-${Name}'  ]] && mv ${BIN_DIR}/.git-${Name} ${BIN_DIR}/${CODE_DIR}/.git"
# source /home/tomcat/.bash_profile && [[  -d '${BIN_DIR}/.git-${Name}'  ]] && mv ${BIN_DIR}/.git-${Name} ${BIN_DIR}/${CODE_DIR}/.git
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
echo "source /home/tomcat/.bash_profile && mkdir -p ${BIN_DIR}/${CODE_DIR}/"
# source /home/tomcat/.bash_profile && mkdir -p ${BIN_DIR}/${CODE_DIR}/
echo "source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git checkout master 1>/dev/null"
# source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git checkout master 1>/dev/null
echo "source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git checkout ./.  1>/dev/null"
# source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git checkout ./.  1>/dev/null
echo "source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git pull origin master"
# source /home/tomcat/.bash_profile && cd ${BIN_DIR}/${CODE_DIR}/ && git pull origin master
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
echo "source /home/tomcat/.bash_profile && [[  -d '${BIN_DIR}/${CODE_DIR}/.git'  ]] && mv ${BIN_DIR}/${CODE_DIR}/.git ${BIN_DIR}/.git-${Name}"
# source /home/tomcat/.bash_profile && [[  -d '${BIN_DIR}/${CODE_DIR}/.git'  ]] && mv ${BIN_DIR}/${CODE_DIR}/.git ${BIN_DIR}/.git-${Name}
echo "source /home/tomcat/.bash_profile && cd ${BIN_DIR} && ${Bin_Config} 1>/dev/null"
# source /home/tomcat/.bash_profile && cd ${BIN_DIR} && ${Bin_Config} 1>/dev/null
echo "source /home/tomcat/.bash_profile && cd ${BIN_DIR} && ${Bin_Start}"
# source /home/tomcat/.bash_profile && cd ${BIN_DIR} && ${Bin_Start}
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
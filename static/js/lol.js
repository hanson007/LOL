/**
 * Created by Hanson on 2017/9/23.
 */
/*$(document).ready(function(){
  // 在这里写你的代码...
    init_font();
    init_account();
    init_script();
});*/

var shell_tmp = function () {/*
#!/bin/bash

anynowtime="date +'%Y-%m-%d %H:%M:%S'"
NOW="echo [\`$anynowtime\`][PID:$$]"

#####可在脚本开始运行时调用，打印当时的时间戳及PID。
function job_start
{
    echo "`eval $NOW` job_start"
}

#####可在脚本执行成功的逻辑分支处调用，打印当时的时间戳及PID。
function job_success
{
    MSG="$*"
    echo "`eval $NOW` job_success:[$MSG]"
    exit 0
}

#####可在脚本执行失败的逻辑分支处调用，打印当时的时间戳及PID。
function job_fail
{
    MSG="$*"
    echo "`eval $NOW` job_fail:[$MSG]"
    exit 1
}

job_start

######可在此处开始编写您的脚本逻辑代码
######作业平台中执行脚本成功和失败的标准只取决于脚本最后一条执行语句的返回值
######如果返回值为0，则认为此脚本执行成功，如果非0，则认为脚本执行失败

*/};

var python_tmp = function () {/*
#!/usr/bin/env python
# -*- coding: utf8 -*-

import datetime
import os
import sys

def _now(format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(format)

#####可在脚本开始运行时调用，打印当时的时间戳及PID。
def job_start():
    print "[%s][PID:%s] job_start" % (_now(), os.getpid())

#####可在脚本执行成功的逻辑分支处调用，打印当时的时间戳及PID。
def job_success(msg):
    print "[%s][PID:%s] job_success:[%s]" % (_now(), os.getpid(), msg)
    sys.exit(0)

#####可在脚本执行失败的逻辑分支处调用，打印当时的时间戳及PID。
def job_fail(msg):
    print "[%s][PID:%s] job_fail:[%s]" % (_now(), os.getpid(), msg)
    sys.exit(1)

if __name__ == '__main__':

    job_start()

######可在此处开始编写您的脚本逻辑代码
######iJobs中执行脚本成功和失败的标准只取决于脚本最后一条执行语句的返回值
######如果返回值为0，则认为此脚本执行成功，如果非0，则认为脚本执行失败

*/};

//定义一个实现多行字符串的函数multiline
var multiline = function (fn) {
    var str = fn.toString().split('\n');
    return str.slice(1, str.length - 1 ).join('\n');
};




/**
 * init editor
 */
function init_editor() {
    // create first editor
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/sh");
    editor.renderer.setScrollMargin(10, 10);
    editor.setOptions({
        // "scrollPastEnd": 0.8,
        autoScrollEditorIntoView: true
    });
    //设置字体
    document.getElementById('editor').style.fontSize='18px';
    //语法补全
    editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true
    });
    //默认shell
    editor.setValue(multiline(shell_tmp));
    editor.gotoLine(1);
}



/*
*初始化字体选择项
*/
function init_font() {
    for (var i=12;i<23;i++)
    {
        var cont = "<option value='"+ i +"'>"+ i +"</option>";
        $('#font').append(cont);
    }
    $('#font').val('18');
}
$('#font').change(function () {
    var font_val = $(this).val() + 'px';
    document.getElementById('editor').style.fontSize=font_val;
    console.log($(this).val())
});


/*
*初始化账户
*/
function init_account() {
    var url = '/business/get_account/';
    var index = layer.load();
    $.post(url, function (data) {
        var _data = $.parseJSON(data);
        var cont0 = "<option value=''>请选择</option>";
        $('#account').append(cont0);
        $.each(_data, function (k,v) {
            var cont = "<option value='"+ v.name +"'>"+ v.name + " " + v.desc +"</option>";
            $('#account').append(cont);
        });
        $("#account").chosen();
        layer.close(index);
    });
}


/*
*脚本类型、模板选择
*/
$("input:radio[name='script_type']").click(function () {
    var _type = $(this).val();
    if (_type=='1'){
        editor.setValue(multiline(shell_tmp));
        editor.session.setMode("ace/mode/sh");
    }
   else {
        editor.setValue(multiline(python_tmp));
        editor.session.setMode("ace/mode/python");
    }
    editor.gotoLine(1);
});


/**
 *初始化脚本
 */
function init_script() {
    var url = '/business/get_script/';
    var index = layer.load();
    $.post(url, function (data) {
        var _data = $.parseJSON(data);
        var cont0 = "<option value=''>请选择</option>";
        $('#script').append(cont0);
        $.each(_data, function (k,v) {
            var cont = "<option value='"+ v.id +"'>"+ v.name + "</option>";
            $('#script').append(cont);
        });
        $("#script").chosen();
        layer.close(index);
    });
}


/**
 *设置按esc键全屏切换
 */
function set_editor_fullscreen() {
　　　$(window).keyup(function(e){
　  　　if(e.keyCode==27){//此处代表按的是键盘的Esc键
            var dom = require("ace/lib/dom");
            var fullScreen = dom.toggleCssClass(document.body, "fullScreen");
            dom.setCssClass(editor.container, "fullScreen", fullScreen);
            editor.setAutoScrollEditorIntoView(!fullScreen);
            editor.resize()
　　　　}
　　　});
}
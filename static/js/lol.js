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
function init_editor(selectorById) {
    // create first editor
    var editor = ace.edit(selectorById);
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/sh");
    editor.renderer.setScrollMargin(10, 10);
    editor.setOptions({
        // "scrollPastEnd": 0.8,
        autoScrollEditorIntoView: true
    });
    //设置字体
    document.getElementById(selectorById).style.fontSize='18px';
    //语法补全
    editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true
    });
    //默认shell
    editor.setValue(multiline(shell_tmp));
    editor.gotoLine(1);
    return editor
}



/*
*初始化字体选择项
*/
function init_font($selector) {
    for (var i=12;i<23;i++)
    {
        var cont = "<option value='"+ i +"'>"+ i +"</option>";
        $selector.append(cont);
    }
    $selector.val('18');
}


/**
 * 修改编辑器字体
 */
$("select[name='font']").change(function () {
    var font_val = $(this).val() + 'px';
    var editorId =$(this).siblings('pre').attr('id');
    document.getElementById(editorId).style.fontSize=font_val;
});



/*
*初始化账户
*/
function init_account($selector) {
    var url = '/business/get_account/';
    var index = layer.load();
    $.post(url, function (data) {
        var _data = $.parseJSON(data);
        var cont0 = "<option value=''>请选择</option>";
        $selector.append(cont0);
        $.each(_data, function (k,v) {
            var cont = "<option value='"+ v.name +"'>"+ v.name + " " + v.desc +"</option>";
            $selector.append(cont);
        });
        $selector.chosen();
        layer.close(index);
    });
}


/**
 * 脚本类型选择
 */
function ModifyScriptType(editor, $script_type) {
    $script_type.click(function () {
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
}



/**
 * 初始化脚本选项
 */
function init_script($selector) {
    var url = '/business/get_script/';
    var index = layer.load();
    $.post(url, function (data) {
        var _data = $.parseJSON(data);
        var cont0 = "<option value=''>请选择</option>";
        $selector.append(cont0);
        $.each(_data, function (k,v) {
            var cont = "<option value='"+ v.id +"'>"+ v.name + "</option>";
            $selector.append(cont);
        });
        $selector.chosen();
        layer.close(index);
    });
}


/**
 * 设置按esc键退出全屏
 */
function editorFullscreen(editor) {
    $(window).keyup(function(e){
        if(e.keyCode==27){//此处代表按的是键盘的Esc键
            $('body').toggleClass('fullScreen');
            $(editor.container).removeClass('fullScreen');
            editor.resize();
　　　　}
    });
}


/**
 * 全屏
 */
$("button[name='fullScreen']").click(function () {
    $('body').toggleClass('fullScreen');
    $(this).siblings('pre').addClass('fullScreen');
});


/**
 * 节点展开、收缩显示
 */
$('body').on('click', "label[for='scriptLabel']", function() {
    var siblings = $(this).siblings();/*清空缩略脚本参数、缩略账号*/
    var scriptParamSpan = siblings.eq(1).children();
    var accountSpan = siblings.eq(2).children();
    var parentSib = $(this).parent().siblings();
    if(parentSib.eq(0).is(':hidden')){
        /*展开节点时清空缩略脚本参数、缩略账号*/
        accountSpan.text('');
        scriptParamSpan.text('');
    }
    else{
        /*在隐藏节点时将参数、账号赋值到缩略脚本参数、缩略账号*/
        var scriptParam = parentSib.eq(3).find('input').val();
        var account = parentSib.eq(0).find('select').val();
        scriptParamSpan.eq(0).text('参数：');
        scriptParamSpan.eq(1).text(scriptParam);
        accountSpan.eq(0).text('账户：');
        accountSpan.eq(1).text(account);
    }

    $.each(parentSib, function (k, div) {
        $(div).slideToggle();
    });
});


/**
 * init all editor
 */
function initAllEditor() {
    $("pre").each(function () {
        var editorId = $(this).attr('id');
        var editor = init_editor(editorId);
        var $script_type = $(this).siblings().find("input[name='script_type']");
        ModifyScriptType(editor, $script_type);
        editorFullscreen(editor);
        console.log($(this).attr('id'))
    })
}
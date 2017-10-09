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


/**
 * 初始化字体选择项
 */
function initFont($selector) {
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
$('body').on('click', "select[name='font']", function () {
    var font_val = $(this).val() + 'px';
    var editorId =$(this).siblings('pre').attr('id');
    document.getElementById(editorId).style.fontSize=font_val;
});


/**
 * 初始化账户
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
function exitFullscreen(editor) {
    $(window).keyup(function(e){
        if(e.keyCode==27){//此处代表按的是键盘的Esc键
            var dom = require("ace/lib/dom");
            var fullScreen = dom.removeCssClass(document.body, "fullScreen");
            dom.setCssClass(editor.container, "fullScreen", fullScreen);
            editor.setAutoScrollEditorIntoView(!fullScreen);
            editor.resize()
　　　　}
    });
}


/**
 * 全屏
 */
function fullScreen(editor, $fullScreen) {
    $fullScreen.click(function () {
        var dom = require("ace/lib/dom");
        var fullScreen = dom.toggleCssClass(document.body, "fullScreen");
        dom.setCssClass(editor.container, "fullScreen", fullScreen);
        editor.setAutoScrollEditorIntoView(!fullScreen);
        editor.resize()
    });
}


/**
 * 脚本节点展开、收缩显示
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
 * 文件节点展开、收缩显示
 */
$('body').on('click', "label[for='fileLabel']", function() {
    var siblings = $(this).siblings();/*清空缩略脚本参数、缩略账号*/
    var fileTargetPath = siblings.eq(1).children();
    var accountSpan = siblings.eq(2).children();
    var parentSib = $(this).parent().siblings();
    if(parentSib.eq(0).is(':hidden')){
        /*展开节点时清空缩略脚本参数、缩略账号*/
        accountSpan.text('');
        fileTargetPath.text('');
    }
    else{
        /*在隐藏节点时将参数、账号赋值到缩略脚本参数、缩略账号*/
        var targetPathParam = parentSib.eq(1).find('input').val();
        var account = parentSib.eq(2).find('select').val();
        fileTargetPath.eq(0).text('目标路径：');
        fileTargetPath.eq(1).text(targetPathParam);
        accountSpan.eq(0).text('账户：');
        accountSpan.eq(1).text(account);
    }
    $.each(parentSib, function (k, div) {
        $(div).slideToggle();
    });
});


/**
 * add file blockOrd
 */
function addFileBlockOrd() {
    $('#addFileBlockOrd').click(function () {
        var $addBlock = $(this).parents(".panel-default");
        $addBlock.before($('#fileBlockOrdTemplate').html());
        /*设置步骤的data-name属性*/
        var count = $addBlock.prevAll().length;
        $addBlock.prev().find("form[data-type='pushFile']").attr('data-name', 'blockOrd' + count);
        $addBlock.prev().find("form[data-type='pushFile']").after($('#fileOrdTemplate').html());
        init_account($addBlock.prev().find("select[name='account']"));
        initTableSelected($addBlock.prev().find("table[data-name='table_selected']"));
        initFileTableSelected($addBlock.prev().find("table[data-name='table_selected_file']"));
        addFileOrd();
        // console.log($addBlock.prev().find("select[name='account']"));
    })
}


/**
 * add script blockOrd
 */
function addScriptBlockOrd() {
    $('#addScriptBlockOrd').click(function () {
        $(this).parents(".panel-default").before($('#scriptBlockOrdTemplate').html());
    })
}


/**
 * init editor all action
 */
function initEditorAction($pre) {
    $pre.each(function () {
        var editorId = $(this).attr('id');
        var editor = init_editor(editorId);
        var $script_type = $(this).siblings().find("input[name='script_type']");
        var $fullScreen = $(this).siblings("button[name='fullScreen']");
        ModifyScriptType(editor, $script_type);
        fullScreen(editor, $fullScreen);
        exitFullscreen(editor);
        console.log($(this).attr('id'))
    })
}


/**
 * 初始化服务器已选表格
 */
function initTableSelected($table_selected) {
    $table_selected.bootstrapTable({
        pagination: true,                   //是否显示分页（*）
        sortable: false,                     //是否启用排序
        sortOrder: "asc",                   //排序方式
        showColumns: true,
        showRefresh: true,
        clickToSelect: true,
        uniqueId: "id",
        sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
        pageNumber: 1,                       //初始化加载第一页，默认第一页
        pageSize: 5,                       //每页的记录行数（*）
        pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
        search: true,                  //是否显示搜索 --前端搜索
        columns: serverColumns()
    });
}



/**
 * 初始化服务器选择表格
 */
function init_server_choice() {
    $('#table_choice').bootstrapTable({
        url: '/cmdb/get_index/',
        pagination: true,                   //是否显示分页（*）
        sortable: false,                     //是否启用排序
        sortOrder: "asc",                   //排序方式
        showColumns: true,
        showRefresh: true,
        clickToSelect: true,
        uniqueId: "id",
        sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
        pageNumber: 1,                       //初始化加载第一页，默认第一页
        pageSize: 10,                       //每页的记录行数（*）
        pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
        search: true,                  //是否显示搜索 --前端搜索
        columns: serverColumns()
    });
}


/**
 * 新增服务器
 */
$('body').on('click', "button[data-name='add_server']", function () {
        var $table_selected = $(this).siblings().find("table[data-name='table_selected']");
        init_server_choice();
         $('#table_choice_div').removeClass('hide');
        //页面层
        layer.open({
            type: 1,
            skin: 'layui-layer-rim', //加上边框
            area: ['820px', '540px'], //宽高
            content: $('#table_choice_div')
            ,btn: ['add', 'close']
            ,yes: function(index1, layero){
                addServer($table_selected); //新增
                layer.close(index1);
            }
            ,btn2: function(index, layero){
            //return false 开启该代码可禁止点击该按钮关闭
            }
            ,cancel: function(){
            //右上角关闭回调
            }
        });
});



/**
 * 添加服务器到已选表格里
 */
function addServer($table_selected) {
    var choice_data = $('#table_choice').bootstrapTable('getSelections');
    var selected_data = $table_selected.bootstrapTable('getData');
    var selected_id = [];
    $.each(selected_data, function (sk, selected_v) {
        selected_id.push(selected_v.id);
    });
    $.each(choice_data, function (k, choice_v) {
        if (selected_id.indexOf(choice_v.id) == -1){
            $table_selected.bootstrapTable('append', choice_v);
        }
    });
}


/**
 * 删除已选服务器
 */
$('body').on('click', "button[data-name='delete']", function () {
    var $table_selected = $(this).siblings().find("table[data-name='table_selected']");
    var data = $table_selected.bootstrapTable('getSelections');
    $.each(data, function (sk, v) {
        $table_selected.bootstrapTable('removeByUniqueId', v.id);
    });
});


/**
 * 获取服务器表格的列columns
 */
function serverColumns() {
    var columns =[{
         field: 'checkbox',
         checkbox: true
    },{
        title: '序号',//标题  可不加
        formatter: function (value, row, index) {
            return index+1;
            }
    }, {
        field: 'id',
        title: 'ID',
        visible: false
    }, {
        field: 'ip',
        title: '服务器IP地址'
    }, {
        field: 'desc',
        title: '描述'
    }, {
        field: 'creater',
        title: '创建人'
    }, {
        field: 'createTime',
        title: '创建时间'
    }, {
        field: 'ModifyUser',
        title: '修改人'
    }, {
        field: 'ModifyTime',
        title: '修改时间'
    }];
    return columns
}


/**
 * 上传文件
 */
$('body').on('change', "input[data-name='file']", function () {
    var files = $(this)[0].files;
    var $tableSelectedFile = $(this).siblings().find("table[data-name='table_selected_file']");
    console.log($tableSelectedFile)
    add_table_file(files, $tableSelectedFile);
    $.each(files, function (k, file) {
        upload_file(file, $tableSelectedFile);
    });
});


/**
 * 上传文件到salt master服务器
 */
function upload_file(file, $tableSelectedFile) {
    var formData = new FormData();
    formData.append('file', file);
    var index = layer.load();
	$.ajax({
			url: '/job/fastPushfile_upload_file/',
			type: 'POST',
			cache: false,
			data: formData,
			processData: false,
			contentType: false,
            xhr: function(){
                myXhr = $.ajaxSettings.xhr();
                if(myXhr.upload){
                  myXhr.upload.addEventListener('progress',function(e) {
                    if (e.lengthComputable) {
                        var percent = Math.floor(e.loaded/e.total*100);
                        var progress = percent + '%';
                        var data = $tableSelectedFile.bootstrapTable('getData');
                        $.each(data, function (k, v) {
                            if (v.name == file.name){
                                $tableSelectedFile.bootstrapTable('updateCell', {index: k, field: 'progress', value: percent});
                                $tableSelectedFile.bootstrapTable('updateCell', {index: k, field: 'percent', value: percent});
                            }
                        });
                    }
                  }, false);
                }
                return myXhr;
            },
            success: function (res) {
                layer.close(index);
                var data = $tableSelectedFile.bootstrapTable('getData');
                    resfile = $.parseJSON(res);
                    console.log(resfile)
                ajax_callback1('上传成功')
            }
		})
}


/**
 * 将需要上传的文件添加到文件表格
 */
function add_table_file(files, $tableSelectedFile) {
    var selected_data = $tableSelectedFile.bootstrapTable('getData');
    var selected_id = [];
    $.each(selected_data, function (sk, selected_v) {
        selected_id.push(selected_v.name);
    });
    $.each(files, function (k, file) {
        var data = {'name': file.name, 'size': file.size, 'lastModified': file.lastModified,
                    'progress': 0, 'percent': 0, 'id': k};
        if (selected_id.indexOf(file.name) == -1){
            $tableSelectedFile.bootstrapTable('append', data);
        }
    });
}


/**
 * 删除文件
 */
$('body').on('click', "button[data-name='delete_file']", function () {
    var $tableSelectedFile = $(this).siblings().find("table[data-name='table_selected_file']");
    var names = $.map($tableSelectedFile.bootstrapTable('getSelections'), function (row) {
        return row.name;
    });
    $tableSelectedFile.bootstrapTable('remove', {
        field: 'name',
        values: names
    });
});


/**
 * 初始化文件表格
 */
function initFileTableSelected($table_selected_file) {
    $table_selected_file.bootstrapTable({
        pagination: true,                   //是否显示分页（*）
        sortable: false,                     //是否启用排序
        sortOrder: "asc",                   //排序方式
        showColumns: true,
        showRefresh: true,
        clickToSelect: true,
        uniqueId: "id",
        sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
        pageNumber: 1,                       //初始化加载第一页，默认第一页
        pageSize: 5,                       //每页的记录行数（*）
        pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
        search: true,                  //是否显示搜索 --前端搜索
        columns:get_file_columns()
    });
}



/**
 * 获取文件表格 的列columns
 */
function get_file_columns() {
    var columns =[{
         field: 'checkbox',
         checkbox: true
    },{
        title: '序号',//标题  可不加
        formatter: function (value, row, index) {
            return index+1;
            }
    }, {
        field: 'id',
        title: 'id',
        visible: false
    }, {
        field: 'name',
        title: 'name'
    }, {
        field: 'size',
        title: 'size',
        formatter: sizeFormatter
    }, {
        field: 'lastModified',
        title: 'lastModified',
        formatter: lastModifieldFormatter
    }, {
        field: 'progress',
        title: 'Progress',
        formatter: ProgressFormatter
    }, {
        field: 'percent',
        title: '',
        formatter: percentFormatter
    }];
    return columns
}

/**
 * 格式化文件大小
 */
function sizeFormatter(limit){
    var size = "";
    if( limit < 0.1 * 1024 ){ //如果小于0.1KB转化成B
        size = limit.toFixed(2) + "B";
    }else if(limit < 0.1 * 1024 * 1024 ){//如果小于0.1MB转化成KB
        size = (limit / 1024).toFixed(2) + "KB";
    }else if(limit < 0.1 * 1024 * 1024 * 1024){ //如果小于0.1GB转化成MB
        size = (limit / (1024 * 1024)).toFixed(2) + "MB";
    }else{ //其他转化成GB
        size = (limit / (1024 * 1024 * 1024)).toFixed(2) + "GB";
    }

    var sizestr = size + "";
    var len = sizestr.indexOf("\.");
    var dec = sizestr.substr(len + 1, 2);
    if(dec == "00"){//当小数点后为00时 去掉小数部分
        return sizestr.substring(0,len) + sizestr.substr(len + 3,2);
    }
    return sizestr;
}


/**
 * 格式化文件修改时间
 */
function lastModifieldFormatter(value, row, index) {
    return timetrans(value);
}


/**
 * 时间转换
 */
function timetrans(date){
    var date = new Date(date);//如果date为13位不需要乘1000
    var Y = date.getFullYear() + '-';
    var M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
    var D = (date.getDate() < 10 ? '0' + (date.getDate()) : date.getDate()) + ' ';
    var h = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours()) + ':';
    var m = (date.getMinutes() <10 ? '0' + date.getMinutes() : date.getMinutes()) + ':';
    var s = (date.getSeconds() <10 ? '0' + date.getSeconds() : date.getSeconds());
    return Y+M+D+h+m+s;
}


/**
 * 进度条格式化
 */
function ProgressFormatter(value, row, index) {
    var cont = ['<div class="progress" style="height:12px; margin:5px 0 0 0;">',
                            '<div class="progress-bar" name="progress" style="width: ', value+'%', '">',
                            '</div>',
                        '</div>'
                ].join('');
    return cont
}


/**
 * 百分比格式化
 */
function percentFormatter(value, row, index) {
    var cont = ['<div name="percent">',
                    value + '%',
                '</div>'
                ].join('');
    return cont
}


/**
 * 新增节点
 */
function initAddOrd() {
    addScriptOrd();
    addFileOrd();
}

/**
 * add script ord
 */
function addScriptOrd() {
    var $addOrdBtn = $("form[data-type='runScript']").siblings().find("button[data-name='addOrd']");
    $addOrdBtn.click(function () {
        $(this).parents('form').before($('#scriptOrdTemplate').html());
        var $ords = $(this).parents('form').siblings("form[data-name^='ord']");
        var ordNum = $ords.length;
        $ords.last().attr('data-name', 'ord'+ ordNum);
        $ords.last().find("pre[id^='editor']").attr('id', 'editor'+ ordNum);
        init_account($ords.last().find("select[name='account']"));
        init_script($ords.last().find("select[name='script']"));
        initTableSelected($ords.last().find("table[data-name='table_selected']"));
        initEditorAction($ords.last().find("pre[id^='editor']"));
        initFont($ords.last().find("select[name='font']"));
    });
}


/**
 * add file ord
 */
function addFileOrd() {
    var $addOrdBtn = $("form[data-type='pushFile']").siblings().find("button[data-name='addOrd']");
    $addOrdBtn.click(function () {
        $(this).parents('form').before($('#fileOrdTemplate').html());
        console.log($("form[data-type='pushFile']"));
        init_account($(this).parents('form').prev().find("select[name='account']"));
        initTableSelected($(this).parents('form').prev().find("table[data-name='table_selected']"));
        initFileTableSelected($(this).parents('form').prev().find("table[data-name='table_selected_file']"));
    });
}


/**
 * ordUp
 */
function ordUp() {
    $('body').on('click', "#main-container button[data-name='ordUp']", function () {
        var $ordForm = $(this).parents("form[data-name^='ord']");
        $ordForm.prev("form[data-name^='ord']").before($ordForm);
    })
}


/**
 * ordDown
 */
function ordDown() {
    $('body').on('click', "#main-container button[data-name='ordDown']", function () {
        var $ordForm = $(this).parents("form[data-name^='ord']");
        $ordForm.next("form[data-name^='ord']").after($ordForm);
    })
}


/**
 * ajax get callback
 */
function ajax_callback1(msg){
    var index = layer.alert(msg, {
        skin: 'layui-layer-molv' //样式类名
    },function(){
       layer.close(index)
    });
}
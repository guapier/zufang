/**
 * Ajax get请求
 * @param uri
 * @param callbackFunction 回调的函数，注意不带括号
 * @param errorFunction 错误处理的函数，注意不带括号
 */
function tomxin_GetInfo(uri, callbackFunction, errorFunction) {
    var Authorization = $.cookie('token');
    uri = encodeURI(uri);//中文要转换
    $.ajax({
        url: base.sys_param.DOMIN + uri,
        type: 'get',
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", Authorization);
        },
        success: function (data) {
            callbackFunction(data);
        },
        error: function (data, textStatus) {
            errorFunction(data)
        }
    });
}

/**
 *  Ajax post请求
 * @param uri
 * @param body 消息体
 * @param callbackFunction 回调的函数，注意不带括号
 * @param errorFunction 错误处理的函数，注意不带括号
 */
function tomxin_PostInfo(uri, body, callbackFunction, errorFunction) {
    var Authorization = $.cookie('token');
    $.ajax({
        type: "POST",
        url: base.sys_param.DOMIN + uri,
        dataType: "json",
        data:JSON.stringify(body),
        contentType: "application/json",
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", Authorization);
        },
        success: function (data) {
            callbackFunction(data);
        },
        error: function (data) {
            errorFunction(data);
        },
        complete: function (XMLHttpRequest, textStatus) {
        }
    });
};

/**
 *  Ajax put请求
 * @param uri
 * @param body 消息体
 * @param callbackFunction 回调的函数，注意不带括号
 * @param errorFunction 错误处理的函数，注意不带括号
 */
function tomxin_PutInfo(uri, body, callbackFunction, errorFunction) {
    var Authorization = $.cookie('token');
    $.ajax({
        type: "PUT",
        url: base.sys_param.DOMIN + uri,
        dataType: "json",
        data:JSON.stringify(body),
        contentType: "application/json",
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", Authorization);
        },
        success: function (data) {
            callbackFunction(data);
        },
        error: function (data) {
            errorFunction(data);
        },
        complete: function (XMLHttpRequest, textStatus) {
        }
    });
};
/**
 * 判断string是否为空
 * @param str
 * @returns {boolean}
 */
function tomxin_IsEmpty(str) {
    if(str == "" || str == null || str == undefined || str == "null" ){ // "",null,undefined
        return true;
    }
    return false;
}


/**
 * 格式化时间
 * @param time
 * @returns {string}
 */
function tomxin_FormatDate(time){
    var date = new Date(time);
    var year = date.getFullYear(),
        month = date.getMonth()+1,//月份是从0开始的
        day = date.getDate(),
        hour = date.getHours(),
        min = date.getMinutes(),
        sec = date.getSeconds();
    var newTime = year + '-' +
        (month < 10? '0' + month : month) + '-' +
        (day < 10? '0' + day : day) + ' ' +
        (hour < 10? '0' + hour : hour) + ':' +
        (min < 10? '0' + min : min) + ':' +
        (sec < 10? '0' + sec : sec);

    return newTime;
}
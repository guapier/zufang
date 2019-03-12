var city_data;

//初始化
$(function () {
    var user_name = $.cookie('user_name');
    if (!tomxin_IsEmpty(user_name)){
        $("#login_button").html(user_name);
    }
    get_city();
});


//用户登录
function userCenter() {
    var user_name = $.cookie('user_name');
    if (tomxin_IsEmpty(user_name)){
        toLogin();
    }else{
        logout();
    }
}

//登录
function toLogin() {
    QC.Login.showPopup({
        appId: base.sys_param.APP_ID,
        redirectURI:base.sys_param.CALLBACKURL
    });
}

//跳转到个人中心
function logout() {
    location.href = "user.html";
}


//后端读取城市
function get_city() {
    var option_model = '<option value="{city_value}" i="set_city_url({i})">{city}</option>';
    var option = "";
    var option_html = "";
    var uri = '/city/list';
    function callbackFunction(data) {
        city_data = data;
        for (i in city_data) {
            //构建option
            option = option_model;
            option = option.replace("{city_value}", i);
            option = option.replace("{city}", city_data[i].cityName);
            option_html += option;
        }
        $("#city").html(option_html);
        //设置网址一网址二
        set_city_url(0);
    }
    tomxin_GetInfo(uri, callbackFunction);
}

//设置网址一网址二和二维码
function set_city_url(value) {
    var city_url = city_data[value].douBanUrl;
    var url_model = '<a href="{city_url}" target="_blank">网址{city_i}</a>';
    var result = city_url.split(",");
    var url_head = "https://www.douban.com/group/";
    var html_a ="";

    for(var i=0; i<result.length; i++){
        var url = url_model;
        url = url_model.replace("{city_url}",url_head + result[i]);
        url = url.replace("{city_i}",i+1);
        html_a += "  " + url;
    }
    $("#city_url").html(html_a);
    //设置二维码
    // var city = city_data[value];
    // if (!tomxin_IsEmpty(city.qrcode)){
    //     var model = '            <p>　　最近在内测一个【{city}简单租房】微信号，内容是一些经过算法和人工同时审核的租房信息，如果您有需要，扫描下方二维码即可体验，如果有任何建议或者意见，请发送邮件到tomxin7@163.com，祝您生活愉快。</p>\n' +
    //         '            <img class="img_wx" src="{qrcode}">';
    //     model = model.replace("{qrcode}", city.qrcode);
    //     model = model.replace("{city}", city.cityName);
    //     $("#qr_code").html(model);
    // }else {
    //     model = '            <p>　　最近在内测一个【程序员的小浪漫】微信公众号号，内容是一些让生活更加简单的小工具或者网站，如果您有需要，扫描下方二维码即可体验，如果有任何建议或者意见，请发送邮件到tomxin7@163.com，祝您生活愉快。</p>\n' +
    //         '            <img class="img_wx" src="http://qiniu.tomxin.cn/blog/180521/8Ke7g8eh53.jpg?imageslim">'
    //     $("#qr_code").html(model);
    // }
}

//添加用户的记录
function postRecord() {
    var remind = $("#email").val();
    if (tomxin_IsEmpty(remind)){
        remind = $("#wx").val();
    }
    var uri = "/record";
    var body = {
        "cityName": $("#city option:selected").text(),
        "keyWord": $("#key").val(),
        "remindType": $("input[name='remindType']:checked").val(),
        "remind": remind,
    };

    function callbackFunction(data){
        alert("添加成功");
        location.href='user.html';
    }
    tomxin_PostInfo(uri, body, callbackFunction)
};

//校验邮箱格式
function checkEmail(str){
    var re = /^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$/;
    if (!re.test(str)) {
        alert("邮箱格式不正确");
        return true;
    }
}

//点击提交
$('.btn-loading-example').click(function () {
    var token = $.cookie('token');
    if (tomxin_IsEmpty(token)) {
        alert("请登录后重试");
        return false;
    };
    var email = $("#email").val();
    var wx = $("#wx").val();
    var key = $("#key").val();
    key   =   key.replace(/\s+/g,"");
    if (tomxin_IsEmpty(key)){
        alert("关键字不能为空");
        return false;
    }
    //如果不是微信，判断邮箱格式
    if (tomxin_IsEmpty(wx)) {
        if (checkEmail(email)){
            return false;
        }
    }else {
        //判断微信格式
        if (wx.length < 20){
            alert("请检查微信推送id格式是否正确")
        }
    }

    var $btn = $(this);
    $btn.button('loading');
    postRecord();
});

//跳转到个人中心
function to_user(){
    var token = $.cookie('token');
    if (tomxin_IsEmpty(token)) {
        alert("请登录后重试");
        return false;
    };
    location.href = "user.html";
}


//切换微信
function switch_wx() {
    $("#mail_tips").attr("style","display: none");
    $("#wx_tips").attr("style","");
}

//切换邮箱
function switch_mail() {
    $("#wx_tips").attr("style","display: none");
    $("#mail_tips").attr("style","");
}
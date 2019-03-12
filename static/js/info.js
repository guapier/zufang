var id = getQueryString("id");
get_info(id)


//获取url中的参数
function getQueryString(name) {
    var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return unescape(r[2]);
    }
    return null;
}

function get_info(id) {
    //拼接发起请求的URI
    var uri = '/info/' + id;

    //请求成功后的回调函数
    function callbackFunction(data) {
        // console.log(data)
        set_info(data)
    }

    //请求失败后的回调函数,可以不处理
    function errorFunction(data) {
        console.log(data.responseJSON.message)
    }

    //发起ajax get请求，注意函数传参不能加括号
    tomxin_GetInfo(uri, callbackFunction, errorFunction);
}

function set_info(data) {
    var model = '  <p>  亲爱的{user_name} 你的任务:【{task}】</p><p> 在{create_time} 监控到以下房源</p>\n' +
        '\n' +
        '      <div class="remind"> 风险提醒：以下内容来自互联网，未经验证，请自行甄别，谨防受骗'

    model = model.replace("{user_name}", data['userName'])
    model = model.replace("{create_time}", data['createTime'])
    model = model.replace("{task}", data['task'])
    $("#info").html(model);


    //处理信息列表
    model = '            <tr>\n' +
        '              <td><a href="{url}" target="_blank">{title}</a></td>\n' +
        '            </tr>'

    html_str = ''
    var recruitList = JSON.parse(data['content']);

    //循环输出
    for (i in recruitList) {
        var recruit = recruitList[i];
        model_str = model.replace("{url}", recruit.url)
        model_str = model_str.replace("{title}", recruit.title)
        html_str = html_str + model_str;
    }
    $("#house").html(html_str);

}
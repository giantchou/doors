/******************************************************************************
* filename: index.js
* Include Modul Scripting


*******************************************************************************/
SKIN_PATH="/Skins/default/";
function initCommonHeader() {
    $.get("/ajax.ashx?action=initcommonheader&t=" + Math.random(), function (rsp) {
        var IM = gav(rsp, "showIM");
        showIM(IM);
        var username = gav(rsp, "username");
        if (username.length > 0) {
            $j("commonHeaderGuest").hide();
            $j("commonHeaderUsername").html(username);
            $j("commonHeaderUser").fadeIn(80);
            $j("login_user").show();
            $j("user_default").hide();
            return username;
        }
    });
    return "";
}
//获取电话号码
function GetInfoTel() {
    var domae = window.location.host;
    $.post("/ajax.ashx?action=showtel&t=" + Math.random(), {
        domae: domae
    }, function (msg) {
        var sMsg = gav(msg, "msg");
        var sta = gav(msg, "state");
        if (sta == 1) {
            if (sMsg != "") {
                $(".phone h3").text(sMsg);
              
            }

        }

    });
}
//获取公司底部信息
function GetInfoadd() {
    var domae = window.location.host;
    $.post("/ajax.ashx?action=showaddr&t=" + Math.random(), {
        domae: domae
    }, function (msg) {
        var sMsg = gav(msg, "msg");
        var sta = gav(msg, "state");
        if (sta == 1) {
            if (sMsg != "") {
                $("#addr").html(sMsg);
                $("#addr").next("p").remove();
            }

        }

    });
}
function subLeaveword(src) {
    var name = $("#txtName").val();
    var phone = $("#txtPhone").val();
    var email = $("#txtEmail").val();
    var shortdesc = $("#qq").val();
    var errorMsg = "";
    var reg = /^\s*$/;
    if (name == "" || name == "姓名") {
        errorMsg += "<p>联系人不可为空</p>";
    }
    if (phone == "" || phone == "联系电话") {
        errorMsg += "<p>手机不可为空</p>";
    }
    if (email == "" || email == "邮箱") {
        errorMsg += "<p>邮箱不可为空</p>";
    }
//    if (shortdesc == "" || shortdesc == "需求") {
//        errorMsg += "<p>您的需求不能为空</p>";
//    }

    var partten = /^1\d{10}$/;
    if (!partten.test(phone)) {
        errorMsg += "<p>请输入正确的手机号码</p>";
    }
    var ptn = /\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/;

    var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (!filter.test(email)) {
        errorMsg += "<p>请输入正确的邮箱</p>";
    }
    if (errorMsg.length > 0) {
        $a(errorMsg);
        return;
    }
    showProc(src);
    $.post("/ajax.ashx?action=subLeavewords&t=" + Math.random(), {

        name: name,
        phone: phone,
        email: email,
        desc: shortdesc

    }, function (msg) {
        var sta = gav(msg, "state");
        var sMsg = gav(msg, "msg");
        if (sta == "1") {
            $a(sMsg, 1);

            $("#txtName").val("");
            $("#txtPhone").val("");
            $("#txtEmail").val("");
            $("#qq").val("");

        } else {
            $a(sMsg);
        }

        showProc(src, false);
    });

}


function resrt(str)
{

    str=str.toLocaleString().replace("","");
     str=str.toLocaleString().replace( "& ", "&amp; ");
    str=str.toLocaleString().replace( " ' ", "&#39; ");
    str=str.toLocaleString().replace( "alert", "&#34; ");
    str = str.toLocaleString().replace("script", "&#34; ");
    str=str.toLocaleString().replace( " < ", "&lt");
    str=str.toLocaleString().replace( "> ", "&gt");
    str=str.toLocaleString().replace("where", "$1h&#101;re ");
    str=str.toLocaleString().replace("select", "$1el&#101;ct ");
    str=str.toLocaleString().replace("insert", "$1ns&#101;rt ");
    str=str.toLocaleString().replace("create", "$1r&#101;ate ");
    str=str.toLocaleString().replace("drop","$1ro&#112; ");
    str=str.toLocaleString().replace("alter", "$1lt&#101;r ");
    str=str.toLocaleString().replace("delete", "$1el&#101;te ");
    str=str.toLocaleString().replace("update", "$1p&#100;ate ");
    str = str.toLocaleString().replace("and", "$1h&#101;nd ");
    str = str.toLocaleString().replace("</title>", "$1h&#101;nd ");
    str = str.toLocaleString().replace("</head>", "$1h&#101;nd ");
    str = str.toLocaleString().replace("</body>", "$1h&#101;nd ");
   
}

function xuanze() {
    
    var xz =document.getElementById('seachkeywords').value;
   
    if (xz.length == 0) {
        xz = "";
    }
    window.location.href = '/Search/Index.aspx?objtype=product&kwd=' +xz;
}
/********************
* 根据key获取 ajax对象节点值getAjaxVal
* xMsg : xml对象
* key : 节点的属性key
********************/
function gav(xMsg, key) {
    var jMsg = $(xMsg);
    var s = $(jMsg.find("node[key=" + key + "]")).text();
    return s;
}
//是否显示在线客服
function showIM(res) {
    if ($("#bodd").html() != "") {
        if (res == "True") {
            $("#bodd").show();
            $("#kefubtn").hide();
            $("#divOranIm").show();
        }
        else {
            $("#bodd").hide();
            $("#kefubtn").show();
            $("#divOranIm").hide();
        }
    }
}


//初始化头部热门关键词
function initCommonHeaderKeywords(_s) {
    if (_s == "") _s = "6";
    $.post("/ajax.ashx?action=initcommonheaderkeywords&t=" + Math.random(), {
        s: _s
    }, function (msg) {
        $j("commonHeaderkeywords").html(msg);
    });
}

function $j(elmId) { return $("#" + elmId); }
function $v(elmId, val) {
    if (val == null) {
        var o = $j(elmId).attr("value");
        if (o == null || o == undefined)
            return "";
        return o;
    } else {
        return $j(elmId).attr("value", val);
    }
}
function $tv(elmId) { return $.trim($v(elmId)); }


    //邮件订阅
function subscription(src, elmId) {
    if (elmId == null) {
        elmId = "txtSubscriptionEmail";
    }
    var _email = $.trim($j(elmId).val());
    var ptn = /\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/;
    if (_email.length == 0) {
        $a("E-Mail 不可为空");
        $j(elmId).focus();
        return false;
    }
    if (!ptn.test(_email)) {
        $a("E-Mail 格式错误。");
        $j(elmId).focus();
        return false;
    }
    showProc(src);
    $.post("/ajax.ashx?action=subscription&t=" + Math.random(), {
        email: _email
    }, function(msg) {
        var sta = gav(msg, "state");
        var sMsg = gav(msg, "msg");
        if (sta == "1") {
            $a(sMsg, 1);
        } else {
            $a(sMsg);
        }
        showProc(src, false);
    });
}

function showProc(src, show) {
    var oImg = $j("imgProc");
    if (show == null)
        show = true;
    if (show) {
        $(src).hide();
        if (oImg.length > 0) {
            oImg.remove();
        }
        $("<img src='" + SKIN_PATH + "img/processing.gif' id='imgProc' alt='正在处理' />").insertAfter(src);
    } else {
        $(src).show();
        oImg.remove();
    }
}
function hideDdl(cntrId) {
    var arrTags = ["select", "iframe", "applet", "object"];
    var jCntr;
    if (cntrId != null) {
        jCntr = $j(cntrId);
    } else {
        jCntr = $(document.body);
    }
    for (var i = 0; i < arrTags.length; ++i) {
        jCntr.find(arrTags[i]).css("visibility", "hidden");
    }

}

function $a(sMsg, boxType, autoClose, focusElmId, sTitle, behavior) {
    if (boxType == null) {
        boxType = 2;
    }
    if (autoClose == null) {
        autoClose = -1;
    }
    //标题
    if (sTitle == null) {
        sTitle = "消息提示";
    }

    hideDdl();
    var jMesbook1 = $j("mesbook1");
    if (jMesbook1.length == 0) {
        var sHtml = "<div id='mesbook1'>"
				+ "<div><img style='float:right' onclick='hideMsg()' id='mesbook1ImgClose' src='" + SKIN_PATH + "Img/ico9_close.gif' alt='关闭' class='fr p vam ml5' /><span id='mesbook1Title'></span></div>"
				+ "<dl class='b1'>"
					+ "<dt><img id='mesbook1Icon' src='" + SKIN_PATH + "Img/message_ico_03.gif' alt='' title='' /></dt>"
					+ "<dd class='l_25' id='mesbook1Msg'></dd>"
					+ "<dd class='b' style='visibility:hidden' id='mesbook1AutoClose'>此窗口<span id='mesbook1Delay' style='margin:0 5px;'></span>秒钟后自动关闭。</dd>"
					+ "<dd id='mesbook1Btns'>"
					+ "<input type='button' class='b15' value='关 闭' />"
					+ "</dd>"
				+ "</dl>"
			+ "</div>";
        $(document.body).append(sHtml);
    }
    var jMesbook1 = $j("mesbook1");
    var jMesbook1ImgClose = $j("mesbook1ImgClose");
    var jMesbook1Icon = $j("mesbook1Icon");
    var jMesbook1Msg = $j("mesbook1Msg");
    var jMesbook1AutoClose = $j("mesbook1AutoClose");
    var jMesbook1Delay = $j("mesbook1Delay");
    var jMesbook1Title = $j("mesbook1Title");
    var jMesbook1Btns = $j("mesbook1Btns");

    jMesbook1Title.html(sTitle);
    //消息内容
    jMesbook1Msg.html(sMsg);
    //图标
    var iconPath = SKIN_PATH + "Img/";
    switch (boxType) {
        case 1: iconPath += "ico_ok.gif"; break;
        case 2: iconPath += "ico_info.gif"; break;
        case 3: iconPath += "ioc_ques.gif"; break;
        case -1: iconPath += "ico_error.gif"; break;
        default: iconPath += "ico_normal.gif"; break;
    }
    jMesbook1Icon.attr("src", iconPath);

    //关闭按钮
    var okBtn = jMesbook1Btns.find("input");
    okBtn.removeAttr("onclick");
    okBtn.click(function() {
        hideMsg();
        if (focusElmId != null) {
            $j(focusElmId).focus();
        }
        if (behavior != null) {
            behavior();
        }
    });
    jMesbook1ImgClose.removeAttr("onclick");
    jMesbook1ImgClose.click(function() {
        hideMsg();
        if (focusElmId != null) {
            $j(focusElmId).focus();
        }
        if (behavior != null) {
            behavior();
        }
    });
    okBtn.focus();

    //显示
    showFullBg();
    setCM("mesbook1");
    //relocation("mesbook1");
    jMesbook1.fadeIn(80);
}
/********************
* 显示一个全屏灰度背景
* elmId : 元素ID或元素
********************/
function showFullBg(elmId, isHideDdl, opacity, bgColor, zIndex, speed, behavior) {
    if (elmId == null) {
        elmId = "oran_full_bg";
    }
    var jElm = $j(elmId);
    if (jElm.length == 0) {
        var sHtml = "<div style='position:absolute;top:0;left:0;display:none;' id='" + elmId + "'></div>";
        $(document.body).append(sHtml);
    }
    if (opacity == null) {
        opacity = 0.75;
    }
    if (bgColor == null) {
        bgColor = "#777";
    }
    if (zIndex == null) {
        zIndex = "9";
    }
    if (speed == null) {
        speed = 80;
    }
    if (isHideDdl == null) {
        isHideDdl = true;
    }
    var jElm = $j(elmId);
    var dd = document.documentElement;
    var sWidth = dd.scrollWidth;
    var sHeight = dd.scrollHeight;
    var cH = dd.clientHeight;
    var cW = dd.clientWidth;
    if (sHeight < cH) {
        sHeight = cH;
    }
    if (sWidth < cW) {
        sWidth = cW;
    }
    jElm.css({ "z-index": zIndex, "background": bgColor, "opacity": opacity, "filter": "progid:DXImageTransform.Microsoft.Alpha(opacity=" + opacity * 100 + ")" });
    jElm.css({ "height": sHeight, "width": sWidth });
    if (isHideDdl) {
        hideDdl(null, behavior);
    }
    jElm.fadeIn(speed);
    if (behavior != null) {
        behavior();
    }
}

function setCM(elmId, speed) {
    var jElm;
    if (typeof (elmId).toString().toLowerCase() == "string") {
        jElm = $j(elmId);
    } else {
        jElm = $(elmId);
    }
    if (speed == null) {
        speed = 80;
    }
    var h = jElm.height() / 2;
    var w = jElm.width() / 2;
    var $w = $(window);
    var top = $w.height() / 2 + $w.scrollTop();
    //jElm.css({ "top": top+"px", "margin-top" : "0px !important", "left": "50%", "margin-left": "-" + w + "px" });
    jElm.css({ top: top + "px", marginTop: "0px", left: "50%", marginLeft: (-w) + "px" });
    var isIE = navigator.userAgent.toUpperCase().indexOf("MSIE") == -1 ? false : true;

    $w.scroll(function() {
        var top = $w.height() / 2 + $w.scrollTop();
        jElm.css({ 'top': top + 'px' });
    });
    //if(isIE){
    jElm.css({ "position": "absolute", "z-index": "999" });
    //    }else{
    //        jElm.css({ "position": "fixed", "z-index": "999"});
    //    }
    jElm.fadeIn(speed);
}

function setCMS(elmId, speed) {
    var jElm;
    if (typeof (elmId).toString().toLowerCase() == "string") {
        jElm = $j(elmId);
    } else {
        jElm = $(elmId);
    }
    if (speed == null) {
        speed = 80;
    }
    var h = jElm.height() / 2;
    var w = jElm.width() / 2;
    var height = document.documentElement.scrollTop;
    if (height > 100) {
        jElm.css({ "top": "50%", "margin-top": "-" + h + "px", "left": "50%", "margin-left": "-" + w + "px" });
    }
    else {
        h = 200;
        jElm.css({ "margin-top": "-" + h + "px", "left": "50%", "margin-left": "-" + w + "px" });
    }

    jElm.css({ "position": "absolute", "z-index": "999" });
    jElm.fadeIn(speed);
}
/********************
* 重置一个层为绝对居中于窗口的位置
* elmId : 元素ID或元素
********************/
function relocation(elmId) {
    var jElm;
    if (typeof (elmId).toString().toLowerCase() == "string") {
        jElm = $j(elmId);
    } else {
        jElm = $(elmId);
    }
    if (jElm.length == 0) {
        return;
    }

    var dd = document.documentElement;
    var t = (dd.scrollTop - (jElm.height() / 2) + "px");
    jElm.css({ "margin-top": t/*, "left": l */ });
}

/********************
* 隐藏消息提示层
********************/
function hideMsg() {
    showDdl();
    var jShadow = $j("mesbook1");
    hideFullBg();
    jShadow.fadeOut(80);
}

/********************
* 隐藏下拉框函数
********************/
function showDdl() {
    var arrTags = ["select", "iframe", "applet", "object"];
    for (var i = 0; i < arrTags.length; ++i) {
        $(arrTags[i]).css("visibility", "visible");
    }
}

/********************
* 隐藏全屏灰度背景
* speed : (可选)渐变消退的速度
********************/
function hideFullBg(elmId, speed) {
    if (elmId == null) {
        elmId = "oran_full_bg";
    }
    if (speed == null) {
        speed = 80;
    }
    var jElm = $j(elmId);
    jElm.fadeOut(speed);
    showDdl();
}




//用户登陆
function LoginCheck(_username, _password) {
    if (_username == undefined || _username.length == 0) {
        $a("请输入用户名", "错误提示", "txtUsername");
        return;
    }
    if (_password == undefined || _password.length == 0) {
        $a("请输入密码", "错误提示", "txtPassword");
        return;
    }
    $.post("/ajax.ashx?action=logincheck&t=" + Math.random(), {
        username: _username,
        password: _password
    },
       function(msg) {
           if (gav(msg, "state") == "1") {
               $a(gav(msg, "msg"), null, null, null, null, function() {
                   window.location.href = location.href + "?t=" + Math.random();
               });
               //window.location.href = url;
           }
           else {
               $a(gav(msg, "msg"));
           };
       });
}


function SearchObjectByGet(FieldList, url, getUrlOnly) {
    if (getUrlOnly == null) {
        getUrlOnly = false;
    }
    var newUrl = GetSearchURL(FieldList, url);
    if (getUrlOnly) {
        return newUrl;
    }
    window.location.href = newUrl;
}

//根据字段列表获取查询页面路径字符串
//FieldList格式：控件ID名称,查询字段名称|控件ID名称1,查询字段名称1|.. 
function GetSearchURL(FieldList, URL) {
    //1\定义变量
    if (URL == null) {
        URL = getIntactRawUrl();
    }

    //2\循环把变量列表取出来,组合成URL
    var TempFieldList = FieldList.split("|");
    for (var i = 0; i < TempFieldList.length; i++) {
        //1>寻找控件
        var control1 = TempFieldList[i].split(",");
        var controlname;
        var control = document.getElementById(control1[0]);
        if (control1.length == 2) { controlname = control1[1]; } else { controlname = control1[0]; }
        if (control != null) {
            //2>取出控件的值
            var controlvalue = control.value;
            //3>设置URL
            if (controlvalue != null) {
                URL += "&" + controlname + "=" + encodeURIComponent(controlvalue);
            }
        }
    }
    return URL;
}
function getIntactRawUrl() {
    var path = location.href;
    var pos;
    pos = path.lastIndexOf('#');
    path = path.substring(0, pos);
    return path;
}

/********************
* 增加书签
* url : URL
* title : 收藏项目的标题
********************/
function addBookmark(url, title) {
    if (window.sidebar) {
        window.sidebar.addPanel(title, url, "");
    } else if (document.all) {
        window.external.AddFavorite(url, title);
    } else if (window.opera && window.print) {
        return true;
    }
}

//加入收藏
function addBookmark() {
    var title = document.title;
    var url = document.URL;
    try {
        window.external.addFavorite(url, title);
    }
    catch (e) {
        try {
            window.sidebar.addPanel(title, url, "");
        }
        catch (e) {
            alert("抱歉，您所使用的浏览器无法完成此操作。\n\n加入收藏失败，请使用Ctrl+D进行添加");
        }
    }
}


/*!
* SuperSlide v2.1.1 
* 轻松解决网站大部分特效展示问题
* 详尽信息请看官网：http://www.SuperSlide2.com/
*
* Copyright 2011-2013, 大话主席
*
* 请尊重原创，保留头部版权
* 在保留版权的前提下可应用于个人或商业用途

* v2.1.1：修复当调用多个SuperSlide，并设置returnDefault:true 时返回defaultIndex索引错误

*/

!function (a) { a.fn.slide = function (b) { return a.fn.slide.defaults = { type: "slide", effect: "fade", autoPlay: !1, delayTime: 500, interTime: 2500, triggerTime: 150, defaultIndex: 0, titCell: ".hd li", mainCell: ".bd", targetCell: null, trigger: "mouseover", scroll: 1, vis: 1, titOnClassName: "on", autoPage: !1, prevCell: ".prev", nextCell: ".next", pageStateCell: ".pageState", opp: !1, pnLoop: !0, easing: "swing", startFun: null, endFun: null, switchLoad: null, playStateCell: ".playState", mouseOverStop: !0, defaultPlay: !0, returnDefault: !1 }, this.each(function () { var c = a.extend({}, a.fn.slide.defaults, b), d = a(this), e = c.effect, f = a(c.prevCell, d), g = a(c.nextCell, d), h = a(c.pageStateCell, d), i = a(c.playStateCell, d), j = a(c.titCell, d), k = j.size(), l = a(c.mainCell, d), m = l.children().size(), n = c.switchLoad, o = a(c.targetCell, d), p = parseInt(c.defaultIndex), q = parseInt(c.delayTime), r = parseInt(c.interTime); parseInt(c.triggerTime); var Q, t = parseInt(c.scroll), u = parseInt(c.vis), v = "false" == c.autoPlay || 0 == c.autoPlay ? !1 : !0, w = "false" == c.opp || 0 == c.opp ? !1 : !0, x = "false" == c.autoPage || 0 == c.autoPage ? !1 : !0, y = "false" == c.pnLoop || 0 == c.pnLoop ? !1 : !0, z = "false" == c.mouseOverStop || 0 == c.mouseOverStop ? !1 : !0, A = "false" == c.defaultPlay || 0 == c.defaultPlay ? !1 : !0, B = "false" == c.returnDefault || 0 == c.returnDefault ? !1 : !0, C = 0, D = 0, E = 0, F = 0, G = c.easing, H = null, I = null, J = null, K = c.titOnClassName, L = j.index(d.find("." + K)), M = p = -1 == L ? p : L, N = p, O = p, P = m >= u ? 0 != m % t ? m % t : t : 0, R = "leftMarquee" == e || "topMarquee" == e ? !0 : !1, S = function () { a.isFunction(c.startFun) && c.startFun(p, k, d, a(c.titCell, d), l, o, f, g) }, T = function () { a.isFunction(c.endFun) && c.endFun(p, k, d, a(c.titCell, d), l, o, f, g) }, U = function () { j.removeClass(K), A && j.eq(N).addClass(K) }; if ("menu" == c.type) return A && j.removeClass(K).eq(p).addClass(K), j.hover(function () { Q = a(this).find(c.targetCell); var b = j.index(a(this)); I = setTimeout(function () { switch (p = b, j.removeClass(K).eq(p).addClass(K), S(), e) { case "fade": Q.stop(!0, !0).animate({ opacity: "show" }, q, G, T); break; case "slideDown": Q.stop(!0, !0).animate({ height: "show" }, q, G, T) } }, c.triggerTime) }, function () { switch (clearTimeout(I), e) { case "fade": Q.animate({ opacity: "hide" }, q, G); break; case "slideDown": Q.animate({ height: "hide" }, q, G) } }), B && d.hover(function () { clearTimeout(J) }, function () { J = setTimeout(U, q) }), void 0; if (0 == k && (k = m), R && (k = 2), x) { if (m >= u) if ("leftLoop" == e || "topLoop" == e) k = 0 != m % t ? (0 ^ m / t) + 1 : m / t; else { var V = m - u; k = 1 + parseInt(0 != V % t ? V / t + 1 : V / t), 0 >= k && (k = 1) } else k = 1; j.html(""); var W = ""; if (1 == c.autoPage || "true" == c.autoPage) for (var X = 0; k > X; X++) W += "<li>" + (X + 1) + "</li>"; else for (var X = 0; k > X; X++) W += c.autoPage.replace("$", X + 1); j.html(W); var j = j.children() } if (m >= u) { l.children().each(function () { a(this).width() > E && (E = a(this).width(), D = a(this).outerWidth(!0)), a(this).height() > F && (F = a(this).height(), C = a(this).outerHeight(!0)) }); var Y = l.children(), Z = function () { for (var a = 0; u > a; a++) Y.eq(a).clone().addClass("clone").appendTo(l); for (var a = 0; P > a; a++) Y.eq(m - a - 1).clone().addClass("clone").prependTo(l) }; switch (e) { case "fold": l.css({ position: "relative", width: D, height: C }).children().css({ position: "absolute", width: E, left: 0, top: 0, display: "none" }); break; case "top": l.wrap('<div class="tempWrap" style="overflow:hidden; position:relative; height:' + u * C + 'px"></div>').css({ top: -(p * t) * C, position: "relative", padding: "0", margin: "0" }).children().css({ height: F }); break; case "left": l.wrap('<div class="tempWrap" style="overflow:hidden; position:relative; width:' + u * D + 'px"></div>').css({ width: m * D, left: -(p * t) * D, position: "relative", overflow: "hidden", padding: "0", margin: "0" }).children().css({ "float": "left", width: E }); break; case "leftLoop": case "leftMarquee": Z(), l.wrap('<div class="tempWrap" style="overflow:hidden; position:relative; width:' + u * D + 'px"></div>').css({ width: (m + u + P) * D, position: "relative", overflow: "hidden", padding: "0", margin: "0", left: -(P + p * t) * D }).children().css({ "float": "left", width: E }); break; case "topLoop": case "topMarquee": Z(), l.wrap('<div class="tempWrap" style="overflow:hidden; position:relative; height:' + u * C + 'px"></div>').css({ height: (m + u + P) * C, position: "relative", padding: "0", margin: "0", top: -(P + p * t) * C }).children().css({ height: F }) } } var $ = function (a) { var b = a * t; return a == k ? b = m : -1 == a && 0 != m % t && (b = -m % t), b }, _ = function (b) { var c = function (c) { for (var d = c; u + c > d; d++) b.eq(d).find("img[" + n + "]").each(function () { var b = a(this); if (b.attr("src", b.attr(n)).removeAttr(n), l.find(".clone")[0]) for (var c = l.children(), d = 0; d < c.size(); d++) c.eq(d).find("img[" + n + "]").each(function () { a(this).attr(n) == b.attr("src") && a(this).attr("src", a(this).attr(n)).removeAttr(n) }) }) }; switch (e) { case "fade": case "fold": case "top": case "left": case "slideDown": c(p * t); break; case "leftLoop": case "topLoop": c(P + $(O)); break; case "leftMarquee": case "topMarquee": var d = "leftMarquee" == e ? l.css("left").replace("px", "") : l.css("top").replace("px", ""), f = "leftMarquee" == e ? D : C, g = P; if (0 != d % f) { var h = Math.abs(0 ^ d / f); g = 1 == p ? P + h : P + h - 1 } c(g) } }, ab = function (a) { if (!A || M != p || a || R) { if (R ? p >= 1 ? p = 1 : 0 >= p && (p = 0) : (O = p, p >= k ? p = 0 : 0 > p && (p = k - 1)), S(), null != n && _(l.children()), o[0] && (Q = o.eq(p), null != n && _(o), "slideDown" == e ? (o.not(Q).stop(!0, !0).slideUp(q), Q.slideDown(q, G, function () { l[0] || T() })) : (o.not(Q).stop(!0, !0).hide(), Q.animate({ opacity: "show" }, q, function () { l[0] || T() }))), m >= u) switch (e) { case "fade": l.children().stop(!0, !0).eq(p).animate({ opacity: "show" }, q, G, function () { T() }).siblings().hide(); break; case "fold": l.children().stop(!0, !0).eq(p).animate({ opacity: "show" }, q, G, function () { T() }).siblings().animate({ opacity: "hide" }, q, G); break; case "top": l.stop(!0, !1).animate({ top: -p * t * C }, q, G, function () { T() }); break; case "left": l.stop(!0, !1).animate({ left: -p * t * D }, q, G, function () { T() }); break; case "leftLoop": var b = O; l.stop(!0, !0).animate({ left: -($(O) + P) * D }, q, G, function () { -1 >= b ? l.css("left", -(P + (k - 1) * t) * D) : b >= k && l.css("left", -P * D), T() }); break; case "topLoop": var b = O; l.stop(!0, !0).animate({ top: -($(O) + P) * C }, q, G, function () { -1 >= b ? l.css("top", -(P + (k - 1) * t) * C) : b >= k && l.css("top", -P * C), T() }); break; case "leftMarquee": var c = l.css("left").replace("px", ""); 0 == p ? l.animate({ left: ++c }, 0, function () { l.css("left").replace("px", "") >= 0 && l.css("left", -m * D) }) : l.animate({ left: --c }, 0, function () { l.css("left").replace("px", "") <= -(m + P) * D && l.css("left", -P * D) }); break; case "topMarquee": var d = l.css("top").replace("px", ""); 0 == p ? l.animate({ top: ++d }, 0, function () { l.css("top").replace("px", "") >= 0 && l.css("top", -m * C) }) : l.animate({ top: --d }, 0, function () { l.css("top").replace("px", "") <= -(m + P) * C && l.css("top", -P * C) }) } j.removeClass(K).eq(p).addClass(K), M = p, y || (g.removeClass("nextStop"), f.removeClass("prevStop"), 0 == p && f.addClass("prevStop"), p == k - 1 && g.addClass("nextStop")), h.html("<span>" + (p + 1) + "</span>/" + k) } }; A && ab(!0), B && d.hover(function () { clearTimeout(J) }, function () { J = setTimeout(function () { p = N, A ? ab() : "slideDown" == e ? Q.slideUp(q, U) : Q.animate({ opacity: "hide" }, q, U), M = p }, 300) }); var bb = function (a) { H = setInterval(function () { w ? p-- : p++, ab() }, a ? a : r) }, cb = function (a) { H = setInterval(ab, a ? a : r) }, db = function () { z || (clearInterval(H), bb()) }, eb = function () { (y || p != k - 1) && (p++, ab(), R || db()) }, fb = function () { (y || 0 != p) && (p--, ab(), R || db()) }, gb = function () { clearInterval(H), R ? cb() : bb(), i.removeClass("pauseState") }, hb = function () { clearInterval(H), i.addClass("pauseState") }; if (v ? R ? (w ? p-- : p++, cb(), z && l.hover(hb, gb)) : (bb(), z && d.hover(hb, gb)) : (R && (w ? p-- : p++), i.addClass("pauseState")), i.click(function () { i.hasClass("pauseState") ? gb() : hb() }), "mouseover" == c.trigger ? j.hover(function () { var a = j.index(this); I = setTimeout(function () { p = a, ab(), db() }, c.triggerTime) }, function () { clearTimeout(I) }) : j.click(function () { p = j.index(this), ab(), db() }), R) { if (g.mousedown(eb), f.mousedown(fb), y) { var ib, jb = function () { ib = setTimeout(function () { clearInterval(H), cb(0 ^ r / 10) }, 150) }, kb = function () { clearTimeout(ib), clearInterval(H), cb() }; g.mousedown(jb), g.mouseup(kb), f.mousedown(jb), f.mouseup(kb) } "mouseover" == c.trigger && (g.hover(eb, function () { }), f.hover(fb, function () { })) } else g.click(eb), f.click(fb) }) } } (jQuery), jQuery.easing.jswing = jQuery.easing.swing, jQuery.extend(jQuery.easing, { def: "easeOutQuad", swing: function (a, b, c, d, e) { return jQuery.easing[jQuery.easing.def](a, b, c, d, e) }, easeInQuad: function (a, b, c, d, e) { return d * (b /= e) * b + c }, easeOutQuad: function (a, b, c, d, e) { return -d * (b /= e) * (b - 2) + c }, easeInOutQuad: function (a, b, c, d, e) { return (b /= e / 2) < 1 ? d / 2 * b * b + c : -d / 2 * (--b * (b - 2) - 1) + c }, easeInCubic: function (a, b, c, d, e) { return d * (b /= e) * b * b + c }, easeOutCubic: function (a, b, c, d, e) { return d * ((b = b / e - 1) * b * b + 1) + c }, easeInOutCubic: function (a, b, c, d, e) { return (b /= e / 2) < 1 ? d / 2 * b * b * b + c : d / 2 * ((b -= 2) * b * b + 2) + c }, easeInQuart: function (a, b, c, d, e) { return d * (b /= e) * b * b * b + c }, easeOutQuart: function (a, b, c, d, e) { return -d * ((b = b / e - 1) * b * b * b - 1) + c }, easeInOutQuart: function (a, b, c, d, e) { return (b /= e / 2) < 1 ? d / 2 * b * b * b * b + c : -d / 2 * ((b -= 2) * b * b * b - 2) + c }, easeInQuint: function (a, b, c, d, e) { return d * (b /= e) * b * b * b * b + c }, easeOutQuint: function (a, b, c, d, e) { return d * ((b = b / e - 1) * b * b * b * b + 1) + c }, easeInOutQuint: function (a, b, c, d, e) { return (b /= e / 2) < 1 ? d / 2 * b * b * b * b * b + c : d / 2 * ((b -= 2) * b * b * b * b + 2) + c }, easeInSine: function (a, b, c, d, e) { return -d * Math.cos(b / e * (Math.PI / 2)) + d + c }, easeOutSine: function (a, b, c, d, e) { return d * Math.sin(b / e * (Math.PI / 2)) + c }, easeInOutSine: function (a, b, c, d, e) { return -d / 2 * (Math.cos(Math.PI * b / e) - 1) + c }, easeInExpo: function (a, b, c, d, e) { return 0 == b ? c : d * Math.pow(2, 10 * (b / e - 1)) + c }, easeOutExpo: function (a, b, c, d, e) { return b == e ? c + d : d * (-Math.pow(2, -10 * b / e) + 1) + c }, easeInOutExpo: function (a, b, c, d, e) { return 0 == b ? c : b == e ? c + d : (b /= e / 2) < 1 ? d / 2 * Math.pow(2, 10 * (b - 1)) + c : d / 2 * (-Math.pow(2, -10 * --b) + 2) + c }, easeInCirc: function (a, b, c, d, e) { return -d * (Math.sqrt(1 - (b /= e) * b) - 1) + c }, easeOutCirc: function (a, b, c, d, e) { return d * Math.sqrt(1 - (b = b / e - 1) * b) + c }, easeInOutCirc: function (a, b, c, d, e) { return (b /= e / 2) < 1 ? -d / 2 * (Math.sqrt(1 - b * b) - 1) + c : d / 2 * (Math.sqrt(1 - (b -= 2) * b) + 1) + c }, easeInElastic: function (a, b, c, d, e) { var f = 1.70158, g = 0, h = d; if (0 == b) return c; if (1 == (b /= e)) return c + d; if (g || (g = .3 * e), h < Math.abs(d)) { h = d; var f = g / 4 } else var f = g / (2 * Math.PI) * Math.asin(d / h); return -(h * Math.pow(2, 10 * (b -= 1)) * Math.sin((b * e - f) * 2 * Math.PI / g)) + c }, easeOutElastic: function (a, b, c, d, e) { var f = 1.70158, g = 0, h = d; if (0 == b) return c; if (1 == (b /= e)) return c + d; if (g || (g = .3 * e), h < Math.abs(d)) { h = d; var f = g / 4 } else var f = g / (2 * Math.PI) * Math.asin(d / h); return h * Math.pow(2, -10 * b) * Math.sin((b * e - f) * 2 * Math.PI / g) + d + c }, easeInOutElastic: function (a, b, c, d, e) { var f = 1.70158, g = 0, h = d; if (0 == b) return c; if (2 == (b /= e / 2)) return c + d; if (g || (g = e * .3 * 1.5), h < Math.abs(d)) { h = d; var f = g / 4 } else var f = g / (2 * Math.PI) * Math.asin(d / h); return 1 > b ? -.5 * h * Math.pow(2, 10 * (b -= 1)) * Math.sin((b * e - f) * 2 * Math.PI / g) + c : .5 * h * Math.pow(2, -10 * (b -= 1)) * Math.sin((b * e - f) * 2 * Math.PI / g) + d + c }, easeInBack: function (a, b, c, d, e, f) { return void 0 == f && (f = 1.70158), d * (b /= e) * b * ((f + 1) * b - f) + c }, easeOutBack: function (a, b, c, d, e, f) { return void 0 == f && (f = 1.70158), d * ((b = b / e - 1) * b * ((f + 1) * b + f) + 1) + c }, easeInOutBack: function (a, b, c, d, e, f) { return void 0 == f && (f = 1.70158), (b /= e / 2) < 1 ? d / 2 * b * b * (((f *= 1.525) + 1) * b - f) + c : d / 2 * ((b -= 2) * b * (((f *= 1.525) + 1) * b + f) + 2) + c }, easeInBounce: function (a, b, c, d, e) { return d - jQuery.easing.easeOutBounce(a, e - b, 0, d, e) + c }, easeOutBounce: function (a, b, c, d, e) { return (b /= e) < 1 / 2.75 ? d * 7.5625 * b * b + c : 2 / 2.75 > b ? d * (7.5625 * (b -= 1.5 / 2.75) * b + .75) + c : 2.5 / 2.75 > b ? d * (7.5625 * (b -= 2.25 / 2.75) * b + .9375) + c : d * (7.5625 * (b -= 2.625 / 2.75) * b + .984375) + c }, easeInOutBounce: function (a, b, c, d, e) { return e / 2 > b ? .5 * jQuery.easing.easeInBounce(a, 2 * b, 0, d, e) + c : .5 * jQuery.easing.easeOutBounce(a, 2 * b - e, 0, d, e) + .5 * d + c } });

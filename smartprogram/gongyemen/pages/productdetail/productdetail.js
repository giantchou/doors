var requests = require('../../utils/requests.js');
var encryption = require('../../utils/util.js');
var setTKD = require('../../utils/tkd.js');
var bdParse = require('../../utils/bdParse/bdParse.js');
Page({
    data: {
        data: {
            toView: 'view4',
            scrollTop: 100,
            windowsheight:'',
            productinfo:{}
        },
    },
    onLoad: function (option) {
        // 监听页面加载的生命周期函数
        console.log(option)
        var pid = option.pid;
        var that = this;
        var params = encryption.encryption();
        params['pid']=pid;
        requests.requests.get(params,'product/detail/',function(data){
            console.log(data)
            var content = data.data.content;
            that.setData('productinfo',data.data);
            that.setData({ content:bdParse.bdParse('article', 'html', content, that, 5), })
            swan.setNavigationBarTitle({
                title: data.data.title
            });
            setTKD.setTKD(data.data.title,data.data.abstract,data.data.keyword);
        });

        
    },
    onReady: function() {
        // 监听页面初次渲染完成的生命周期函数
    },
    onShow: function() {
        // 监听页面显示的生命周期函数
    },
    onHide: function() {
        // 监听页面隐藏的生命周期函数
    },
    onUnload: function() {
        // 监听页面卸载的生命周期函数
    },
    onPullDownRefresh: function() {
        // 监听用户下拉动作
    },
    onReachBottom: function() {
        // 页面上拉触底事件的处理函数
    },
    onShareAppMessage: function () {
        // 用户点击右上角转发
    },
});
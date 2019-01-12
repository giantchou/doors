var requests = require('../../utils/requests.js');
var encryption = require('../../utils/util.js');
var page=1;
var cate='';
Page({
    data: {
        catelist:[
            {id:'',name:'热销',css:'row-view-this'},
            {id:'10',name:'悬浮门',css:''},
            {id:'2',name:'伸缩门',css:''},
            {id:'4',name:'旋转门',css:''},
            {id:'3',name:'别墅门',css:''},
            {id:'9',name:'感应门',css:''},
            {id:'11',name:'刷卡门',css:''},
        ],
        products:[
        ]
    },
    onLoad: function () {
        // 监听页面加载的生命周期函数 
        var params = encryption.encryption();
        var that=this;
        console.log(params);
        params['cate1']=cate;
        requests.requests.get(params,'product/',function(data){
            console.log(data)
            that.setData('products',data.data)
        });
    },
    onReady: function() {
        // 监听页面初次渲染完成的生命周期函数
        this.setData();
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
    toLeft() {
        // swan.showToast({
        //     duration: 1000,
        //     title: '到最左边了'
        // });
    },
    toRight() {
        swan.showToast({
            duration: 1000,
            title: '到最右边了'
        });
    },
    upper() {
        swan.showToast({
            duration: 1000,
            title: '到顶了'
        });
    },

    lower() {
        // swan.showToast({
        //     duration: 1000,
        //     title: '到底了'
        // });
        page=page+1;
        var that =this;
        var params = encryption.encryption();
        params['cate1']=cate;
        params['page']=page;
        requests.requests.get(params,'product/',function(data){
            console.log(data)
            that.setData('products',data.data)
        })
    },

    myscroll(e) {
        console.log('获取滚动事件的详细信息e.detail：' + e.detail);
        console.dir(e.detail);
    },
    goToCate(e){
        var that=this;
        var catelist = this.data.catelist;
        var cid = e.currentTarget.dataset.swan;
        cate=cid;
        for(var i=0;i<catelist.length;i++){
            if(cid ==catelist[i].id ){
                catelist[i].css = "row-view-this"
            }else{
                catelist[i].css = ""
            }
        }
        that.setData('catelist',catelist)
        var params = encryption.encryption();
        params['cate1']=cate;
        requests.requests.get(params,'product/',function(data){
            console.log(data)
            that.setData('products',data.data)
        });
    },
    goToProductDetail(e){
        var pid = e.currentTarget.dataset.swan;
        swan.navigateTo({
            url:'/pages/productdetail/productdetail?pid='+pid
        })
    },
});
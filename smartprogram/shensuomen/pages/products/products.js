
Page({
    data: {
        catelist:[
            {id:'1',name:'热销',css:'row-view-this'},
            {id:'2',name:'平移门',css:''},
            {id:'3',name:'伸缩门',css:''},
            {id:'4',name:'旋转门',css:''},
            {id:'5',name:'别墅门',css:''}
        ],
        productexample:[
            {pid:"33",name:"别墅庭院大门-T006",image:"https://upyun.doors360.cn/image_upload/1544659058_61.jpg"},
            {pid:"18",name:"悬浮折叠门-F007",image:"https://upyun.doors360.cn/image_upload/1544632349_73.jpg"},
            {pid:"420",name:"钢化玻璃感应门B",image:"https://upyun.doors360.cn/image_upload/B1122534912767.jpg"},
            {pid:"50",name:"mini两翼旋转门",image:"https://upyun.doors360.cn/image_upload/1544664122_58.jpg"},
            {pid:"430",name:"侧小门(爱心型)JY-C1703",image:"https://upyun.doors360.cn/image_upload/C1703.jpg"},
            {pid:"2",name:"电动伸缩门 宝莱斯顿-10",image:"https://upyun.doors360.cn/image_upload/1544632110_3.jpg"},
            {pid:"424",name:"小区声障",image:"https://upyun.doors360.cn/image_upload/xiaoqu_shengzhang.jpeg"},
            {pid:"422",name:"小区电动刷卡门",image:"https://upyun.doors360.cn/image_upload/2018-12-20_23_50.jpg"}
        ]
    },
    onLoad: function () {
        // 监听页面加载的生命周期函数 
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
        swan.showToast({
            duration: 1000,
            title: '到最左边了'
        });
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
        swan.showToast({
            duration: 1000,
            title: '到底了'
        });
    },

    myscroll(e) {
        console.log('获取滚动事件的详细信息e.detail：' + e.detail);
        console.dir(e.detail);
    },
    goToCate(e){
        var catelist = this.data.catelist;
        var cid = e.currentTarget.dataset.swan;
        for(var i=0;i<catelist.length;i++){
            if(cid ==catelist[i].id ){
                catelist[i].css = "row-view-this"
            }else{
                catelist[i].css = ""
            }
        }
        this.setData('catelist',catelist)

    },
    goToProductDetail(e){
        swan.navigateTo({
            url:'/pages/productdetail/productdetail'
        })
    },
});
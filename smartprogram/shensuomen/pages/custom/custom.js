
Page({
    data: {
        catelist:[
            {id:'1',name:'分类A',css:'row-view-this'},
            {id:'2',name:'分类B',css:''},
            {id:'3',name:'分类C',css:''}
        ],
        productexample:[
            {pid:"1",name:"产品1",image:"../../images/example.jpeg"},
            {pid:"2",name:"产品2",image:"../../images/example.jpeg"},
            {pid:"3",name:"产品3",image:"../../images/example.jpeg"}
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
Page({
    data: {
        peopleindex: 1,
        typeindex: 1,
        BxPeople: ['铝合金','普通钢','不锈钢'],
        BxType:['立柱','百叶','菱格','方框','其他'],
        // regionData: ['全部', '全部', '全部'],
    },
    peopleChange(e) {
        console.log('picker-date changed，值为', e.detail.value);
        this.setData(
            // 'BxPeople', e.detail.value,
            'peopleindex',e.detail.value
        );
    },
    typeChange(e) {
        console.log('picker-date changed，值为', e.detail.value);
        this.setData(
            // 'BxPeople', e.detail.value,
            'typeindex',e.detail.value
        );
    },

    formSubmitHandle: function(e) {
      console.log('form表单submit：', e.detail.value);
      console.log('form表单submit：', e.detail.formId);
      var name = e.detail.value.bxname;
      var bxtel = e.detail.value.bxtel;
      var bxcity = e.detail.value.bxcity;
      if(!name){
        swan.showToast({
            title: '姓名不能忘了哦',
            icon: 'none',
            duration: 1000,
        });
      }
      if(!bxtel){
        swan.showToast({
            title: '电话是必填哦',
            icon: 'none',
            duration: 1000,
        });
      }
      var people = this.data.BxPeople[this.data.peopleindex];
      var bxtype = this.data.BxType[this.data.typeindex];
      if(name && bxtel){
        swan.request({
                url: 'https://m.doors360.cn/customization/', // 仅为示例，并非真实的接口地址
                method: 'POST',
                dataType: 'json',
                data: {
                    name: name,
                    tel: bxtel,
                    city: bxcity,
                    bxpeople: people,
                    bxtype: bxtype,
                },
                header: {
                    'content-type': 'application/json' // 默认值
                },
                success: function (res) {
                    console.log(res.data);
                    swan.showToast({
                        title: '定制成功哦',
                        icon: 'success',
                        duration: 1000,
                    });
                },
                fail: function (err) {
                    console.log('错误码：' + err.errCode);
                    console.log('错误信息：' + err.errMsg);
                }
            }); 
        }

    },
    onLoad: function () {
        // 监听页面加载的生命周期函数
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
    }
});
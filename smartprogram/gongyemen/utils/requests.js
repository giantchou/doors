var requests={
    get:function(kwargs,url,func){
            var data = {};
            swan.request({
            url:"https://m.doors360.cn/api/"+url, // 仅为示例，并非真实的接口地址
            method: 'GET',
            dataType: 'json',
            data: kwargs,
            header: {
                'content-type': 'application/json' // 默认值
            },
            success: function (res) {
                console.log("res=",res)
                data = res.data;
                func(data)
            },
            fail: function (err) {
                console.log('错误码：' + err.errCode);
                console.log('错误信息：' + err.errMsg);
            }
        });
    },
    post:function(kwargs,url,func){
            var data = {};
            swan.request({
            url:url, // 仅为示例，并非真实的接口地址
            method: 'POST',
            dataType: 'json',
            data: kwargs,
            header: {
                'content-type': 'application/json' // 默认值
            },
            success: function (res) {
                data = res.data;
                func(data)
            },
            fail: function (err) {
                console.log('错误码：' + err.errCode);
                console.log('错误信息：' + err.errMsg);
            }
        });
    },
}
// function requests (kwargs,url,method,func){
//             var data = {};
//             swan.request({
//             url:url, // 仅为示例，并非真实的接口地址
//             method: method,
//             dataType: 'json',
//             data: kwargs,
//             header: {
//                 'content-type': 'application/json' // 默认值
//             },
//             success: function (res) {
//                 data = res.data;
//                 func(data)
//             },
//             fail: function (err) {
//                 console.log('错误码：' + err.errCode);
//                 console.log('错误信息：' + err.errMsg);
//             }
//         });
        
// }
module.exports.requests = requests;
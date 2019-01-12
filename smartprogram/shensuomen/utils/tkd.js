
function setTKD(title,desc,keyword){
        //keyword='小程序, 关键字'
        var Title = '电动门,伸缩门,自动伸缩门,旋转门,车牌识别系统,河南伸缩门厂家';
        var Description = '金洋九峰15年专注电动门,伸缩门,电动伸缩门,伸缩门厂家,电动门厂家,电动伸缩门厂家,设计研发,产品全工序制造,品质层层把控,值得信赖,为企业提供一站式门道系统解决方案.';
        var Keyword = '电动门,伸缩门,电动伸缩门,河南电动门,河南伸缩门,河南电动伸缩门,伸缩门厂家,电动门厂家,电动伸缩门厂家';
        if(!title){
            title = Title
        }
        if(!desc){
            desc = Description
        }
        if(!keyword){
            keyword = Keyword
        }
        swan.setDocumentTitle && swan.setDocumentTitle({
            title: title
        });
        swan.setMetaKeywords && swan.setMetaKeywords({
            content: keyword,
            success: function (res) {
                console.log('设置keyword成功');
            },
            fail: function (res) {
                console.log('设置keyword失败');
            },
            complete: function (res) {
                console.log('设置keyword失败');
            }
        });
        swan.setMetaDescription && swan.setMetaDescription({
            content: desc,
            success: function (res) {
                console.log('设置desc成功');
            },
            fail: function (res) {
                console.log('设置desc失败');
            },
            complete: function (res) {
                console.log('设置desc失败');
            }
        });
}
module.exports.setTKD = setTKD;
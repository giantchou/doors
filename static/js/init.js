 layui.use(['jquery','carousel','form','layer'], function(){
    var element = layui.element,
        form = layui.form,
        layur = layui.layer,
   carousel = layui.carousel;
   $(".page-next").on("click",function () {
            var page = Number($('.page-location').html())+Number(1);
            window.location.href = "/products/?page="+page;
        })
      //建造实例
      //图片轮播
      carousel.render({
        elem: '#test10'
        ,width: '100%'
        ,height: '300px'
        ,interval: 3000
      });
      carousel.render({
        elem: '#test11'
        ,width: '100%'
        ,height: '420px'
        ,arrow: 'always'
        ,interval: 3000
      });
 //监听提交
  form.on('submit(formDemo)', function(data){
    $.ajax({
        url:"/buyuser",
        type:"post",
        dataType: "json",
        data:data.field,
        success:function (result) {
            alert(result);
            layer.msg(result.msg,{time:2000});
            if(result.code==0){
                setTimeout(function () {
                    $("#zaixian_liuyan").css("display","none");
                },2000);
            }
        }

    });
    return false;
  });

});
//*******init*********
 (function () {
    $.getJSON("/api/cate/",function (data) {
        $.each(data.data,function (i,d) {
            $('.cate-container').append('<div class="layui-col-xs12">\n' +
                '            <a href="/'+d[0]+'"><span class="layui-badge-dot"></span>&nbsp;'+d[1]+'</a>\n' +
                '        </div>')
        })
    })
 })();
$(".new-products").on("click",function () {
    $(this).addClass("this");
    $("#new-products").css("display",'block');
    $(".hot-products").removeClass("this");
    $("#hot-products").css("display",'none');
});
$(".hot-products").on("click",function () {
    $(this).addClass("this");
    $("#hot-products").css("display",'block');
    $(".new-products").removeClass("this");
    $("#new-products").css("display",'none');
});
    // 点击按钮，返回顶部
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}
function zaixianliuyan() {
    var liuyan=document.getElementById("zaixian_liuyan");
    liuyan.style.display="block";
}
function closeDiv() {
    var liuyan=document.getElementById("zaixian_liuyan");
    liuyan.style.display="none";
}
function zhedie() {
  $("#chc-cate").animate({right:"0%"});
  $(".layui-fluid").css("background-color","#000000").css("opacity","0.2");
  $(".chc-cate").css("opacity","1.0");
}

// document.addEventListener("click", function(e){
//      // 判断被点击的元素是不是scheduleInput元素，不是的话，就隐藏之
//     var cateleft = document.getElementById("zhedieid");
//     console.log(e.target);
//      if( e.target !== cateleft ){
//            $("#chc-cate").animate({right:"-59%"});
//      }
// });
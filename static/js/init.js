 layui.use(['jquery','carousel'], function(){
    var element = layui.element,
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


});


$("#homesubmitform").on("click",function () {
    alert("sssss")
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
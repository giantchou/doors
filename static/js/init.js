 layui.use('jquery', function(){
   $ = layui.jquery;
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
document.addEventListener("click", function(e){
     // 判断被点击的元素是不是scheduleInput元素，不是的话，就隐藏之
    var cateleft = document.getElementById("zhedieid");
    console.log(e.target);
     if( e.target !== cateleft ){
           $("#chc-cate").animate({right:"-59%"});
     }
});

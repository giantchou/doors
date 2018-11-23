















if(typeof doyoo=='undefined' || !doyoo){
var d_genId=function(){
var id ='',ids='0123456789abcdef';
for(var i=0;i<32;i++){ id+=ids.charAt(Math.floor(Math.random()*16)); } return id;
};

var schema='http';
if(location.href.indexOf('https:') == 0){
	schema = 'https';
}
var doyoo={
env:{
secure:schema=='https',
mon:schema+'://m2423.talk99.cn/monitor',
chat:schema+'://chat2431.talk99.cn/chat',
file:schema+'://yun-static.soperson.com/131221',
compId:10039707,
confId:10063404,
workDomain:'',
vId:d_genId(),
lang:'',
fixFlash:0,
fixMobileScale:1,
subComp:13377,
_mark:'f1c744ffdc95edd9548b889eeddd76eebeb0cec7e3b015095ecc71a31278ca434250854864edf844'
},
chat:{
mobileColor:'',
mobileHeight:80,
mobileChatHintBottom:0,
mobileChatHintMode:0,
mobileChatHintColor:'',
mobileChatHintSize:0,
priorMiniChat:0
}

, monParam:{
index:-1,
preferConfig:1,

style:{mbg:'http://a.looyu.com/20000202/2674fadf33ee400bb35de5ba15122d7e.png',mh:180,mw:360,
elepos:'0 0 0 0 0 0 0 0 78 10 110 50 180 10 110 50 0 0 0 0',
mbabg:'',
mbdbg:'',
mbpbg:''},

title:'',
text:'',
auto:5,
group:'10063943',
start:'00:00',
end:'24:00',
mask:false,
status:false,
fx:0,
mini:1,
pos:0,
offShow:1,
loop:15,
autoHide:0,
hidePanel:0,
miniStyle:'#0680b2',
miniWidth:'340',
miniHeight:'490',
showPhone:0,
monHideStatus:[4,5,5],
monShowOnly:'',
autoDirectChat:3,
allowMobileDirect:1,
minBallon:0,
chatFollow:1,
backCloseChat:1,
ratio:0
}


, panelParam:{
mobileIcon:'',
mobileIconWidth:0,
mobileIconHeight:0,
category:'icon',
preferConfig:0,
position:1,
vertical:120,
horizon:5


,mode:1,
target:'10063943',
online:'http://a.looyu.com/20000202/295a631055f54cc1b9b8c17fecf75250.jpg',
offline:'http://a.looyu.com/20000202/295a631055f54cc1b9b8c17fecf75250.jpg',
width:136,
height:407,
status:0,
closable:0,
regions:[],
collapse:0



}



};

if(typeof talk99Init == 'function'){
talk99Init(doyoo);
}
if(!document.getElementById('doyoo_panel')){
var supportJquery=typeof jQuery!='undefined';
var doyooWrite=function(html){
document.writeln(html);
}

doyooWrite('<div id="doyoo_panel"></div>');


doyooWrite('<div id="doyoo_monitor"></div>');


doyooWrite('<div id="talk99_message"></div>')

doyooWrite('<div id="doyoo_share" style="display:none;"></div>');
doyooWrite('<lin'+'k rel="stylesheet" type="text/css" href="'+schema+'://yun-static.soperson.com/131221/oms.css?171107"></li'+'nk>');
doyooWrite('<scr'+'ipt type="text/javascript" src="'+schema+'://yun-static.soperson.com/131221/oms.js?181102" charset="utf-8"></scr'+'ipt>');
}
}

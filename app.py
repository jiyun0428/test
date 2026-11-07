
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="THE LAST WARD",
    page_icon="👻",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #050507;
    color: white;
}
header, footer, #MainMenu {
    visibility: hidden;
}
.block-container {
    padding: 1rem;
    max-width: 1400px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style="text-align:center;color:#b90020;
letter-spacing:8px;text-shadow:0 0 20px red">
THE LAST WARD
</h1>
<p style="text-align:center;color:#aaa">
마지막 병동 · HORROR SURVIVAL
</p>
""", unsafe_allow_html=True)

game = r"""
<!DOCTYPE html>
<html>
<head>
<style>
* {box-sizing:border-box}
body {
 margin:0;
 background:#050507;
 color:white;
 font-family:Arial;
 overflow:hidden;
}
#wrap {
 position:relative;
 width:100%;
 height:620px;
 background:#000;
 overflow:hidden;
 border:1px solid #79101b;
}
canvas {
 width:100%;
 height:100%;
 display:block;
 cursor:crosshair;
}
#hud {
 position:absolute;
 inset:0;
 pointer-events:none;
 padding:15px;
}
#top {
 display:flex;
 justify-content:space-between;
 font-size:13px;
}
.stat {
 background:#000b;
 border:1px solid #722;
 padding:10px;
}
#message {
 position:absolute;
 bottom:25px;
 left:50%;
 transform:translateX(-50%);
 background:#000c;
 padding:12px 20px;
 text-align:center;
}
#overlay {
 position:absolute;
 inset:0;
 background:#050507ee;
 display:flex;
 align-items:center;
 justify-content:center;
 text-align:center;
 z-index:5;
}
.panel {
 max-width:500px;
 padding:20px;
}
.panel h1 {
 color:#d00027;
 letter-spacing:5px;
 text-shadow:0 0 20px red;
}
button {
 background:#570011;
 color:white;
 border:1px solid red;
 padding:15px 30px;
 font-size:18px;
 cursor:pointer;
}
#scare {
 display:none;
 position:absolute;
 inset:0;
 z-index:4;
 align-items:center;
 justify-content:center;
 font-size:150px;
 background:#6005;
 text-shadow:0 0 30px red;
}
</style>
</head>
<body>

<div id="wrap">
<canvas id="screen"></canvas>

<div id="hud">
 <div id="top">
  <div class="stat">
   ❤️ 체력 <span id="health">100</span>%
  </div>
  <div class="stat">
   🔦 배터리 <span id="battery">100</span>%
  </div>
  <div class="stat" id="objective">열쇠 찾기</div>
 </div>
 <div id="message">주변을 살펴보세요...</div>
</div>

<div id="scare">👹</div>

<div id="overlay">
 <div class="panel">
  <h1>THE LAST WARD</h1>
  <h2>마지막 병동</h2>
  <p>
   새벽 3시 17분.<br>
   당신은 버려진 병원에서 깨어났다.<br>
   출구는 잠겨 있고 누군가 당신을 지켜보고 있다.
  </p>
  <p style="color:#ff4444">
   ⚠️ 어둠 속에 오래 머물지 마세요.
  </p>
  <button id="start">게임 시작</button>
 </div>
</div>
</div>

<script>
const canvas=document.getElementById("screen");
const ctx=canvas.getContext("2d");
const wrap=document.getElementById("wrap");

let W=800,H=620;

function resize(){
 W=wrap.clientWidth;
 H=wrap.clientHeight;
 canvas.width=W;
 canvas.height=H;
}
resize();
window.addEventListener("resize",resize);

const map=[
"############",
"#..........#",
"#.##..#....#",
"#......#...#",
"#.##...#...#",
"#......#...#",
"###.##.....#",
"#..........#",
"#.####..##.#",
"#..........#",
"#..........#",
"############"
];

let p={
 x:1.5,y:1.5,angle:0,
 health:100,battery:100,
 flashlight:true,hasKey:false
};

let key={x:9.5,y:9.5,found:false};
let door={x:6.5,y:10.5};

let monster={
 x:9.5,y:2.5,active:false
};

let started=false,dead=false,won=false;
let last=performance.now();
let fear=0,shake=0;
const pressed={};

function wall(x,y){
 let a=Math.floor(x),b=Math.floor(y);
 return !map[b]||map[b][a]!=="." ;
}

function dist(x,y,a,b){
 return Math.hypot(x-a,y-b);
}

function say(t){
 document.getElementById("message").textContent=t;
}

document.getElementById("start").onclick=()=>{
 started=true;
 document.getElementById("overlay").style.display="none";
 canvas.requestPointerLock?.();
 say("WASD로 이동하고 열쇠를 찾으세요.");
 last=performance.now();
 requestAnimationFrame(loop);
};

canvas.addEventListener("click",()=>{
 if(started&&!dead&&!won)
  canvas.requestPointerLock?.();
});

document.addEventListener("mousemove",e=>{
 if(document.pointerLockElement===canvas)
  p.angle+=e.movementX*.0025;
});

document.addEventListener("keydown",e=>{
 pressed[e.code]=true;

 if(e.code==="KeyF"){
  p.flashlight=!p.flashlight;
  say(p.flashlight?"손전등 ON":"손전등 OFF");
 }

 if(e.code==="KeyE") interact();
});

document.addEventListener("keyup",e=>{
 pressed[e.code]=false;
});

function move(dx,dy){
 if(!wall(p.x+dx,p.y))p.x+=dx;
 if(!wall(p.x,p.y+dy))p.y+=dy;
}

function interact(){
 if(!key.found&&dist(p.x,p.y,key.x,key.y)<1.5){
  key.found=true;
  p.hasKey=true;
  monster.active=true;
  say("열쇠를 획득했다! 무언가 깨어났다!");
  shake=15;
  return;
 }

 if(dist(p.x,p.y,door.x,door.y)<1.5){
  if(p.hasKey){
   won=true;
   ending("탈출 성공","당신은 병원을 탈출했다...");
  }else{
   say("문이 잠겨 있다. 열쇠가 필요하다.");
  }
  return;
 }

 say("아무것도 없다.");
}

function ending(title,desc){
 document.exitPointerLock?.();
 let o=document.getElementById("overlay");
 o.style.display="flex";
 o.innerHTML=`
 <div class="panel">
 <h1>${title}</h1>
 <p>${desc}</p>
 <button onclick="location.reload()">다시 시작</button>
 </div>`;
}

function scare(){
 let el=document.getElementById("scare");
 el.style.display="flex";
 shake=25;
 setTimeout(()=>el.style.display="none",700);
}

function updateMonster(dt){
 if(!monster.active)return;

 let d=dist(p.x,p.y,monster.x,monster.y);

 if(d>.7){
  let dx=(p.x-monster.x)/d;
  let dy=(p.y-monster.y)/d;
  let speed=.6*dt;
  if(!wall(monster.x+dx*speed,monster.y))
   monster.x+=dx*speed;
  if(!wall(monster.x,monster.y+dy*speed))
   monster.y+=dy*speed;
 }

 fear=d<4?Math.min(100,fear+dt*20):
 Math.max(0,fear-dt*8);

 if(d<1.1){
  p.health-=dt*35;
  if(Math.random()<dt*2)scare();
 }

 if(p.health<=0){
  dead=true;
  ending("GAME OVER","괴물에게 붙잡혔다.");
 }
}

function render(){
 ctx.fillStyle="#09080d";
 ctx.fillRect(0,0,W,H/2);

 let floor=ctx.createLinearGradient(0,H/2,0,H);
 floor.addColorStop(0,"#28222b");
 floor.addColorStop(1,"#050507");
 ctx.fillStyle=floor;
 ctx.fillRect(0,H/2,W,H/2);

 const rays=240;
 let z=[];

 for(let i=0;i<rays;i++){
  let camera=(i/rays-.5)*1.15;
  let angle=p.angle+camera;
  let dx=Math.cos(angle),dy=Math.sin(angle);
  let d=0,x,y,hit=false;

  while(d<15&&!hit){
   d+=.025;
   x=p.x+dx*d;
   y=p.y+dy*d;
   if(wall(x,y))hit=true;
  }

  d*=Math.cos(camera);
  z[i]=d;

  let height=Math.min(H*2,H/(d||.1)*.78);
  let top=H/2-height/2;
  let light=p.flashlight?
   Math.max(.12,1-d/10)*Math.max(.15,1-Math.abs(camera)*1.5):
   .12;

  let red=Math.floor(45*light);
  let green=Math.floor(45*light);
  let blue=Math.floor(53*light);

  ctx.fillStyle=`rgb(${red},${green},${blue})`;
  ctx.fillRect(i*W/rays,top,W/rays+1,height);
 }

 function sprite(x,y,emoji,size,color){
  let dx=x-p.x,dy=y-p.y;
  let d=Math.hypot(dx,dy);
  let a=Math.atan2(dy,dx)-p.angle;
  while(a>Math.PI)a-=Math.PI*2;
  while(a< -Math.PI)a+=Math.PI*2;
  if(Math.abs(a)>.8||d<.1)return;

  let sx=W/2+Math.tan(a)*W*.82;
  let h=Math.min(H*1.5,H/d*.75*size);
  let col=Math.floor(sx/W*rays);
  if(col>=0&&col<rays&&d>z[col]+.1)return;

  ctx.save();
  ctx.textAlign="center";
  ctx.font=h+"px serif";
  ctx.shadowBlur=25;
  ctx.shadowColor=color;
  ctx.fillText(emoji,sx,H/2+h*.35);
  ctx.restore();
 }

 if(!key.found)sprite(key.x,key.y,"🔑",.5,"gold");
 sprite(door.x,door.y,"🚪",.7,"red");

 if(monster.active)
  sprite(monster.x,monster.y,"👹",1.2,"red");

 // 손전등 조명
 if(p.flashlight){
  let g=ctx.createRadialGradient(
   W/2,H/2,20,W/2,H/2,W*.55
  );
  g.addColorStop(0,"transparent");
  g.addColorStop(1,"rgba(0,0,0,.8)");
  ctx.fillStyle=g;
  ctx.fillRect(0,0,W,H);
 }else{
  ctx.fillStyle="rgba(0,0,0,.8)";
  ctx.fillRect(0,0,W,H);
 }

 if(fear>0){
  ctx.fillStyle=`rgba(130,0,0,${fear/500})`;
  ctx.fillRect(0,0,W,H);
 }
}

function loop(now){
 if(!started||dead||won)return;

 let dt=Math.min((now-last)/1000,.05);
 last=now;

 let speed=(pressed.ShiftLeft?2.8:1.7)*dt;
 let f=0,s=0;

 if(pressed.KeyW)f++;
 if(pressed.KeyS)f--;
 if(pressed.KeyA)s--;
 if(pressed.KeyD)s++;

 if(pressed.ArrowLeft)p.angle-=dt*1.8;
 if(pressed.ArrowRight)p.angle+=dt*1.8;

 let len=Math.hypot(f,s)||1;
 f/=len;s/=len;

 move(
  (Math.cos(p.angle)*f+
   Math.cos(p.angle+Math.PI/2)*s)*speed,
  (Math.sin(p.angle)*f+
   Math.sin(p.angle+Math.PI/2)*s)*speed
 );

 if(p.flashlight){
  p.battery=Math.max(0,p.battery-dt*.5);
  if(p.battery===0){
   p.flashlight=false;
   say("손전등 배터리가 방전되었다!");
  }
 }else{
  p.battery=Math.min(100,p.battery+dt*.1);
 }

 updateMonster(dt);

 ctx.save();
 if(shake>0){
  ctx.translate(
   (Math.random()-.5)*shake,
   (Math.random()-.5)*shake
  );
  shake=Math.max(0,shake-.5);
 }

 render();
 ctx.restore();

 document.getElementById("health").textContent=
  Math.floor(p.health);
 document.getElementById("battery").textContent=
  Math.floor(p.battery);
 document.getElementById("objective").textContent=
  p.hasKey?"출구로 이동":"열쇠 찾기";

 requestAnimationFrame(loop);
}

// 초기 화면
ctx.fillStyle="#080609";
ctx.fillRect(0,0,W,H);
ctx.fillStyle="#9c1528";
ctx.textAlign="center";
ctx.font="bold 24px Arial";
ctx.fillText("ABANDONED HOSPITAL",W/2,H/2);

</script>
</body>
</html>
"""

components.html(game, height=660, scrolling=False)

st.markdown("""
<p style="text-align:center;color:#777">
WASD 이동 · 마우스 시점 · SHIFT 달리기 · F 손전등 · E 상호작용
</p>
""", unsafe_allow_html=True)


import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ABANDONED HOSPITAL",
    page_icon="👻",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #08080d;
    color: white;
}
header, footer, #MainMenu {
    visibility: hidden;
}
.block-container {
    max-width: 1200px;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style="
text-align:center;
color:#d00027;
letter-spacing:5px;
text-shadow:0 0 20px red;">
👻 ABANDONED HOSPITAL
</h1>
<p style="text-align:center;color:#aaa;">
버려진 병원에서 살아남으세요.
</p>
""", unsafe_allow_html=True)

game = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {box-sizing:border-box}
body {
    margin:0;
    background:#08080d;
    color:white;
    font-family:Arial,sans-serif;
}
#game {
    position:relative;
    width:100%;
    max-width:900px;
    margin:auto;
}
canvas {
    display:block;
    width:100%;
    background:#09090d;
    border:2px solid #65111b;
    cursor:crosshair;
    outline:none;
    touch-action:none;
}
#hud {
    display:flex;
    justify-content:space-between;
    gap:8px;
    padding:10px;
    background:#160b12;
    font-size:13px;
    flex-wrap:wrap;
}
.stat {
    padding:8px;
    border:1px solid #55202a;
}
#overlay {
    position:absolute;
    inset:0;
    background:#000e;
    display:flex;
    align-items:center;
    justify-content:center;
    text-align:center;
    z-index:5;
    padding:15px;
}
.panel {
    max-width:450px;
}
.panel h1 {
    color:#e00030;
    text-shadow:0 0 20px red;
    letter-spacing:4px;
}
button {
    padding:14px 28px;
    color:white;
    background:#650018;
    border:1px solid #ff304c;
    font-size:17px;
    cursor:pointer;
}
button:hover {
    background:#a00025;
    box-shadow:0 0 20px red;
}
#message {
    text-align:center;
    color:#ff6666;
    min-height:25px;
    padding:8px;
}
#help {
    text-align:center;
    color:#999;
    font-size:12px;
    padding:10px;
    line-height:2;
}
</style>
</head>

<body>

<div id="game">

<div id="hud">
    <div class="stat">❤️ 체력: <span id="hp">100</span>%</div>
    <div class="stat">🔦 배터리: <span id="battery">100</span>%</div>
    <div class="stat">🔑 열쇠: <span id="keyStatus">없음</span></div>
    <div class="stat">👹 괴물: <span id="monsterStatus">대기 중</span></div>
</div>

<canvas id="canvas" width="900" height="620"
tabindex="0"></canvas>

<div id="message">병원에서 탈출하세요...</div>

<div id="overlay">
    <div class="panel">
        <h1>ABANDONED HOSPITAL</h1>
        <h3>버려진 병원</h3>
        <p>
            당신은 폐병원에 갇혔습니다.<br>
            병원 어딘가에 출구 열쇠가 있습니다.<br>
            하지만 이곳에는 당신 외에 다른 존재가 있습니다.
        </p>
        <p style="color:#ff5555">
            괴물을 조심하세요.
        </p>
        <button id="start">게임 시작</button>
    </div>
</div>

</div>

<div id="help">
    W : 위로 이동　 A : 왼쪽 이동<br>
    S : 아래로 이동　 D : 오른쪽 이동<br>
    SHIFT : 달리기　 F : 손전등 켜기/끄기<br>
    E : 주변 물건 조사하기<br>
    게임 화면을 한 번 클릭한 후 키보드를 사용하세요.
</div>

<script>
const canvas=document.getElementById("canvas");
const ctx=canvas.getContext("2d");

const TILE=60;
const COLS=15;
const ROWS=10;

const map=[
"###############",
"#.............#",
"#..##.........#",
"#..##..###....#",
"#......#......#",
"#.####.#.##...#",
"#......#......#",
"#..###........#",
"#.............#",
"###############"
];

let player={
    x:1.5*TILE,
    y:1.5*TILE,
    size:23,
    hp:100,
    battery:100,
    flashlight:true,
    hasKey:false
};

let monster={
    x:12.5*TILE,
    y:1.5*TILE,
    active:false,
    speed:55
};

const key={
    x:12.5*TILE,
    y:7.5*TILE,
    found:false
};

const exit={
    x:7.5*TILE,
    y:8.5*TILE
};

let started=false;
let gameOver=false;
let won=false;
let last=performance.now();
let shake=0;
let fear=0;
let flicker=0;
let messageTimer=0;

const pressed={};

function say(text) {
    document.getElementById("message").textContent=text;
    messageTimer=performance.now()+2500;
}

function wallAt(x,y) {
    const c=Math.floor(x/TILE);
    const r=Math.floor(y/TILE);

    return r<0 || c<0 ||
        r>=ROWS || c>=COLS ||
        map[r][c]==="#";
}

function distance(a,b,c,d) {
    return Math.hypot(a-c,b-d);
}

function collides(x,y) {
    const s=player.size/2;

    return wallAt(x-s,y-s) ||
           wallAt(x+s,y-s) ||
           wallAt(x-s,y+s) ||
           wallAt(x+s,y+s);
}

function movePlayer(dx,dy) {
    if(!collides(player.x+dx,player.y))
        player.x+=dx;

    if(!collides(player.x,player.y+dy))
        player.y+=dy;
}

function startGame() {
    if(started)return;

    started=true;
    document.getElementById("overlay").style.display="none";
    canvas.focus();
    last=performance.now();
    say("열쇠를 찾아 출구로 가세요.");
    requestAnimationFrame(loop);
}

document.getElementById("start")
.addEventListener("click",startGame);

canvas.addEventListener("click",()=>{
    canvas.focus();
});

document.addEventListener("keydown",e=>{
    if(["KeyW","KeyA","KeyS","KeyD",
        "ArrowUp","ArrowDown","ArrowLeft","ArrowRight",
        "Space"].includes(e.code)) {
        e.preventDefault();
    }

    pressed[e.code]=true;

    if(!started || gameOver || won)return;

    if(e.repeat)return;

    if(e.code==="KeyF") {
        player.flashlight=!player.flashlight;
        say(player.flashlight?
            "손전등을 켰습니다.":"손전등을 껐습니다.");
    }

    if(e.code==="KeyE") interact();
});

document.addEventListener("keyup",e=>{
    pressed[e.code]=false;
});

function interact() {
    if(!key.found &&
       distance(player.x,player.y,key.x,key.y)<65) {

        key.found=true;
        player.hasKey=true;
        monster.active=true;
        say("열쇠를 획득했다! 괴물이 깨어났다!");
        shake=10;
        return;
    }

    if(distance(player.x,player.y,exit.x,exit.y)<65) {
        if(player.hasKey) {
            won=true;
            ending("ESCAPE SUCCESS",
            "당신은 병원에서 탈출했습니다. 정말 끝난 것일까요?");
        } else {
            say("출구가 잠겨 있다. 열쇠가 필요하다.");
        }
        return;
    }

    say("주변에 조사할 물건이 없습니다.");
}

function ending(title,text) {
    document.getElementById("overlay").style.display="flex";

    document.getElementById("overlay").innerHTML=`
        <div class="panel">
            <h1>${title}</h1>
            <p>${text}</p>
            <button onclick="location.reload()">다시 시작</button>
        </div>
    `;
}

function drawMap() {
    for(let r=0;r<ROWS;r++) {
        for(let c=0;c<COLS;c++) {
            const x=c*TILE;
            const y=r*TILE;

            if(map[r][c]==="#") {
                ctx.fillStyle="#29262b";
                ctx.fillRect(x,y,TILE,TILE);

                ctx.strokeStyle="#443a40";
                ctx.strokeRect(x,y,TILE,TILE);

                // 벽의 낡은 얼룩
                ctx.fillStyle="#38252b";
                ctx.fillRect(x+8,y+12,4,20);
            } else {
                ctx.fillStyle="#17151a";
                ctx.fillRect(x,y,TILE,TILE);

                ctx.strokeStyle="#242027";
                ctx.strokeRect(x,y,TILE,TILE);

                // 바닥의 타일
                ctx.fillStyle="#211c23";
                ctx.fillRect(x+2,y+2,2,2);
            }
        }
    }

    // 병원 침대
    drawBed(3*TILE,1*TILE);
    drawBed(3*TILE,6*TILE);
    drawBed(9*TILE,5*TILE);

    // 책상
    ctx.fillStyle="#49332e";
    ctx.fillRect(10*TILE+8,2*TILE+8,40,35);
}

function drawBed(x,y) {
    ctx.fillStyle="#4d4147";
    ctx.fillRect(x+7,y+9,44,38);

    ctx.fillStyle="#b2a5a6";
    ctx.fillRect(x+11,y+13,36,12);

    ctx.fillStyle="#292027";
    ctx.fillRect(x+8,y+38,5,8);
    ctx.fillRect(x+46,y+38,5,8);
}

function drawObjects() {
    // 열쇠
    if(!key.found) {
        ctx.save();
        ctx.shadowBlur=20;
        ctx.shadowColor="#ffdd00";
        ctx.fillStyle="#ffe600";
        ctx.font="32px Arial";
        ctx.textAlign="center";
        ctx.fillText("🔑",key.x,key.y+10);
        ctx.restore();
    }

    // 출구
    ctx.fillStyle=player.hasKey?"#276b40":"#6b202b";
    ctx.fillRect(exit.x-20,exit.y-25,40,50);

    ctx.fillStyle="#ddd";
    ctx.fillRect(exit.x+10,exit.y,5,5);
    ctx.fillStyle="white";
    ctx.font="11px Arial";
    ctx.textAlign="center";
    ctx.fillText("EXIT",exit.x,exit.y-32);
}

function drawMonster() {
    if(!monster.active)return;

    ctx.save();
    ctx.shadowBlur=25;
    ctx.shadowColor="red";
    ctx.fillStyle="#b00017";

    ctx.beginPath();
    ctx.arc(monster.x,monster.y,20,0,Math.PI*2);
    ctx.fill();

    ctx.fillStyle="white";
    ctx.beginPath();
    ctx.arc(monster.x-7,monster.y-5,4,0,Math.PI*2);
    ctx.arc(monster.x+7,monster.y-5,4,0,Math.PI*2);
    ctx.fill();

    ctx.fillStyle="black";
    ctx.fillRect(monster.x-8,monster.y+7,16,4);

    ctx.restore();
}

function drawPlayer() {
    // 그림자
    ctx.fillStyle="#000";
    ctx.beginPath();
    ctx.ellipse(player.x+3,player.y+8,15,9,0,0,Math.PI*2);
    ctx.fill();

    // 플레이어
    ctx.fillStyle="#4c8ed9";
    ctx.beginPath();
    ctx.arc(player.x,player.y,player.size/2,0,Math.PI*2);
    ctx.fill();

    ctx.fillStyle="#f3d3ba";
    ctx.beginPath();
    ctx.arc(player.x,player.y-3,7,0,Math.PI*2);
    ctx.fill();

    // 바라보는 방향
    ctx.strokeStyle="#ffe9a0";
    ctx.lineWidth=3;
    ctx.beginPath();
    ctx.moveTo(player.x,player.y);
    ctx.lineTo(player.x,player.y-16);
    ctx.stroke();
}

function drawLighting() {
    const radius=player.flashlight?175:75;

    const gradient=ctx.createRadialGradient(
        player.x,player.y,15,
        player.x,player.y,radius
    );

    gradient.addColorStop(0,"rgba(255,235,180,0.35)");
    gradient.addColorStop(.45,"rgba(220,210,180,0.13)");
    gradient.addColorStop(1,"rgba(0,0,0,0)");

    ctx.fillStyle="rgba(0,0,0,.91)";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    ctx.globalCompositeOperation="destination-out";

    const hole=ctx.createRadialGradient(
        player.x,player.y,8,
        player.x,player.y,radius
    );

    hole.addColorStop(0,"rgba(0,0,0,1)");
    hole.addColorStop(.65,"rgba(0,0,0,.9)");
    hole.addColorStop(1,"rgba(0,0,0,0)");

    ctx.fillStyle=hole;
    ctx.beginPath();
    ctx.arc(player.x,player.y,radius,0,Math.PI*2);
    ctx.fill();

    ctx.globalCompositeOperation="source-over";

    if(!player.flashlight) {
        ctx.fillStyle="rgba(0,0,0,.2)";
        ctx.fillRect(0,0,canvas.width,canvas.height);
    }

    if(fear>0) {
        ctx.fillStyle=`rgba(120,0,0,${fear/450})`;
        ctx.fillRect(0,0,canvas.width,canvas.height);
    }

    if(flicker>0) {
        ctx.fillStyle=`rgba(0,0,0,${flicker})`;
        ctx.fillRect(0,0,canvas.width,canvas.height);
    }
}

function updateMonster(dt) {
    if(!monster.active)return;

    const d=distance(
        player.x,player.y,
        monster.x,monster.y
    );

    if(d>25) {
        const dx=(player.x-monster.x)/d;
        const dy=(player.y-monster.y)/d;

        const speed=monster.speed*dt;

        let nx=monster.x+dx*speed;
        let ny=monster.y+dy*speed;

        if(!wallAt(nx,monster.y))monster.x=nx;
        if(!wallAt(monster.x,ny))monster.y=ny;
    }

    if(d<160) {
        fear=Math.min(100,fear+dt*25);
    } else {
        fear=Math.max(0,fear-dt*10);
    }

    if(d<27) {
        player.hp-=dt*35;
        shake=5;

        if(player.hp<=0) {
            player.hp=0;
            gameOver=true;
            ending("GAME OVER","괴물에게 붙잡혔습니다.");
        }
    }
}

function updateHUD() {
    document.getElementById("hp").textContent=
        Math.floor(player.hp);

    document.getElementById("battery").textContent=
        Math.floor(player.battery);

    document.getElementById("keyStatus").textContent=
        player.hasKey?"보유":"없음";

    document.getElementById("monsterStatus").textContent=
        monster.active?"추격 중":"대기 중";
}

function render() {
    ctx.clearRect(0,0,canvas.width,canvas.height);

    ctx.save();

    if(shake>0) {
        ctx.translate(
            (Math.random()-.5)*shake,
            (Math.random()-.5)*shake
        );
        shake=Math.max(0,shake-.4);
    }

    drawMap();
    drawObjects();
    drawMonster();
    drawPlayer();
    drawLighting();

    ctx.restore();
}

function update(dt) {
    let speed=(pressed.ShiftLeft||pressed.ShiftRight)?150:95;
    speed*=dt;

    let dx=0,dy=0;

    if(pressed.KeyW||pressed.ArrowUp)dy--;
    if(pressed.KeyS||pressed.ArrowDown)dy++;
    if(pressed.KeyA||pressed.ArrowLeft)dx--;
    if(pressed.KeyD||pressed.ArrowRight)dx++;

    const len=Math.hypot(dx,dy)||1;
    dx/=len;
    dy/=len;

    const oldX=player.x;
    const oldY=player.y;

    const nx=player.x+dx*speed;
    const ny=player.y+dy*speed;

    if(!collides(nx,player.y))player.x=nx;
    if(!collides(player.x,ny))player.y=ny;

    function collides(x,y) {
        const r=player.size/2-3;

        return wallAt(x-r,y-r)||
               wallAt(x+r,y-r)||
               wallAt(x-r,y+r)||
               wallAt(x+r,y+r);
    }

    const moving=(oldX!==player.x||oldY!==player.y);

    if(player.flashlight) {
        player.battery=Math.max(0,player.battery-dt*.55);

        if(player.battery===0) {
            player.flashlight=false;
            say("손전등 배터리가 방전되었습니다!");
        }
    } else {
        player.battery=Math.min(100,player.battery+dt*.15);
    }

    if(moving && (pressed.ShiftLeft||pressed.ShiftRight)) {
        player.battery=Math.max(0,player.battery-dt*.1);
    }

    updateMonster(dt);

    if(Math.random()<dt*.6) {
        flicker=Math.random()*.15;
    } else {
        flicker=Math.max(0,flicker-dt);
    }

    updateHUD();

    if(messageTimer && performance.now()>messageTimer) {
        say("병원에서 탈출하세요...");
        messageTimer=0;
    }
}

function loop(now) {
    if(!started||gameOver||won)return;

    const dt=Math.min((now-last)/1000,.05);
    last=now;

    update(dt);
    render();

    requestAnimationFrame(loop);
}

// 최초 게임 화면
render();

</script>
</body>
</html>
"""

components.html(game, height=760, scrolling=False)

st.caption(
    "ABANDONED HOSPITAL | WASD 이동 · SHIFT 달리기 · "
    "F 손전등 · E 조사"
)

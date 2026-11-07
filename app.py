
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="THE HAUNTED HOUSE",
    page_icon="👹",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #08070a;
    color: white;
}
header, footer, #MainMenu {
    visibility: hidden;
}
.block-container {
    padding: 1rem;
    max-width: 1100px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style="text-align:center;color:#38a9ff;
text-shadow:0 0 20px #006aff;letter-spacing:5px;">
THE HAUNTED HOUSE
</h1>
<p style="text-align:center;color:#aaa;">
그 집 · 2D SURVIVAL HORROR
</p>
""", unsafe_allow_html=True)

game = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { box-sizing:border-box; }

body {
    margin:0;
    background:#08070a;
    color:white;
    font-family:Arial,sans-serif;
    overflow:hidden;
}

#game {
    width:100%;
    max-width:900px;
    margin:auto;
    position:relative;
}

#hud {
    display:flex;
    justify-content:space-between;
    flex-wrap:wrap;
    gap:6px;
    padding:10px;
    background:#15121a;
    border:1px solid #38303d;
    font-size:13px;
}

.stat {
    padding:7px 12px;
    background:#241d29;
    border:1px solid #493c4b;
}

canvas {
    display:block;
    width:100%;
    height:auto;
    background:#111;
    border:2px solid #44333f;
    image-rendering:pixelated;
    outline:none;
}

#message {
    text-align:center;
    padding:10px;
    min-height:35px;
    color:#9ecfff;
    background:#100d13;
}

#overlay {
    position:absolute;
    inset:0;
    z-index:10;
    background:rgba(0,0,0,.94);
    display:flex;
    justify-content:center;
    align-items:center;
    text-align:center;
    padding:20px;
}

.panel {
    max-width:500px;
}

.panel h1 {
    color:#36aaff;
    text-shadow:0 0 20px #006aff;
    letter-spacing:4px;
}

button {
    padding:14px 32px;
    background:#07518b;
    border:1px solid #42aaff;
    color:white;
    font-size:17px;
    cursor:pointer;
}

button:hover {
    background:#0878c5;
}

#controls {
    text-align:center;
    padding:10px;
    font-size:12px;
    color:#999;
    line-height:2;
}
</style>
</head>

<body>

<div id="game">

    <div id="hud">
        <div class="stat">❤️ 체력: <span id="hp">100</span></div>
        <div class="stat">🔑 열쇠: <span id="keys">0</span></div>
        <div class="stat">👹 괴물: <span id="enemy">잠복 중</span></div>
        <div class="stat">📍 위치: <span id="location">거실</span></div>
    </div>

    <canvas id="canvas" width="900" height="600"></canvas>

    <div id="message">이 집에서 탈출해야 한다...</div>

    <div id="overlay">
        <div class="panel">
            <h1>THE HAUNTED HOUSE</h1>
            <h2>그 집</h2>
            <p>
                당신은 낯선 저택에서 눈을 떴다.<br>
                현관문은 잠겨 있다.<br>
                어딘가에서 이상한 발소리가 들린다.
            </p>
            <p style="color:#64baff;">
                파란 괴물에게 잡히지 말고 탈출하세요.
            </p>
            <button id="start">게임 시작</button>
        </div>
    </div>

</div>

<div id="controls">
    W A S D : 이동　
    SHIFT : 달리기　
    E : 조사 / 문 열기　
    SPACE : 숨기
</div>

<script>
(function() {

"use strict";

// ==================================
// 1. 게임 기본 설정
// ==================================

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const WIDTH = 900;
const HEIGHT = 600;
const TILE = 60;

const COLS = 15;
const ROWS = 10;

// # 벽 / . 바닥
const map = [
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

// ==================================
// 2. 플레이어 설정
// ==================================

const player = {
    x: 90,
    y: 90,
    radius: 13,
    speed: 145,
    hp: 100,
    keys: 0,
    hidden: false,
    hasKey: false
};

// ==================================
// 3. 파란 괴물 설정
// ==================================

const monster = {
    x: 780,
    y: 150,
    speed: 75,
    active: false,
    attackDistance: 28,
    direction: 0
};

// ==================================
// 4. 게임 오브젝트
// ==================================

const objects = {
    key: {
        x: 750,
        y: 450,
        found: false
    },

    note: {
        x: 690,
        y: 270,
        found: false
    },

    exit: {
        x: 450,
        y: 510,
        open: false
    }
};

// ==================================
// 5. 게임 상태
// ==================================

let started = false;
let gameOver = false;
let victory = false;

let lastTime = 0;
let shake = 0;
let fear = 0;

const keys = {};

let currentMessage = "이 집에서 탈출해야 한다.";

// ==================================
// 6. 벽 충돌 확인
// ==================================

function isWall(x, y) {

    const col = Math.floor(x / TILE);
    const row = Math.floor(y / TILE);

    if (
        row < 0 ||
        col < 0 ||
        row >= ROWS ||
        col >= COLS
    ) {
        return true;
    }

    return map[row][col] === "#";
}

function canMove(x, y) {

    const r = player.radius;

    return !(
        isWall(x-r,y-r) ||
        isWall(x+r,y-r) ||
        isWall(x-r,y+r) ||
        isWall(x+r,y+r)
    );
}

function distance(x1,y1,x2,y2) {
    return Math.hypot(x1-x2,y1-y2);
}

// ==================================
// 7. 메시지 표시
// ==================================

function say(text) {
    currentMessage = text;

    document.getElementById("message")
        .textContent = text;
}

// ==================================
// 8. 맵 그리기
// ==================================

function drawMap() {

    for(let r=0; r<ROWS; r++) {

        for(let c=0; c<COLS; c++) {

            const x = c*TILE;
            const y = r*TILE;

            if(map[r][c] === "#") {

                // 벽
                ctx.fillStyle = "#463b3b";
                ctx.fillRect(x,y,TILE,TILE);

                ctx.fillStyle = "#574748";
                ctx.fillRect(x+4,y+4,52,52);

                ctx.strokeStyle = "#292127";
                ctx.strokeRect(x,y,TILE,TILE);

                // 벽 장식
                ctx.fillStyle = "#382d31";
                ctx.fillRect(x+10,y+12,40,4);

            } else {

                // 바닥
                ctx.fillStyle = "#29242a";
                ctx.fillRect(x,y,TILE,TILE);

                ctx.strokeStyle = "#373039";
                ctx.strokeRect(x,y,TILE,TILE);

                // 낡은 나무 바닥
                ctx.fillStyle = "#332a2d";
                ctx.fillRect(x+8,y+8,40,2);
                ctx.fillRect(x+8,y+35,40,2);
            }
        }
    }

    // 카펫
    ctx.fillStyle = "#653038";
    ctx.fillRect(65,65,120,100);

    ctx.strokeStyle = "#a65b61";
    ctx.strokeRect(70,70,110,90);

    // 소파
    ctx.fillStyle = "#67464c";
    ctx.fillRect(230,70,110,45);

    ctx.fillStyle = "#91676c";
    ctx.fillRect(240,77,90,25);

    // 식탁
    ctx.fillStyle = "#63442f";
    ctx.fillRect(550,75,100,65);

    ctx.fillStyle = "#9a7050";
    ctx.fillRect(560,85,80,45);

    // 침대
    drawBed(550,330);
    drawBed(120,390);

    // 책장
    ctx.fillStyle = "#583b2e";
    ctx.fillRect(350,390,100,45);

    ctx.fillStyle = "#a77b50";

    for(let i=0;i<4;i++) {
        ctx.fillRect(360+i*20,395,12,30);
    }
}

// ==================================
// 9. 침대 그리기
// ==================================

function drawBed(x,y) {

    ctx.fillStyle = "#4d3d42";
    ctx.fillRect(x,y,95,55);

    ctx.fillStyle = "#d1c3bd";
    ctx.fillRect(x+7,y+7,81,18);

    ctx.fillStyle = "#65535a";
    ctx.fillRect(x+7,y+28,81,20);

    ctx.fillStyle = "#2c242a";
    ctx.fillRect(x,y+50,10,8);
    ctx.fillRect(x+85,y+50,10,8);
}

// ==================================
// 10. 플레이어 그리기
// ==================================

function drawPlayer() {

    if(player.hidden) return;

    // 그림자
    ctx.fillStyle = "#111";
    ctx.beginPath();
    ctx.ellipse(
        player.x+3,
        player.y+9,
        14,8,0,0,Math.PI*2
    );
    ctx.fill();

    // 몸
    ctx.fillStyle = "#426a9d";
    ctx.fillRect(
        player.x-10,
        player.y-5,
        20,
        20
    );

    // 머리
    ctx.fillStyle = "#e1bba1";
    ctx.fillRect(
        player.x-9,
        player.y-17,
        18,
        16
    );

    // 머리카락
    ctx.fillStyle = "#34252a";
    ctx.fillRect(
        player.x-10,
        player.y-19,
        20,
        6
    );

    // 눈
    ctx.fillStyle = "#222";
    ctx.fillRect(player.x-5,player.y-11,3,3);
    ctx.fillRect(player.x+3,player.y-11,3,3);
}

// ==================================
// 11. 파란 괴물 그리기
// ==================================

function drawMonster() {

    if(!monster.active) return;

    const x = monster.x;
    const y = monster.y;

    ctx.save();

    ctx.shadowBlur = 18;
    ctx.shadowColor = "#008cff";

    // 몸
    ctx.fillStyle = "#145bba";
    ctx.fillRect(x-16,y-5,32,35);

    // 머리
    ctx.fillStyle = "#2379d9";
    ctx.fillRect(x-19,y-31,38,30);

    // 얼굴
    ctx.fillStyle = "#0b244a";
    ctx.fillRect(x-13,y-20,26,10);

    // 눈
    ctx.fillStyle = "#ff3030";
    ctx.fillRect(x-11,y-18,6,6);
    ctx.fillRect(x+5,y-18,6,6);

    // 입
    ctx.fillStyle = "#160d19";
    ctx.fillRect(x-8,y-4,16,5);

    // 이빨
    ctx.fillStyle = "white";
    ctx.fillRect(x-5,y-4,3,4);
    ctx.fillRect(x+3,y-4,3,4);

    // 팔
    ctx.fillStyle = "#164c99";
    ctx.fillRect(x-24,y+2,9,23);
    ctx.fillRect(x+15,y+2,9,23);

    // 다리
    ctx.fillStyle = "#102e6b";
    ctx.fillRect(x-13,y+28,10,15);
    ctx.fillRect(x+3,y+28,10,15);

    ctx.restore();
}

// ==================================
// 12. 게임 오브젝트 그리기
// ==================================

function drawObjects() {

    // 열쇠
    if(!objects.key.found) {

        ctx.font = "30px Arial";
        ctx.textAlign = "center";

        ctx.fillText(
            "🔑",
            objects.key.x,
            objects.key.y+10
        );
    }

    // 쪽지
    if(!objects.note.found) {

        ctx.fillStyle = "#eee3c5";
        ctx.fillRect(
            objects.note.x-12,
            objects.note.y-9,
            24,18
        );

        ctx.fillStyle = "#4a2525";
        ctx.fillRect(
            objects.note.x-7,
            objects.note.y-3,
            14,2
        );
    }

    // 출구
    ctx.fillStyle = objects.exit.open ?
        "#238d54" : "#743039";

    ctx.fillRect(
        objects.exit.x-25,
        objects.exit.y-25,
        50,50
    );

    ctx.fillStyle = "#e6d2aa";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    ctx.fillText(
        "EXIT",
        objects.exit.x,
        objects.exit.y+5
    );
}



// ==================================
// 13. 키보드 입력
// ==================================

const pressed = {};

document.addEventListener("keydown", function(e) {

    const k = e.code;

    if([
        "KeyW","KeyA","KeyS","KeyD",
        "ShiftLeft","ShiftRight","Space"
    ].includes(k)) {
        e.preventDefault();
    }

    pressed[k] = true;

    if(!started || gameOver || victory || e.repeat) return;

    if(k === "KeyE") interact();

    if(k === "Space") hidePlayer();
});

document.addEventListener("keyup", function(e) {
    pressed[e.code] = false;
});

// ==================================
// 14. 숨을 수 있는 옷장
// ==================================

const closets = [
    {x:240,y:180},
    {x:690,y:350},
    {x:300,y:480}
];

function drawClosets() {

    closets.forEach(c => {

        ctx.fillStyle = "#513327";
        ctx.fillRect(c.x-17,c.y-25,34,50);

        ctx.fillStyle = "#80533c";
        ctx.fillRect(c.x-13,c.y-21,26,42);

        ctx.fillStyle = "#e3b76c";
        ctx.fillRect(c.x+7,c.y-3,3,6);

    });
}

function hidePlayer() {

    if(player.hidden) {

        player.hidden = false;
        say("옷장에서 나왔습니다.");

        return;
    }

    const closet = closets.find(c =>
        distance(player.x,player.y,c.x,c.y) < 55
    );

    if(!closet) {
        say("근처에 숨을 수 있는 옷장이 없습니다.");
        return;
    }

    player.hidden = true;

    say("옷장에 숨었습니다. 괴물이 지나가길 기다리세요.");
}

// ==================================
// 15. 상호작용
// ==================================

function interact() {

    // 열쇠 획득
    if(
        !objects.key.found &&
        distance(
            player.x,player.y,
            objects.key.x,objects.key.y
        ) < 55
    ) {

        objects.key.found = true;
        player.hasKey = true;
        player.keys = 1;

        monster.active = true;

        say("열쇠를 획득했다! 어딘가에서 괴성이 들린다!");

        shake = 10;

        return;
    }

    // 쪽지 획득
    if(
        !objects.note.found &&
        distance(
            player.x,player.y,
            objects.note.x,objects.note.y
        ) < 55
    ) {

        objects.note.found = true;

        player.hasCode = true;

        say("쪽지를 발견했다! 비밀번호는 2714!");

        return;
    }

    // 출구
    if(
        distance(
            player.x,player.y,
            objects.exit.x,objects.exit.y
        ) < 65
    ) {

        if(player.hasKey && player.hasCode) {

            victory = true;

            endGame(
                "ESCAPE SUCCESS",
                "당신은 저택에서 탈출했습니다. 하지만 뒤에서 무언가가 당신을 바라보고 있습니다..."
            );

        } else if(!player.hasKey) {

            say("현관문이 잠겨 있다. 열쇠가 필요하다.");

        } else {

            say("비밀번호가 필요하다. 집 안에서 쪽지를 찾아라.");

        }

        return;
    }

    say("주변을 조사했지만 아무것도 발견하지 못했다.");
}

// ==================================
// 16. 플레이어 이동
// ==================================

function updatePlayer(dt) {

    if(player.hidden) return;

    let speed = player.speed;

    if(pressed.ShiftLeft || pressed.ShiftRight) {
        speed = 190;
    }

    let dx = 0;
    let dy = 0;

    if(pressed.KeyW) dy--;
    if(pressed.KeyS) dy++;
    if(pressed.KeyA) dx--;
    if(pressed.KeyD) dx++;

    const length = Math.hypot(dx,dy) || 1;

    dx = dx / length * speed * dt;
    dy = dy / length * speed * dt;

    if(canMove(player.x+dx,player.y)) {
        player.x += dx;
    }

    if(canMove(player.x,player.y+dy)) {
        player.y += dy;
    }
}

// ==================================
// 17. 괴물 AI
// ==================================

function updateMonster(dt) {

    if(!monster.active) return;

    const d = distance(
        player.x,player.y,
        monster.x,monster.y
    );

    // 숨지 않았다면 추격
    if(!player.hidden && d > 20) {

        const dx = (player.x-monster.x)/d;
        const dy = (player.y-monster.y)/d;

        const speed = monster.speed * dt;

        const nextX = monster.x + dx*speed;
        const nextY = monster.y + dy*speed;

        // 벽 충돌
        if(!isWall(nextX,monster.y)) {
            monster.x = nextX;
        }

        if(!isWall(monster.x,nextY)) {
            monster.y = nextY;
        }
    }

    // 괴물이 가까우면 공포 증가
    if(d < 200 && !player.hidden) {
        fear = Math.min(100,fear+dt*25);
    } else {
        fear = Math.max(0,fear-dt*15);
    }

    // 괴물 공격
    if(!player.hidden && d < monster.attackDistance) {

        player.hp -= dt*20;

        shake = 5;

        if(player.hp <= 0) {

            player.hp = 0;
            gameOver = true;

            endGame(
                "GAME OVER",
                "파란 괴물에게 붙잡혔습니다. 다시 도전하세요."
            );
        }
    }
}

// ==================================
// 18. 손전등과 어두운 시야
// ==================================

function drawLighting() {

    ctx.fillStyle = "rgba(0,0,0,0.91)";
    ctx.fillRect(0,0,WIDTH,HEIGHT);

    // 플레이어 주변 조명
    const radius = 185;

    const light = ctx.createRadialGradient(
        player.x,
        player.y,
        10,
        player.x,
        player.y,
        radius
    );

    light.addColorStop(0,"rgba(0,0,0,1)");
    light.addColorStop(0.45,"rgba(0,0,0,0.85)");
    light.addColorStop(1,"rgba(0,0,0,0)");

    ctx.globalCompositeOperation = "destination-out";

    ctx.fillStyle = light;

    ctx.beginPath();

    ctx.arc(
        player.x,
        player.y,
        radius,
        0,
        Math.PI*2
    );

    ctx.fill();

    ctx.globalCompositeOperation = "source-over";

    // 공포에 따른 붉은 효과
    if(fear > 0) {

        ctx.fillStyle = `rgba(100,0,0,${fear/650})`;

        ctx.fillRect(0,0,WIDTH,HEIGHT);
    }

    // 숨었을 때 어두워짐
    if(player.hidden) {

        ctx.fillStyle = "rgba(0,0,0,0.45)";
        ctx.fillRect(0,0,WIDTH,HEIGHT);
    }
}

// ==================================
// 19. 화면 흔들림
// ==================================

function drawGame() {

    ctx.clearRect(0,0,WIDTH,HEIGHT);

    ctx.save();

    if(shake > 0) {

        ctx.translate(
            (Math.random()-0.5)*shake,
            (Math.random()-0.5)*shake
        );

        shake = Math.max(0,shake-0.5);
    }

    drawMap();
    drawClosets();
    drawObjects();
    drawMonster();
    drawPlayer();

    drawLighting();

    ctx.restore();
}

// ==================================
// 20. HUD 업데이트
// ==================================

function updateHUD() {

    document.getElementById("hp").textContent =
        Math.max(0,Math.floor(player.hp));

    document.getElementById("keys").textContent =
        player.keys;

    document.getElementById("enemy").textContent =
        monster.active ? "추격 중" : "잠복 중";

    document.getElementById("location").textContent =
        player.y < 240 ? "거실" :
        player.y < 420 ? "복도" : "현관";
}

// ==================================
// 21. 엔딩
// ==================================

function endGame(title,description) {

    document.getElementById("overlay").style.display = "flex";

    document.getElementById("overlay").innerHTML = `
        <div class="panel">
            <h1>${title}</h1>
            <p>${description}</p>
            <button onclick="location.reload()">
                다시 플레이
            </button>
        </div>
    `;
}

// ==================================
// 22. 게임 메인 루프
// ==================================

function loop(now) {

    if(!started || gameOver || victory) return;

    const dt = Math.min((now-lastTime)/1000,0.05);

    lastTime = now;

    updatePlayer(dt);
    updateMonster(dt);

    updateHUD();
    drawGame();

    requestAnimationFrame(loop);
}

// ==================================
// 23. 게임 시작
// ==================================

document.getElementById("start").addEventListener("click",function() {

    if(started) return;

    started = true;

    document.getElementById("overlay").style.display = "none";

    say("WASD로 이동하세요. 열쇠를 찾아 탈출하세요!");

    canvas.focus();

    lastTime = performance.now();

    requestAnimationFrame(loop);

});

// ==================================
// 24. 최초 화면 렌더링
// ==================================

drawGame();

})();
</script>

<div style="
text-align:center;
padding:12px;
color:#888;
font-size:12px;
">
THE HAUNTED HOUSE · END
</div>

</body>
</html>
"""

# ==================================
# 25. Streamlit 게임 출력
# ==================================

components.html(
    game,
    height=760,
    scrolling=False
)


import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="공포게임 테스트",
    page_icon="👻",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #080808;
    color: white;
}
header, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

st.title("👻 ABANDONED HOSPITAL")
st.write("2D 공포게임 화면 테스트")

html = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    background: #080808;
    color: white;
    text-align: center;
    font-family: Arial;
}
canvas {
    background: #171717;
    border: 3px solid red;
    max-width: 100%;
}
button {
    background: darkred;
    color: white;
    padding: 15px 30px;
    border: 0;
    cursor: pointer;
    font-size: 18px;
}
</style>
</head>
<body>

<h2>폐병원 생존 게임</h2>

<canvas id="game" width="800" height="500"></canvas>

<p id="status">게임 준비 완료</p>

<button onclick="startGame()">게임 시작</button>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let x = 400;
let y = 250;
let started = false;

const keys = {};

document.addEventListener("keydown", e => {
    keys[e.key.toLowerCase()] = true;
});

document.addEventListener("keyup", e => {
    keys[e.key.toLowerCase()] = false;
});

function startGame() {
    started = true;
    document.getElementById("status").innerText =
        "WASD로 캐릭터를 움직이세요!";
    canvas.focus();
}

function draw() {
    ctx.fillStyle = "#171717";
    ctx.fillRect(0, 0, 800, 500);

    // 바닥 격자
    ctx.strokeStyle = "#292929";
    for(let i=0; i<800; i+=50) {
        ctx.beginPath();
        ctx.moveTo(i,0);
        ctx.lineTo(i,500);
        ctx.stroke();
    }

    for(let i=0; i<500; i+=50) {
        ctx.beginPath();
        ctx.moveTo(0,i);
        ctx.lineTo(800,i);
        ctx.stroke();
    }

    // 벽
    ctx.fillStyle = "#555";
    ctx.fillRect(0,0,800,20);
    ctx.fillRect(0,480,800,20);
    ctx.fillRect(0,0,20,500);
    ctx.fillRect(780,0,20,500);

    if(started) {
        if(keys["w"]) y -= 3;
        if(keys["s"]) y += 3;
        if(keys["a"]) x -= 3;
        if(keys["d"]) x += 3;

        x = Math.max(35, Math.min(765,x));
        y = Math.max(35, Math.min(465,y));
    }

    // 플레이어
    ctx.fillStyle = "#4b9cff";
    ctx.beginPath();
    ctx.arc(x,y,15,0,Math.PI*2);
    ctx.fill();

    // 괴물
    ctx.fillStyle = "#c00020";
    ctx.font = "35px Arial";
    ctx.fillText("👹",650,100);

    // 손전등 효과
    const light = ctx.createRadialGradient(
        x,y,10,x,y,160
    );
    light.addColorStop(0,"rgba(255,255,200,0.2)");
    light.addColorStop(1,"rgba(0,0,0,0)");

    ctx.fillStyle = light;
    ctx.fillRect(0,0,800,500);

    requestAnimationFrame(draw);
}

draw();
</script>

</body>
</html>
"""

components.html(html, height=650, scrolling=False)


import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(
    page_title="가위바위보 대결",
    page_icon="🥊",
    layout="wide"
)

# -----------------------------
# 세션 상태
# -----------------------------
defaults = {
    "win": 0,
    "lose": 0,
    "draw": 0,
    "player": "❔",
    "computer": "❔",
    "result": "대결을 시작하세요!",
    "has_played": False,
    "round": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# 디자인
# -----------------------------
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 50% 30%,
        #421078 0%, #18002f 55%, #080015 100%);
    color: white;
}

h1, h2, h3, p, label {
    color: white;
}

.game-title {
    text-align: center;
    font-size: 48px;
    font-weight: 1000;
    color: #ffe66d;
    text-shadow: 0 0 20px #ff00ff;
    padding: 15px;
}

div.stButton > button {
    height: 90px;
    width: 100%;
    border-radius: 22px;
    background: linear-gradient(135deg,#7b2cbf,#c77dff);
    border: 2px solid #ffffff;
    color: white;
    font-size: 25px;
    font-weight: bold;
    box-shadow: 0 0 18px #b517ff;
    transition: all .2s;
}

div.stButton > button:hover {
    transform: scale(1.07);
    background: linear-gradient(135deg,#ff006e,#8338ec);
    color: white;
    box-shadow: 0 0 35px #ff00ff;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="game-title">
    🥊 ROCK PAPER SCISSORS 🥊
</div>
<p style="text-align:center;font-size:20px;">
    최고의 승부를 시작하세요!
</p>
""", unsafe_allow_html=True)

# -----------------------------
# 점수판
# -----------------------------
a, b, c = st.columns(3)

a.metric("🏆 승리", st.session_state.win)
b.metric("💀 패배", st.session_state.lose)
c.metric("🤝 무승부", st.session_state.draw)

st.divider()

# -----------------------------
# 대결 함수
# -----------------------------
choices = {
    "가위": "✌️",
    "바위": "✊",
    "보": "✋"
}

def play(player):

    computer = random.choice(["가위", "바위", "보"])

    st.session_state.player = choices[player]
    st.session_state.computer = choices[computer]

    if player == computer:
        st.session_state.result = "🤝 DRAW!"
        st.session_state.draw += 1

    elif (
        (player == "가위" and computer == "보") or
        (player == "바위" and computer == "가위") or
        (player == "보" and computer == "바위")
    ):
        st.session_state.result = "🏆 YOU WIN!"
        st.session_state.win += 1

    else:
        st.session_state.result = "💀 YOU LOSE!"
        st.session_state.lose += 1

    st.session_state.has_played = True
    st.session_state.round += 1

# -----------------------------
# 대결 버튼
# -----------------------------
st.markdown(
    "<h2 style='text-align:center;'>👇 무엇을 낼까요?</h2>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✌️ 가위"):
        play("가위")
        st.rerun()

with col2:
    if st.button("✊ 바위"):
        play("바위")
        st.rerun()

with col3:
    if st.button("✋ 보"):
        play("보")
        st.rerun()

# -----------------------------
# 애니메이션 경기장
# -----------------------------
if st.session_state.has_played:

    player = st.session_state.player
    computer = st.session_state.computer
    result = st.session_state.result

    if "WIN" in result:
        result_color = "#ffe600"
        result_class = "win"
    elif "LOSE" in result:
        result_color = "#ff3155"
        result_class = "lose"
    else:
        result_color = "#65eaff"
        result_class = "draw"

    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    * { box-sizing: border-box; }

    body {
        margin: 0;
        background: transparent;
        font-family: Arial, sans-serif;
        color: white;
        overflow: hidden;
    }

    .arena {
        height: 490px;
        width: 100%;
        position: relative;
        overflow: hidden;
        border-radius: 25px;
        background:
        radial-gradient(ellipse at center,
        #542080 0%, #21063c 65%, #100020 100%);
        border: 2px solid #bd70ff;
        box-shadow: 0 0 30px #a020f0;
    }

    .arena.shake {
        animation: cameraShake .5s ease-in-out;
    }

    @keyframes cameraShake {
        0% { transform: translate(0,0) rotate(0); }
        15% { transform: translate(-12px,7px) rotate(-1deg); }
        30% { transform: translate(12px,-8px) rotate(1deg); }
        45% { transform: translate(-10px,5px); }
        60% { transform: translate(8px,-5px); }
        75% { transform: translate(-5px,3px); }
        100% { transform: translate(0,0); }
    }

    .heading {
        text-align: center;
        padding-top: 22px;
        font-size: 22px;
        font-weight: bold;
        color: #ffdf80;
    }

    .fighters {
        display: flex;
        justify-content: space-around;
        align-items: center;
        height: 230px;
    }

    .fighter {
        text-align: center;
        width: 45%;
    }

    .name {
        font-size: 19px;
        color: #e5c7ff;
        font-weight: bold;
    }

    .hand {
        font-size: 90px;
        display: inline-block;
        filter: drop-shadow(0 0 15px #ffccff);
        opacity: 0;
    }

    .left-hand.show {
        animation: punchLeft .8s cubic-bezier(.2,.8,.3,1) forwards;
    }

    .right-hand.show {
        animation: punchRight .8s cubic-bezier(.2,.8,.3,1) forwards;
    }

    @keyframes punchLeft {
        0% { opacity:0; transform:translateX(-180px) scale(.2) rotate(-50deg); }
        65% { opacity:1; transform:translateX(35px) scale(1.5) rotate(20deg); }
        85% { transform:translateX(-10px) scale(1.1); }
        100% { opacity:1; transform:translateX(0) scale(1); }
    }

    @keyframes punchRight {
        0% { opacity:0; transform:translateX(180px) scale(.2) rotate(50deg); }
        65% { opacity:1; transform:translateX(-35px) scale(1.5) rotate(-20deg); }
        85% { transform:translateX(10px) scale(1.1); }
        100% { opacity:1; transform:translateX(0) scale(1); }
    }

    .vs {
        position: absolute;
        left: 50%;
        top: 48%;
        transform: translate(-50%,-50%);
        font-size: 35px;
        font-weight: 1000;
        color: #ffe600;
        text-shadow: 0 0 20px #ff00ff;
    }

    .count {
        position: absolute;
        top: 43%;
        left: 50%;
        transform: translate(-50%,-50%);
        font-size: 65px;
        font-weight: 1000;
        color: #ffffff;
        text-shadow: 0 0 25px #ff00ff;
        z-index: 10;
    }

    .result {
        text-align: center;
        font-size: 37px;
        font-weight: 1000;
        margin-top: 8px;
        opacity: 0;
    }

    .result.show {
        animation: resultPop .7s ease forwards;
    }

    @keyframes resultPop {
        0% { opacity:0; transform:scale(.2) rotate(-10deg); }
        70% { opacity:1; transform:scale(1.25) rotate(3deg); }
        100% { opacity:1; transform:scale(1); }
    }

    .flash {
        position: absolute;
        inset: 0;
        background: white;
        opacity: 0;
        pointer-events: none;
        z-index: 20;
    }

    .flash.active {
        animation: flash .35s ease;
    }

    @keyframes flash {
        0% { opacity:0; }
        25% { opacity:.8; }
        100% { opacity:0; }
    }

    .particle {
        position: absolute;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        pointer-events: none;
        animation: burst 1s ease-out forwards;
    }

    @keyframes burst {
        from {
            opacity:1;
            transform:translate(0,0) scale(1);
        }
        to {
            opacity:0;
            transform:translate(var(--x),var(--y)) scale(0);
        }
    }

    </style>
    </head>

    <body>
    <div class="arena" id="arena">

        <div class="heading">
            ⚡ FINAL BATTLE ⚡
        </div>

        <div class="fighters">

            <div class="fighter">
                <div class="name">😎 YOU</div>
                <div class="hand left-hand" id="player">PLAYER</div>
            </div>

            <div class="fighter">
                <div class="name">🤖 COMPUTER</div>
                <div class="hand right-hand" id="computer">COMPUTER</div>
            </div>

        </div>

        <div class="vs">VS</div>

        <div class="count" id="count">READY!</div>

        <div class="flash" id="flash"></div>

        <div class="result" id="result">RESULT</div>

    </div>

    <script>
    const arena = document.getElementById("arena");
    const count = document.getElementById("count");
    const player = document.getElementById("player");
    const computer = document.getElementById("computer");
    const result = document.getElementById("result");
    const flash = document.getElementById("flash");

    const playerEmoji = "PLAYER_EMOJI";
    const computerEmoji = "COMPUTER_EMOJI";
    const resultText = "RESULT_TEXT";
    const resultColor = "RESULT_COLOR";

    function burst() {
        for (let i = 0; i < 55; i++) {
            const p = document.createElement("div");
            p.className = "particle";

            p.style.left = "50%";
            p.style.top = "48%";
            p.style.background =
                ["#fff000","#ff00cc","#00ffff","#ffffff"]
                [Math.floor(Math.random()*4)];

            p.style.boxShadow = "0 0 12px " + p.style.background;
            p.style.setProperty("--x",
                (Math.random()*400-200)+"px");
            p.style.setProperty("--y",
                (Math.random()*300-150)+"px");

            arena.appendChild(p);
            setTimeout(() => p.remove(), 1100);
        }
    }

    // 카운트다운과 손 내기
    async function battle() {

        for (const n of ["3", "2", "1", "가위! 바위! 보!"]) {
            count.textContent = n;
            count.animate([
                {transform:"translate(-50%,-50%) scale(.3)",opacity:0},
                {transform:"translate(-50%,-50%) scale(1.3)",opacity:1},
                {transform:"translate(-50%,-50%) scale(1)",opacity:1}
            ], {duration:380, fill:"forwards"});

            await new Promise(r => setTimeout(r, 650));
        }

        count.style.display = "none";

        player.textContent = playerEmoji;
        computer.textContent = computerEmoji;

        player.classList.add("show");
        computer.classList.add("show");

        setTimeout(() => {
            arena.classList.add("shake");
            flash.classList.add("active");
            burst();
        }, 400);

        setTimeout(() => {
            result.textContent = resultText;
            result.style.color = resultColor;
            result.classList.add("show");
        }, 1100);
    }

    battle();
    </script>
    </body>
    </html>
    """

    html = html.replace("PLAYER_EMOJI", player)
    html = html.replace("COMPUTER_EMOJI", computer)
    html = html.replace("RESULT_TEXT", result)
    html = html.replace("RESULT_COLOR", result_color)

    components.html(
        html,
        height=510,
        scrolling=False
    )

else:
    st.markdown("""
    <div style="
        text-align:center;
        padding:60px 10px;
        font-size:28px;
        color:#e5c7ff;">
        🥊<br><br>
        버튼을 누르면 대결이 시작됩니다!
        <br><br>
        READY? FIGHT!
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# 초기화
# -----------------------------
st.write("")

if st.button("🔄 점수 및 게임 초기화"):
    for key, value in defaults.items():
        st.session_state[key] = value
    st.rerun()

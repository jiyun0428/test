
import streamlit as st
import random

st.set_page_config(
    page_title="가위바위보 게임",
    page_icon="✊",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg, #10002b, #240046, #3c096c
    );
    color: white;
}
h1, h2, h3, p {
    color: white !important;
}
.game-title {
    text-align: center;
    font-size: 45px;
    font-weight: 900;
    color: #ffd700;
    padding: 25px;
}
.subtitle {
    text-align: center;
    font-size: 20px;
    color: #e0b0ff;
}
.choice {
    text-align: center;
    font-size: 65px;
}
.result {
    text-align: center;
    font-size: 35px;
    font-weight: bold;
    color: #ffd700;
    padding: 20px;
}
div.stButton > button {
    width: 100%;
    height: 110px;
    border-radius: 20px;
    border: 2px solid #d8b4fe;
    background: linear-gradient(135deg,#7b2cbf,#5a189a);
    color: white;
    font-size: 25px;
    font-weight: bold;
    transition: 0.2s;
}
div.stButton > button:hover {
    background: linear-gradient(135deg,#c77dff,#9d4edd);
    border-color: #ffd700;
    transform: scale(1.05);
    color: white;
}
</style>
""", unsafe_allow_html=True)

if "computer" not in st.session_state:
    st.session_state.computer = "❔"

if "player" not in st.session_state:
    st.session_state.player = "❔"

if "result" not in st.session_state:
    st.session_state.result = "게임을 시작해 보세요!"

if "win" not in st.session_state:
    st.session_state.win = 0
    st.session_state.lose = 0
    st.session_state.draw = 0

st.markdown("""
<div class="game-title">
    ✊ 가위바위보 게임 ✌️
</div>
<div class="subtitle">
    컴퓨터와 대결해 보세요!
</div>
""", unsafe_allow_html=True)

st.write("")

# 점수판
c1, c2, c3 = st.columns(3)

c1.metric("🏆 승리", st.session_state.win)
c2.metric("😢 패배", st.session_state.lose)
c3.metric("🤝 무승부", st.session_state.draw)

st.divider()

# 대결 화면
left, right = st.columns(2)

with left:
    st.markdown(
        "<div class='choice'>🤖</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h3 style='text-align:center'>컴퓨터</h3>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div class='choice'>{st.session_state.computer}</div>",
        unsafe_allow_html=True
    )

with right:
    st.markdown(
        "<div class='choice'>😎</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h3 style='text-align:center'>나</h3>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div class='choice'>{st.session_state.player}</div>",
        unsafe_allow_html=True
    )

st.write("")

st.markdown(
    "<h3 style='text-align:center'>👇 무엇을 내시겠습니까?</h3>",
    unsafe_allow_html=True
)

# 가위바위보 버튼
col1, col2, col3 = st.columns(3)

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
        st.session_state.result = "🤝 무승부!"
        st.session_state.draw += 1

    elif (
        (player == "가위" and computer == "보") or
        (player == "바위" and computer == "가위") or
        (player == "보" and computer == "바위")
    ):
        st.session_state.result = "🎉 승리했습니다!"
        st.session_state.win += 1
        st.balloons()

    else:
        st.session_state.result = "😭 패배했습니다!"
        st.session_state.lose += 1

with col1:
    if st.button("✌️ 가위"):
        play("가위")

with col2:
    if st.button("✊ 바위"):
        play("바위")

with col3:
    if st.button("✋ 보"):
        play("보")

st.write("")

st.markdown(
    f"<div class='result'>{st.session_state.result}</div>",
    unsafe_allow_html=True
)

# 다시 시작
if st.button("🔄 게임 초기화"):
    st.session_state.win = 0
    st.session_state.lose = 0
    st.session_state.draw = 0
    st.session_state.player = "❔"
    st.session_state.computer = "❔"
    st.session_state.result = "새로운 게임을 시작하세요!"
    st.rerun()

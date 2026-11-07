
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="환영합니다!",
    page_icon="🎆",
    layout="centered"
)

# 배경 및 CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg, #10002b, #240046, #3c096c, #10002b
    );
    color: white;
}
h1, h2, p {
    color: white !important;
}
.welcome {
    text-align: center;
    padding: 35px 10px;
}
.welcome h1 {
    font-size: 48px;
    background: linear-gradient(90deg,
        #ffdf00, #ff69b4, #00ffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.welcome p {
    font-size: 20px;
}
div.stButton > button {
    display: block;
    margin: auto;
    width: 240px;
    height: 65px;
    border-radius: 40px;
    border: 2px solid #ffdf00;
    background: linear-gradient(90deg, #ff006e, #8338ec);
    color: white;
    font-size: 24px;
    font-weight: bold;
    transition: 0.3s;
}
div.stButton > button:hover {
    transform: scale(1.1);
    border-color: white;
    color: white;
    box-shadow: 0 0 25px #ff00ff;
}
</style>
""", unsafe_allow_html=True)

# 메인 화면
st.markdown("""
<div class="welcome">
    <h1>✨ WELCOME! ✨</h1>
    <p>여러분을 진심으로 환영합니다!</p>
    <p>🎊 특별한 순간을 함께 시작해요 🎊</p>
</div>
""", unsafe_allow_html=True)

# 버튼
if st.button("🎆 들어가기 🎆"):

    st.markdown("""
    <div class="welcome">
        <h1>🎉 환영합니다!!! 🎉</h1>
        <p>여러분의 방문을 진심으로 환영합니다!</p>
        <h2>오늘도 행복한 하루 되세요 ❤️</h2>
    </div>
    """, unsafe_allow_html=True)

    # Streamlit 축하 효과
    st.balloons()

    # 화려한 폭죽 애니메이션
    components.html("""
    <canvas id="fireworks"
        style="position:fixed;top:0;left:0;
        width:100vw;height:100vh;
        pointer-events:none;z-index:999999;">
    </canvas>

    <script>
    const canvas = document.getElementById("fireworks");
    const ctx = canvas.getContext("2d");

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();

    let particles = [];

    const colors = [
        "#ff0055", "#ffcc00", "#00ffff",
        "#ff00ff", "#00ff66", "#ffffff",
        "#ff8800", "#aa00ff"
    ];

    function explode(x, y) {
        const color = colors[
            Math.floor(Math.random() * colors.length)
        ];

        for (let i = 0; i < 100; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 7 + 2;

            particles.push({
                x: x,
                y: y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                alpha: 1,
                color: color,
                size: Math.random() * 3 + 1
            });
        }
    }

    // 여러 위치에서 연속 폭죽 발사
    let count = 0;
    const timer = setInterval(() => {
        explode(
            Math.random() * canvas.width,
            Math.random() * canvas.height * 0.65
        );
        count++;

        if (count >= 15) clearInterval(timer);
    }, 180);

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach((p) => {
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.045;
            p.alpha -= 0.009;

            ctx.globalAlpha = Math.max(0, p.alpha);
            ctx.fillStyle = p.color;
            ctx.shadowBlur = 15;
            ctx.shadowColor = p.color;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        });

        particles = particles.filter(p => p.alpha > 0);

        ctx.globalAlpha = 1;
        ctx.shadowBlur = 0;

        requestAnimationFrame(animate);
    }

    animate();
    </script>
    """, height=600, scrolling=False)

else:
    st.markdown("""
    <p style="text-align:center;color:#ffccff;">
        💜 버튼을 누르면 화려한 축제가 시작됩니다! 💜
    </p>
    """, unsafe_allow_html=True)

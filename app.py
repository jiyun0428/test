
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="환영합니다!",
    page_icon="🎆",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,
        #09001f, #210044, #35005c, #09001f);
    color: white;
}

.welcome {
    text-align: center;
    padding: 25px 10px;
}

.welcome h1 {
    font-size: 55px;
    font-weight: 900;
    background: linear-gradient(
        90deg, #fff000, #ff55bb, #00ffff, #fff000
    );
    background-size: 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: rainbow 4s linear infinite;
}

@keyframes rainbow {
    to { background-position: 300%; }
}

.welcome p {
    font-size: 21px;
    color: white;
}

div.stButton > button {
    display: block;
    margin: auto;
    width: 260px;
    height: 70px;
    border-radius: 50px;
    border: 2px solid #ffdf00;
    background: linear-gradient(90deg, #ff006e, #8338ec);
    color: white;
    font-size: 25px;
    font-weight: bold;
    box-shadow: 0 0 20px #ff00ff;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.1);
    box-shadow: 0 0 40px #ff00ff;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="welcome">
    <h1>✨ WELCOME TO OUR WORLD ✨</h1>
    <p>여러분을 진심으로 환영합니다!</p>
    <p>🎊 오늘의 특별한 축제를 시작해 보세요! 🎊</p>
</div>
""", unsafe_allow_html=True)

if "entered" not in st.session_state:
    st.session_state.entered = False

if st.button("🎆 들어가기 🎆"):
    st.session_state.entered = True
    st.balloons()

if st.session_state.entered:

    st.markdown("""
    <div class="welcome">
        <h1>🎉 환영합니다!!! 🎉</h1>
        <p>여러분의 방문을 진심으로 환영합니다 ❤️</p>
        <p>🖱️ 화면을 클릭해 보세요! 폭죽이 터집니다!</p>
    </div>
    """, unsafe_allow_html=True)

    components.html("""
    <canvas id="sky"></canvas>

    <style>
    html, body {
        margin: 0;
        padding: 0;
        overflow: hidden;
        background: transparent;
    }

    #sky {
        display: block;
        width: 100%;
        height: 720px;
        cursor: crosshair;
        background: radial-gradient(
            ellipse at center,
            rgba(65, 0, 100, 0.18),
            rgba(5, 0, 25, 0.12)
        );
    }
    </style>

    <script>
    const canvas = document.getElementById("sky");
    const ctx = canvas.getContext("2d");

    let W, H;
    let particles = [];
    let rockets = [];
    let stars = [];

    function resize() {
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        W = canvas.clientWidth;
        H = canvas.clientHeight;

        canvas.width = W * dpr;
        canvas.height = H * dpr;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    resize();

    const colors = [
        "#ff004c", "#ffcc00", "#00ffff",
        "#ff00ff", "#00ff66", "#ffffff",
        "#ff8800", "#a855ff", "#ff77aa",
        "#66aaff", "#fff4c2"
    ];

    // 반짝이는 별 생성
    for (let i = 0; i < 120; i++) {
        stars.push({
            x: Math.random() * 1200,
            y: Math.random() * 720,
            size: Math.random() * 2 + 0.5,
            alpha: Math.random(),
            speed: Math.random() * 0.035 + 0.01
        });
    }

    // 폭죽 발사
    function launch(x, y) {
        const color = colors[
            Math.floor(Math.random() * colors.length)
        ];

        rockets.push({
            x: x,
            y: H + 10,
            targetY: y,
            vx: (Math.random() - 0.5) * 2,
            vy: -(Math.random() * 5 + 9),
            color: color,
            trail: []
        });
    }

    // 화려한 폭발
    function explode(x, y, color) {

        const count = 180;

        for (let i = 0; i < count; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 8 + 1;

            particles.push({
                x: x,
                y: y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                alpha: 1,
                decay: Math.random() * 0.009 + 0.006,
                color: Math.random() > 0.25
                    ? color
                    : colors[Math.floor(Math.random() * colors.length)],
                size: Math.random() * 3.5 + 1,
                gravity: 0.045,
                twinkle: Math.random() > 0.5
            });
        }

        // 중심부의 반짝이는 작은 별
        for (let i = 0; i < 35; i++) {
            particles.push({
                x: x,
                y: y,
                vx: (Math.random() - 0.5) * 13,
                vy: (Math.random() - 0.5) * 13,
                alpha: 1,
                decay: 0.025,
                color: "#ffffff",
                size: Math.random() * 3 + 1,
                gravity: 0.02,
                twinkle: true
            });
        }
    }

    // 클릭한 위치에 폭죽 여러 개
    canvas.addEventListener("click", (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        launch(x, y);
        launch(
            Math.max(20, Math.min(W - 20, x + 100)),
            Math.max(30, y - 100)
        );
        launch(
            Math.max(20, Math.min(W - 20, x - 100)),
            Math.max(30, y - 60)
        );
    });

    // 최초 입장 시 대형 폭죽 쇼
    let initialCount = 0;

    const initialShow = setInterval(() => {
        launch(
            Math.random() * W,
            Math.random() * H * 0.65 + 40
        );

        initialCount++;

        if (initialCount >= 18) {
            clearInterval(initialShow);
        }
    }, 220);

    // 애니메이션
    function animate() {

        ctx.clearRect(0, 0, W, H);

        // 별빛 반짝임
        stars.forEach(s => {
            s.alpha += s.speed;
            if (s.alpha > 1 || s.alpha < 0) {
                s.speed *= -1;
            }

            ctx.globalAlpha = Math.max(0, s.alpha);
            ctx.fillStyle = "#ffffff";
            ctx.shadowBlur = 8;
            ctx.shadowColor = "#ffffff";

            ctx.beginPath();
            ctx.arc(s.x % W, s.y % H, s.size, 0, Math.PI * 2);
            ctx.fill();
        });

        // 로켓 이동 및 폭발
        rockets.forEach((r, index) => {
            r.trail.push({x: r.x, y: r.y});

            if (r.trail.length > 8) {
                r.trail.shift();
            }

            r.x += r.vx;
            r.y += r.vy;
            r.vy += 0.13;

            ctx.beginPath();
            ctx.strokeStyle = r.color;
            ctx.lineWidth = 3;
            ctx.shadowBlur = 15;
            ctx.shadowColor = r.color;

            if (r.trail.length > 1) {
                ctx.moveTo(r.trail[0].x, r.trail[0].y);

                r.trail.forEach(t => {
                    ctx.lineTo(t.x, t.y);
                });

                ctx.stroke();
            }

            if (r.y <= r.targetY || r.vy >= 0) {
                explode(r.x, r.y, r.color);
                rockets.splice(index, 1);
            }
        });

        // 불꽃 입자와 반짝임
        particles.forEach((p, index) => {

            p.x += p.vx;
            p.y += p.vy;

            p.vx *= 0.985;
            p.vy *= 0.985;
            p.vy += p.gravity;

            p.alpha -= p.decay;

            ctx.globalAlpha = Math.max(0, p.alpha);

            // 반짝이는 효과
            const sparkle = p.twinkle
                ? (Math.random() > 0.5 ? 1 : 0.4)
                : 1;

            ctx.fillStyle = p.color;
            ctx.shadowBlur = 18;
            ctx.shadowColor = p.color;

            ctx.beginPath();
            ctx.arc(
                p.x, p.y,
                Math.max(0.2, p.size * sparkle),
                0, Math.PI * 2
            );
            ctx.fill();

            if (p.alpha <= 0) {
                particles.splice(index, 1);
            }
        });

        ctx.globalAlpha = 1;
        ctx.shadowBlur = 0;

        requestAnimationFrame(animate);
    }

    animate();

    // 창 크기 변경 대응
    window.addEventListener("resize", resize);

    </script>
    """, height=730, scrolling=False)

else:
    st.markdown("""
    <div class="welcome">
        <p>💜 아래 버튼을 눌러 축제를 시작하세요! 💜</p>
    </div>
    """, unsafe_allow_html=True)

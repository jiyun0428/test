import streamlit as st
from datetime import datetime, date, time as d_time
import time

# --- 페이지 설정 ---
st.set_page_config(
    page_title="스마트 학습 관리 앱",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 커스텀 CSS (모바일 최적화 및 깔끔한 UI 디자인) ---
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# --- 세션 상태 초기화 ---
if 'todos' not in st.session_state:
    st.session_state.todos = [
        {"id": 1, "title": "수학 수의 성질 3단원 풀기", "category": "수학", "importance": "중", "due_date": date.today(), "alert_time": "09:00", "completed": False},
        {"id": 2, "title": "영어 단어 50개 암기", "category": "영어", "importance": "상", "due_date": date.today(), "alert_time": "14:00", "completed": False}
    ]

if 'plans' not in st.session_state:
    st.session_state.plans = [
        {"id": 1, "time_slot": "09:00 ~ 10:30", "activity": "수학 수의 성질 3단원 풀기", "subject": "수학", "completed": False, "target_minutes": 90, "actual_minutes": 0, "todo_id": 1},
        {"id": 2, "time_slot": "11:00 ~ 12:00", "activity": "영어 단어 50개 암기", "subject": "영어", "completed": False, "target_minutes": 60, "actual_minutes": 0, "todo_id": 2}
    ]

if 'timer_state' not in st.session_state:
    st.session_state.timer_state = {
        "running": False,
        "subject": "선택 안됨",
        "activity": "",
        "start_timestamp": None,
        "accumulated_seconds": 0,  # 일시정지 등으로 쌓인 누적 초
        "plan_id": None
    }

if 'target_study_hours' not in st.session_state:
    st.session_state.target_study_hours = 6.0

# --- 타이틀 및 네비게이션 ---
st.title("📚 스터디 플래너 & 타임머신")
st.caption(f"오늘 날짜: {date.today().strftime('%Y년 %m월 %d일 (%A)')}")

menu = st.sidebar.radio(
    "📌 메뉴 선택",
    ["🏠 홈", "✅ 할 일", "📅 하루 계획표", "⏱️ 공부 타이머", "📊 학습 리포트"],
    index=0
)

# ==========================================
# 1. 홈 화면
# ==========================================
if menu == "🏠 홈":
    st.markdown("### 👋 오늘의 학습 요약")
    
    total_actual_mins = sum([p["actual_minutes"] for p in st.session_state.plans])
    total_actual_hours = total_actual_mins / 60.0
    achievement_rate = min(int((total_actual_hours / st.session_state.target_study_hours) * 100), 100) if st.session_state.target_study_hours > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="오늘 총 공부시간", value=f"{total_actual_hours:.1f} 시간")
    with col2:
        st.metric(label="목표 대비 달성률", value=f"{achievement_rate}%", delta=f"목표 {st.session_state.target_study_hours}시간")
    with col3:
        completed_todos_count = sum([1 for t in st.session_state.todos if t["completed"]])
        total_todos_count = len(st.session_state.todos)
        st.metric(label="할 일 완료", value=f"{completed_todos_count} / {total_todos_count}")

    st.markdown("---")
    st.markdown("### ⏱️ 진행 중인 타이머 상태")
    if st.session_state.timer_state["running"]:
        st.info(f"현재 측정 중인 과목: **[{st.session_state.timer_state['subject']}] {st.session_state.timer_state['activity']}**")
        if st.button("👉 타이머 화면으로 이동하기"):
            st.warning("왼쪽 메뉴에서 '⏱️ 공부 타이머'를 선택해주세요.")
    else:
        st.write("현재 실행 중인 타이머가 없습니다.")

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🔔 오늘의 마감 알림")
        upcoming_alerts = [t for t in st.session_state.todos if not t["completed"] and t["due_date"] == date.today()]
        if upcoming_alerts:
            for alert in upcoming_alerts:
                st.markdown(f"- ⏰ **[{alert['alert_time']}]** {alert['title']}")
        else:
            st.success("오늘 예정된 마감 알림이 없습니다!")
            
    with col_b:
        st.markdown("### ⭐ 오늘의 주요 할 일")
        today_todos = [t for t in st.session_state.todos if t["due_date"] == date.today()]
        if today_todos:
            for t in today_todos:
                status_icon = "✅" if t["completed"] else "⏳"
                st.markdown(f"- {status_icon} **{t['category']}**: {t['title']}")
        else:
            st.write("등록된 할 일이 없습니다.")

# ==========================================
# 2. 할 일 기록 화면
# =================

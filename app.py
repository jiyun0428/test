import streamlit as st
from datetime import datetime, date, timedelta
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
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# --- 세션 상태(Database Simulation) 초기화 ---
if 'todos' not in st.session_state:
    # 구조: id, title, category, importance, due_date, alert_time, completed, linked_plan
    st.session_state.todos = [
        {"id": 1, "title": "수학 수의 성질 3단원 풀기", "category": "수학", "importance": "중", "due_date": date.today(), "alert_time": "09:00", "completed": False},
        {"id": 2, "title": "영어 단어 50개 암기", "category": "영어", "importance": "상", "due_date": date.today(), "alert_time": "14:00", "completed": False}
    ]

if 'plans' not in st.session_state:
    # 구조: id, time_slot, activity, subject, completed, target_minutes, actual_minutes, todo_id
    st.session_state.plans = [
        {"id": 1, "time_slot": "09:00 - 10:30", "activity": "수학 수의 성질 3단원 풀기", "subject": "수학", "completed": False, "target_minutes": 90, "actual_minutes": 0, "todo_id": 1},
        {"id": 2, "time_slot": "11:00 - 12:00", "activity": "영어 단어 50개 암기", "subject": "영어", "completed": False, "target_minutes": 60, "actual_minutes": 0, "todo_id": 2}
    ]

if 'timer_state' not in st.session_state:
    st.session_state.timer_state = {
        "running": False,
        "subject": "선택 안됨",
        "activity": "",
        "start_time": None,
        "elapsed_seconds": 0,
        "plan_id": None
    }

if 'target_study_hours' not in st.session_state:
    st.session_state.target_study_hours = 6.0  # 기본 목표 6시간

# --- 상단 타이틀 및 사이드바 내비게이션 (하단 메뉴 대체용 상단/사이드바 탭) ---
st.title("📚 스터디 플래너 & 타임머신")
st.caption(f"오늘 날짜: {date.today().strftime('%Y년 %m월 %d일 (%A)')}")

# 5대 메뉴 구현
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
    
    # 오늘 총 공부시간 계산 (분 -> 시간 변환)
    total_actual_mins = sum([p["actual_minutes"] for p in st.session_state.plans])
    total_actual_hours = total_actual_mins / 60.0
    
    # 달성률 계산
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
    
    # 진행 중인 타이머 상태 표시 및 바로 실행
    st.markdown("### ⏱️ 진행 중인 타이머 상태")
    if st.session_state.timer_state["running"]:
        st.info(f"현재 측정 중: **[{st.session_state.timer_state['subject']}] {st.session_state.timer_state['activity']}**")
        if st.button("👉 타이머 화면으로 이동하여 제어하기"):
            st.warning("왼쪽 메뉴에서 '⏱️ 공부 타이머'를 선택하세요.")
    else:
        st.write("현재 실행 중인 타이머가 없습니다. 계획표나 타이머 탭에서 학습을 시작하세요.")

    st.markdown("---")
    
    # 오늘 예정된 일정 및 알림 목록
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🔔 예정된 알림 & 일정")
        upcoming_alerts = [t for t in st.session_state.todos if not t["completed"] and t["due_date"] == date.today()]
        if upcoming_alerts:
            for alert in upcoming_alerts:
                st.markdown(f"- ⏰ **[{alert['alert_time']}]** {alert['title']} (마감: 오늘)")
        else:
            st.success("오늘 예정된 마감 알림이 없습니다!")
            
    with col_b:
        st.markdown("### ⭐ 오늘의 주요 할 일 미리보기")
        today_todos = [t for t in st.session_state.todos if t["due_date"] == date.today()]
        if today_todos:
            for t in today_todos:
                status_icon = "✅" if t["completed"] else "⏳"
                st.markdown(f"- {status_icon} **{t['category']}**: {t['title']}")
        else:
            st.write("등록된 할 일이 없습니다.")

# ==========================================
# 2. 할 일 기록 화면
# ==========================================
elif menu == "✅ 할 일":
    st.markdown("### ✅ 할 일 관리 (일간 / 주간)")
    
    with st.expander("➕ 새로운 할 일 추가하기", expanded=False):
        with st.form("add_todo_form"):
            new_title = st.text_input("할 일 내용")
            new_category = st.selectbox("과목 / 카테고리", ["수학", "영어", "국어", "탐구", "기타"])
            new_importance = st.selectbox("중요도", ["상", "중", "하"])
            new_due_date = st.date_input("마감 날짜", value=date.today())
            new_alert_time = st.text_input("알림 시간 (예: 14:00)", value="12:00")
            
            submit_todo = st.form_submit_button("할 일 추가")
            if submit_todo and new_title:
                new_id = max([t["id"] for t in st.session_state.todos], default=0) + 1
                st.session_state.todos.append({
                    "id": new_id,
                    "title": new_title,
                    "category": new_category,
                    "importance": new_importance,
                    "due_date": new_due_date,
                    "alert_time": new_alert_time,
                    "completed": False
                })
                st.success("할 일이 성공적으로 추가되었습니다!")
                st.rerun()

    st.markdown("---")
    st.markdown("### 📋 전체 할 일 목록")
    
    # 필터링 옵션
    filter_tab = st.radio("보기 선택", ["미완료 항목", "완료된 항목", "전체 보기"], horizontal=True)
    
    for idx, t in enumerate(st.session_state.todos):
        if filter_tab == "미완료 항목" and t["completed"]: continue
        if filter_tab == "완료된 항목" and not t["completed"]: continue
        
        cols = st.columns([0.1, 0.6, 0.3])
        with cols[0]:
            is_checked = st.checkbox("", value=t["completed"], key=f"todo_check_{t['id']}")
            if is_checked != t["completed"]:
                st.session_state.todos[idx]["completed"] = is_checked
                # 연동된 계획표가 있다면 함께 완료 상태 업데이트
                for p in st.session_state.plans:
                    if p.get("todo_id") == t["id"]:
                        p["completed"] = is_checked
                st.rerun()
        with cols[1]:
            st.markdown(f"**[{t['category']}]** {t['title']} <span style='color:gray; font-size:0.8em;'>(마감: {t['due_date']} / 중요도: {t['importance']})</span>", unsafe_allow_html=True)
        with cols[2]:
            if st.button("삭제", key=f"del_todo_{t['id']}"):
                st.session_state.todos.pop(idx)
                st.rerun()

# ==========================================
# 3. 하루 계획표 화면
# ==========================================
elif menu == "📅 하루 계획표":
    st.markdown("### 📅 시간대별 하루 계획표")
    
    with st.expander("➕ 시간대별 일정 등록하기", expanded=False):
        with st.form("add_plan_form"):
            p_time = st.text_input("시간대 (예: 13:00 - 15:00)")
            p_subject = st.selectbox("과목", ["수학", "영어", "국어", "탐구", "기타"], key="plan_subj")
            
            # 할 일 목록에서 항목 연동 선택
            todo_options = {t["title"]: t["id"] for t in st.session_state.todos}
            selected_todo_title = st.selectbox("할 일 목록과 연동 (선택)", ["연동 안 함"] + list(todo_options.keys()))
            
            p_activity = st.text_input("활동 내용 (할 일 선택 시 자동 입력됨)", value="" if selected_todo_title == "연동 안 함" else selected_todo_title)
            p_target_mins = st.number_input("목표 공부 시간 (분)", min_value=10, max_value=360, value=60, step=10)
            
            submit_plan = st.form_submit_button("계획 추가")
            if submit_plan and p_time and p_activity:
                new_pid = max([p["id"] for p in st.session_state.plans], default=0) + 1
                linked_t_id = todo_options.get(selected_todo_title) if selected_todo_title != "연동 안 함" else None
                
                st.session_state.plans.append({
                    "id": new_pid,
                    "time_slot": p_time,
                    "activity": p_activity,
                    "subject": p_subject,
                    "completed": False,
                    "target_minutes": p_target_mins,
                    "actual_minutes": 0,
                    "todo_id": linked_t_id
                })
                st.success("계획이 등록되었습니다!")
                st.rerun()

    st.markdown("---")
    st.markdown("### ⏱️ 오늘의 시간표 및 타이머 연동")
    
    for idx, plan in enumerate(st.session_state.plans):
        cols = st.columns([0.2, 0.5, 0.3])
        with cols[0]:
            st.markdown(f"**{plan['time_slot']}**")
        with cols[1]:
            status_mark = "✅ " if plan["completed"] else "⏳ "
            st.markdown(f"{status_mark} **[{plan['subject']}]** {plan['activity']}  \n<span style='font-size:0.85em; color:gray;'>계획: {plan['target_minutes']}분 | 실제: {plan['actual_minutes']}분</span>", unsafe_allow_html=True)
        with cols[2]:
            # 타이머 실행 버튼
            if st.button("🚀 타이머 시작", key=f"start_timer_btn_{plan['id']}"):
                st.session_state.timer_state = {
                    "running": True,
                    "subject": plan["subject"],
                    "activity": plan["activity"],
                    "start_time": time.time(),
                    "elapsed_seconds": plan["actual_minutes"] * 60, # 기존 누적 시간 반영
                    "plan_id": plan["id"]
                }
                st.success(f"'{plan['activity']}' 타이머가 시작되었습니다!")
                st.rerun()
            
            # 완료 체크 토글
            is_p_checked = st.checkbox("완료", value=plan["completed"], key=f"plan_chk_{plan['id']}")
            if is_p_checked != plan["completed"]:
                st.session_state.plans[idx]["completed"] = is_p_checked
                # 연동된 할 일이 있다면 할 일 목록에도 반영
                if plan.get("todo_id"):
                    for t in st.session_state.todos:
                        if t["id"] == plan["todo_id"]:
                            t["completed"] = is_p_checked
                st.rerun()

    st.markdown("---")
    # 미완료 항목 다음 날 이동 기능 시뮬레이션
    if st.button("🔄 미완료 항목 다음 날로 이월하기"):
        st.info("미완료된 계획 및 할 일이 내일 날짜 기준으로 연장되었습니다.")

# ==========================================
# 4. 공부시간 측정 화면 (타이머)
# ==========================================
elif menu == "⏱️ 공부 타이머":
    st.markdown("### ⏱️ 실시간 공부 타이머")
    
    t_state = st.session_state.timer_state
    
    st.markdown(f"""
    <div style="background-color:#ffffff; padding:30px; border-radius:15px; text-align:center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h3 style="color:#6c757d;">현재 학습 과목</h3>
        <h1 style="color:#007bff; font-size:2.5em;">{t_state['subject']}</h1>
        <p style="font-size:1.2em; font-weight:bold;">{t_state['activity'] if t_state['activity'] else '자율 학습'}</p>
        <hr>
        <h2 style="font-size:3em; font-family:monospace;">
    """, unsafe_allow_html=True)
    
    # 타이머 표시 영역 (Streamlit 세션 연동 실시간 타이머 UI)
    timer_placeholder = st.empty()
    
    # 타이머 제어 버튼
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not t_state["running"]:
            if st.button("▶️ 타이머 시작 / 재시작", use_container_width=True):
                st.session_state.timer_state["running"] = True
                st.session_state.timer_state["start_time"] = time.time() - st.session_state.timer_state["elapsed_seconds"]
                st.rerun()
        else:
            if st.button("⏸️ 일시정지", use_container_width=True):
                if t_state["start_time"]:
                    st.session_state.timer_state["elapsed_seconds"] = int(time.time() - t_state["start_time"])
                st.session_state.timer_state["running"] = False
                st.rerun()
                
    with col2:
        if st.button("⏹️ 종료 및 저장", use_container_width=True):
            if t_state["start_time"]:
                final_elapsed = int(time.time() - t_state["start_time"])
            else:
                final_elapsed = t_state["elapsed_seconds"]
                
            total_minutes = round(final_elapsed / 60)
            
            # 계획표와 연동되어 있다면 실제 공부 시간 자동 누적 반영
            if t_state["plan_id"]:
                for p in st.session_state.plans:
                    if p["id"] == t_state["plan_id"]:
                        p["actual_minutes"] += total_minutes
            
            # 초기화
            st.session_state.timer_state = {
                "running": False,
                "subject": "선택 안됨",
                "activity": "",
                "start_time": None,
                "elapsed_seconds": 0,
                "plan_id": None
            }
            st.success(f"공부시간 총 {total_minutes}분이 학습 리포트 및 계획표에 성공적으로 저장되었습니다!")
            st.rerun()
            
    with col3:
        if st.button("🔄 초기화", use_container_width=True):
            st.session_state.timer_state["elapsed_seconds"] = 0
            st.session_state.timer_state["start_time"] = time.time() if t_state["running"] else None
            st.rerun()

    # 타이머 구동 로직 루프 (실행 중일 때 화면 갱신)
    if t_state["running"]:
        current_elapsed = int(time.time() - t_state["start_time"])
        st.session_state.timer_state["elapsed_seconds"] = current_elapsed
        mins, secs = divmod(current_elapsed, 60)
        hours, mins = divmod(mins, 60)
        timer_placeholder.markdown(f"<h1 style='color: #28a745;'>{hours:02d}:{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
        time.sleep(1)
        st.rerun()
    else:
        current_elapsed = t_state["elapsed_seconds"]
        mins, secs = divmod(current_elapsed, 60)
        hours, mins = divmod(mins, 60)
        timer_placeholder.markdown(f"<h1 style='color: #6c757d;'>{hours:02d}:{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)

# ==========================================
# 5. 학습 달성률 및 종합 관리 화면 (리포트)
# ==========================================
else:
    st.markdown("### 📊 학습 달성률 및 종합 리포트")
    
    # 목표 설정 수정 기능
    with st.expander("⚙️ 일일 목표 공부시간 설정"):
        st.session_state.target_study_hours = st.slider("하루 목표 공부시간 (시간)", min_value=1.0, max_value=14.0, value=st.session_state.target_study_hours, step=0.5)

    st.markdown("---")
    
    # 통계 지표 계산
    total_target_mins = sum([p["target_minutes"] for p in st.session_state.plans])
    total_actual_mins = sum([p["actual_minutes"] for p in st.session_state.plans])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="총 계획 공부시간", value=f"{total_target_mins / 60:.1f} 시간")
    with col2:
        st.metric(label="총 실제 공부시간", value=f"{total_actual_mins / 60:.1f} 시간", delta=f"{(total_actual_mins - total_target_mins) / 60:.1f} 시간 차이")

    st.markdown("---")
    st.markdown("### 📈 과목별 실제 공부시간 통계")
    
    # 과목별 데이터 집계
    subject_stats = {}
    for p in st.session_state.plans:
        subj = p["subject"]
        subject_stats[subj] = subject_stats.get(subj, 0) + p["actual_minutes"]
        
    if subject_stats:
        # Streamlit 내장 바 차트 활용
        st.bar_chart(subject_stats)
    else:
        st.info("표시할 학습 데이터가 아직 없습니다.")
        
    st.markdown("---")
    st.markdown("### 📝 미완료 항목 점검 및 관리")
    uncompleted_plans = [p for p in st.session_state.plans if not p["completed"]]
    if uncompleted_plans:
        st.warning(f"총 {len(uncompleted_plans)}개의 계획이 아직 완료되지 않았습니다.")
        for up in uncompleted_plans:
            st.markdown(f"- **[{up['subject']}]** {up['activity']} (목표: {up['target_minutes']}분)")
    else:
        st.success("🎉 오늘의 모든 계획을 완벽하게 달성했습니다!")

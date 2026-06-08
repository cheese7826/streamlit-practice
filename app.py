import streamlit as st
from datetime import datetime

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="건강 관리 앱")

page = st.sidebar.radio("📌 메뉴", ["🚭 금연", "🍺 금주"])

# -----------------------------
# 초기 상태
# -----------------------------
st.session_state.setdefault("smoke_running", False)
st.session_state.setdefault("smoke_start", None)
st.session_state.setdefault("smoke_best", 0)
st.session_state.setdefault("daily_cigarettes", 20)
st.session_state.setdefault("pack_price", 5000)

st.session_state.setdefault("drink_running", False)
st.session_state.setdefault("drink_start", None)
st.session_state.setdefault("drink_best", 0)
st.session_state.setdefault("weekly_drink", 7)
st.session_state.setdefault("bottle_price", 5000)

# -----------------------------
# 공통 함수
# -----------------------------
def format_time(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{days}일 {hours:02}:{minutes:02}:{secs:02}"

# =========================================================
# 🚭 금연 페이지
# =========================================================
if page == "🚭 금연":

    st.title("🚭 금연 타이머")

    daily = st.number_input("하루 흡연량", 1, value=st.session_state.daily_cigarettes)
    price = st.number_input("한 갑 가격", 1, value=st.session_state.pack_price)

    st.session_state.daily_cigarettes = daily
    st.session_state.pack_price = price

    col1, col2 = st.columns(2)

    with col1:
        if not st.session_state.smoke_running:
            if st.button("🚭 금연 시작"):
                st.session_state.smoke_running = True
                st.session_state.smoke_start = datetime.now()

    with col2:
        if st.button("초기화"):
            st.session_state.smoke_running = False
            st.session_state.smoke_start = None
            st.session_state.smoke_best = 0

    # -----------------------------
    # 계산
    # -----------------------------
    level = 0
    title = "🐣 입문자"
    cig = 0
    money = 0
    seconds = 0

    if st.session_state.smoke_running and st.session_state.smoke_start:
        seconds = int((datetime.now() - st.session_state.smoke_start).total_seconds())

        cig = int(seconds / (86400 / st.session_state.daily_cigarettes))
        level = cig // 30

        if level >= 30:
            title = "👑 비흡연자"
        elif level >= 20:
            title = "🏆 금연 마스터"
        elif level >= 10:
            title = "💎 금연 전문가"
        else:
            title = "🚭 진행 중"

        money = int(cig * (st.session_state.pack_price / 20))

    # -----------------------------
    # 출력
    # -----------------------------
    st.metric("⏱ 시간", format_time(seconds))
    st.metric("🚬 안 피운 담배", cig)
    st.metric("💰 절약 금액", f"{money:,}원")
    st.metric("⭐ 레벨", f"{level} ({title})")

# =========================================================
# 🍺 금주 페이지
# =========================================================
elif page == "🍺 금주":

    st.title("🍺 금주 타이머")

    weekly = st.number_input("일주일 술 소비량", 1, value=st.session_state.weekly_drink)
    price = st.number_input("한 병 가격", 1, value=st.session_state.bottle_price)

    st.session_state.weekly_drink = weekly
    st.session_state.bottle_price = price

    col1, col2 = st.columns(2)

    with col1:
        if not st.session_state.drink_running:
            if st.button("🍺 금주 시작"):
                st.session_state.drink_running = True
                st.session_state.drink_start = datetime.now()

    with col2:
        if st.button("초기화"):
            st.session_state.drink_running = False
            st.session_state.drink_start = None
            st.session_state.drink_best = 0

    # -----------------------------
    # 계산
    # -----------------------------
    level = 0
    title = "🐣 입문자"
    drink = 0
    money = 0
    seconds = 0

    if st.session_state.drink_running and st.session_state.drink_start:
        seconds = int((datetime.now() - st.session_state.drink_start).total_seconds())

        days = seconds // 86400
        drink = int((days * weekly) / 7)

        level = drink // 3

        if level >= 30:
            title = "👑 금주 마스터"
        elif level >= 20:
            title = "🏆 절제 고수"
        elif level >= 10:
            title = "💎 절주 전문가"
        else:
            title = "🍺 진행 중"

        money = drink * st.session_state.bottle_price

    # -----------------------------
    # 출력
    # -----------------------------
    st.metric("⏱ 시간", format_time(seconds))
    st.metric("🍺 줄인 술", drink)
    st.metric("💰 절약 금액", f"{money:,}원")
    st.metric("⭐ 레벨", f"{level} ({title})")
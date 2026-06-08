import streamlit as st
from datetime import datetime
import json
import os
import math

FILE = "quit_smoking_data.json"
st.markdown("🔥 너 지금도 잘하고 있어!")
st.link_button("금연 상담-->금연길라잡이 홈페이지", "https://www.nosmokeguide.go.kr/")
st.markdown("금연은 신체와 정신 건강에 긍정적인 영향을 미치며, 심혈관 건강 개선, 폐 기능 향상, 암 위험 감소 등의 효과를 가져옵니다.")




# -----------------------------
# 데이터 로드 / 저장
# -----------------------------
def save_data():
    data = {
        "running": st.session_state.running,
        "start_time": st.session_state.start_time.isoformat()
        if st.session_state.start_time else None,
        "daily_cigarettes": st.session_state.daily_cigarettes,
        "pack_price": st.session_state.pack_price,
        "best_seconds": st.session_state.best_seconds
    }

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def load_data():
    if not os.path.exists(FILE):
        return

    with open(FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    st.session_state.running = data.get("running", False)

    st.session_state.start_time = None
    if data.get("start_time"):
        st.session_state.start_time = datetime.fromisoformat(
            data["start_time"]
        )

    st.session_state.daily_cigarettes = data.get("daily_cigarettes", 20)
    st.session_state.pack_price = data.get("pack_price", 5000)
    st.session_state.best_seconds = data.get("best_seconds", 0)


# -----------------------------
# 초기 상태
# -----------------------------
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.running = False
    st.session_state.start_time = None
    st.session_state.daily_cigarettes = 20
    st.session_state.pack_price = 5000
    st.session_state.best_seconds = 0

    load_data()


# -----------------------------
# 자동 새로고침 (1초)
# -----------------------------
#st.autorefresh(interval=1000, key="refresh")


# -----------------------------
# 계산 함수
# -----------------------------
def format_time(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{days}일 {hours:02}:{minutes:02}:{secs:02}"


# -----------------------------
# 버튼 기능
# -----------------------------
def start():
    if st.session_state.running:
        return

    st.session_state.running = True
    st.session_state.start_time = datetime.now()
    save_data()


def reset():
    st.session_state.running = False
    st.session_state.start_time = None
    st.session_state.best_seconds = 0
    save_data()


# -----------------------------
# UI
# -----------------------------
st.title("🚭 금연 타이머")

daily = st.number_input(
    "하루 흡연량",
    min_value=1,
    value=st.session_state.daily_cigarettes
)

price = st.number_input(
    "한 갑 가격",
    min_value=1,
    value=st.session_state.pack_price
)

st.session_state.daily_cigarettes = daily
st.session_state.pack_price = price




col1, col2 = st.columns(2)

with col1:
    if not st.session_state.running:
        if st.button("🚭 금연 시작"):
            start()
    else:
        st.button("📊 진행 상황 확인")

with col2:
    if st.button("초기화"):
        reset()

# 🔥 상태 표시 (진짜 핵심)
if st.session_state.running:
    st.success("🚭 금연 진행 중입니다")
else:
    st.info("🚭 시작 버튼을 눌러주세요")







# -----------------------------
# 시간 계산
# -----------------------------
if st.session_state.running and st.session_state.start_time:
    elapsed = datetime.now() - st.session_state.start_time
    seconds = int(elapsed.total_seconds())

    if seconds > st.session_state.best_seconds:
        st.session_state.best_seconds = seconds
        save_data()

    cig_count = int(seconds / (86400 / st.session_state.daily_cigarettes))
    # ⭐ 레벨 시스템
    level = cig_count // 30
    if level >= 30:
        title_rank = "👑 전설"
    elif level >= 20:
        title_rank = "🏆 마스터"
    elif level >= 10:
        title_rank = "💎 전문가"
    elif level >= 7:
        title_rank = "🔥 숙련자"
    elif level >= 5:
        title_rank = "💪 성장 중"
    elif level >= 3:
        title_rank = "🌱 적응 중"
    elif level >= 1:
        title_rank = "🚭 시작 단계"
    else:
        title_rank = "🐣 입문자"
    remaining = 30 - (cig_count % 30)
    money = int(cig_count * (st.session_state.pack_price / 20))

else:
    seconds = 0
    cig_count = 0
    money = 0


# -----------------------------
# 출력
# -----------------------------
st.metric("⏱ 시간", format_time(seconds))
st.metric("🚭 금연 일수", f"{seconds // 86400}일")
st.metric("🚬 안 피운 담배", f"{cig_count:,}개비")
st.metric("💰 절약 금액", f"{money:,}원")
st.metric("🏆 최고 기록", format_time(st.session_state.best_seconds))
st.metric("⭐ 레벨", f"{level} ({title_rank})")
st.metric("🎯 다음 레벨까지", f"{remaining}개비")


# -----------------------------
# 간단한 시각 효과 (연기 느낌)
# -----------------------------
smoke = "💨 " * min(10, (seconds // 60) % 10)
st.text(smoke)
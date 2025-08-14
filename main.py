import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="MBTI 직업 추천 💼",
    page_icon="🎯",
    layout="centered"
)

# CSS 스타일
st.markdown("""
<style>
    .title {
        font-size: 42px;
        font-weight: bold;
        color: #ff4b4b;
        text-align: center;
    }
    .subtitle {
        font-size: 20px;
        color: #555;
        text-align: center;
        margin-bottom: 20px;
    }
    .job-card {
        background-color: #fff3e6;
        padding: 12px;
        border-radius: 15px;
        margin: 8px 0;
        font-size: 18px;
        font-weight: 500;
        box-shadow: 0px 3px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# MBTI 데이터
mbti_jobs = {
    "INTJ": {
        "설명": "🧠 전략가형 — 계획적, 분석적, 미래 지향 💡",
        "추천 직업": ["📊 데이터 과학자", "📈 전략 컨설턴트", "💻 시스템 엔지니어", "🔍 연구원", "🏦 금융 분석가"]
    },
    "INTP": {
        "설명": "🌀 사색가형 — 창의적 문제 해결, 논리적 사고 🧩",
        "추천 직업": ["🖥 프로그래머", "🔬 연구원", "📚 교수", "📐 설계 엔지니어", "🧪 과학자"]
    },
    "ENTJ": {
        "설명": "🚀 지도자형 — 목표 지향적, 결단력, 조직 관리 능력 💼",
        "추천 직업": ["🏢 CEO", "📊 경영 컨설턴트", "💼 프로젝트 매니저", "📈 투자 분석가", "🏦 은행 임원"]
    },
    "ENTP": {
        "설명": "🎯 발명가형 — 창의적, 논쟁을 즐김, 도전 정신🔥",
        "추천 직업": ["🚀 창업가", "🎤 방송인", "📢 마케터", "🎬 영화 감독", "📚 작가"]
    },
    "INFJ": {
        "설명": "🌱 옹호자형 — 이상주의, 깊은 통찰력, 타인 배려 💖",
        "추천 직업": ["🎓 심리상담사", "📖 작가", "🎨 예술가", "🌍]()


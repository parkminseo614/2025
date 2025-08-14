import streamlit as st

# MBTI별 직업 추천 데이터
mbti_jobs = {
    "INTJ": {
        "설명": "전략가형, 계획적이고 분석적인 성향을 가짐.",
        "추천 직업": ["데이터 과학자", "전략 컨설턴트", "시스템 엔지니어"]
    },
    "ENFP": {
        "설명": "열정적이고 창의적인 성향, 사람과의 소통을 좋아함.",
        "추천 직업": ["광고 기획자", "마케터", "스타트업 창업가"]
    },
    "ISTP": {
        "설명": "문제 해결을 즐기고, 실용적인 접근을 선호함.",
        "추천 직업": ["기계 엔지니어", "항공 정비사", "응급구조사"]
    },
    "ESFJ": {
        "설명": "사교적이고 타인의 필요를 잘 파악함.",
        "추천 직업": ["교사", "간호사", "인사 담당자"]
    }
}

# 웹앱 제목
st.title("MBTI 기반 진로 추천 사이트")
st.write("당신의 MBTI를 선택하면, 성향에 맞는 직업을 추천해드립니다.")

# MBTI 선택
selected_mbti = st.selectbox("MBTI를 선택하세요", list(mbti_jobs.keys()))

# 결과 표시
if selected_mbti:
    st.subheader(f"💡 {selected_mbti} 성향")
    st.write(mbti_jobs[selected_mbti]["설명"])

    st.subheader("📌 추천 직업")
    for job in mbti_jobs[selected_mbti]["추천 직업"]:
        st.write(f"- {job}")


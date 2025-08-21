import streamlit as st
import pandas as pd
from io import StringIO

# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(
    page_title="피부 고민별 성분 추천",
    page_icon="🌿",
    layout="wide",
)

st.title("🌿 피부 고민별 화장품 성분 추천기")
st.caption("피부 상태와 목표에 맞는 성분을 똑똑하게 고르세요. (의료 정보가 아닌 일반 가이드입니다)")

# ---------------------------
# 데이터베이스 (간단 버전)
# ---------------------------
ingredients_db = {
    # 미백/색소
    "나이아신아마이드": {
        "concerns": ["미백/잡티", "피지/유분", "진정/붉은기", "모공/결"],
        "desc": "비타민 B3. 색소 균일화, 피지 조절, 장벽 강화, 홍반 개선에 도움.",
        "pairs": ["아젤라익산", "알파알부틴", "징크 PCA", "세라마이드"],
        "avoid_with": [],
        "usage": "매일 AM/PM 사용 가능. 2~5%로 시작.",
        "strength": "2–10%",
        "pregnancy_safe": True,
        "skin": ["건성", "지성", "복합성", "민감성", "중성"],
        "kproducts": [
            "뷰티오브조선 글로우 세럼: 프로폴리스+나이아신", 
            "라운드랩 자작나무 수분 토너 (나이아신 함유)",
            "닥터지 레드 블레미쉬 클리어 수딩 크림"
        ],
    },
    "비타민C(아스코빅산)": {
        "concerns": ["미백/잡티", "탄력/주름", "항산화"],
        "desc": "강력한 항산화 및 색소 완화. 콜라겐 합성 보조.",
        "pairs": ["비타민E", "페룰산", "나이아신아마이드(완충/저자극형)", "선크림"],
        "avoid_with": ["강산성 각질제거제(같은 루틴 고농도)", "벤조일퍼옥사이드(동시 사용 비권장)"],
        "usage": "아침 단독 또는 항산화 세럼 단계. 저농도(5–10%)→적응 후 15%. 산화 주의.",
        "strength": "5–20% (L-AA 기준)",
        "pregnancy_safe": True,
        "skin": ["건성", "지성", "복합성", "중성"],
        "kproducts": [
            "브링그린 비타C 톤업 세럼",
            "코스알엑스 더 비타민C 23 세럼"
        ],
    },
    "알파알부틴": {
        "concerns": ["미백/잡티"],
        "desc": "티로시나아제 억제. 잡티/멜라닌 완화.",
        "pairs": ["나이아신아마이드", "아젤라익산"],
        "avoid_with": [],
        "usage": "AM/PM 사용 가능. 1–2%.",
        "strength": "1–2%",
        "pregnancy_safe": True,
        "skin": ["건성", "지성", "복합성", "민감성", "중성"],
        "kproducts": ["더랩바이블랑두 알부틴 세럼"],
    },
    # 여드름/피지
    "살리실산(BHA)": {
        "concerns": ["여드름", "블랙헤드", "모공/결", "피지/유분"],
        "desc": "지용성 각질 용해. 블랙헤드/각질/피지 정리.",
        "pairs": ["나이아신아마이드", "징크 PCA"],
        "avoid_with": ["레티노이드(동시 고농도)", "벤조일퍼옥사이드(자극↑)"],
        "usage": "격일 저빈도로 시작. 토너/세럼/스팟. 반드시 보습 & 자외선 차단.",
        "strength": "0.5–2%",
        "pregnancy_safe": True,
        "skin": ["지성", "복합성", "중성"],
        "kproducts": [
            "파이올로지 BHA 토너",
            "바이오더마 세비엄 세럼 (국내 유통 버전 상이 가능)"
        ],
    },
    "글리콜릭산(AHA)": {
        "concerns": ["모공/결", "미백/잡티", "탄력/주름"],
        "desc": "수용성 각질 제거. 표피 턴오버, 피부결 개선.",
        "pairs": ["나이아신아마이드", "PHA", "보습제"],
        "avoid_with": ["비타민C(같은 루틴 고농도)", "레티노이드(동시 고농도)"],
        "usage": "주 2–3회 밤에. 저농도(5–8%)에서 시작.",
        "strength": "5–10%(홈케어)",
        "pregnancy_safe": True,
        "skin": ["건성", "복합성", "중성"],
        "kproducts": ["토리든 다이브인 AHA 토너"],
    },
    "아젤라익산": {
        "concerns": ["여드름", "미백/잡티", "진정/붉은기"],
        "desc": "항염/여드름/색소/홍조 다목적.",
        "pairs": ["나이아신아마이드", "BHA", "세라마이드"],
        "avoid_with": ["강산성 제품 다중 레이어링"],
        "usage": "하루 1회 밤부터. 10% 전후 홈케어.",
        "strength": "5–15%",
        "pregnancy_safe": True,
        "skin": ["건성", "지성", "복합성", "민감성", "중성"],
        "kproducts": ["더랩바이블랑두 아젤라익산 크림"],
    },
    "벤조일퍼옥사이드": {
        "concerns": ["여드름"],
        "desc": "P. acnes 살균. 염증성 스팟에 효과적.",
        "pairs": ["나이아신아마이드", "진정/보습"],
        "avoid_with": ["레티노이드(동시)", "비타민C(L-AA) 동시"],
        "usage": "스팟 또는 저농도 전면. 천천히 적응.",
        "strength": "2.5–5%",
        "pregnancy_safe": True,
        "skin": ["지성", "복합성"],
        "kproducts": ["일부 의약외품/약국 제품 참고"],
    },
    # 장벽/보습/진정
    "세라마이드": {
        "concerns": ["건조/장벽", "민감/홍조"],
        "desc": "피부 장벽 지질 보충. 자극 완화 및 수분 유지.",
        "pairs": ["콜레스테롤", "지방산", "나이아신아마이드"],
        "avoid_with": [],
        "usage": "AM/PM 크림 단계. 각질제거/레티놀과 병행 시 자극 완화.",
        "strength": "성분 배합형",
        "pregnancy_safe": True,
        "skin": ["건성", "지성", "복합성", "민감성", "중성"],
        "kproducts": ["일리윤 세라마이드 아토 크림", "라로슈포제 시카플라스트 B5"],
    },
    "히알루론산": {
        "concerns": ["건조/장벽", "수분부족"],
        "desc": "수분 결합. 토너/세럼/크림 어디서나 보습.",
        "pairs": ["글리세린", "판테놀", "세라마이드"],
        "avoid_with": ["매우 건조한 실내·야외에서 단독 사용(증발 유의)"],
        "usage": "젖은 피부에 레이어링, 이후 크림으로 밀폐.",
        "strength": "저·중·고분자 혼합 선호",
        "pregnancy_safe": True,
        "skin": ["모든 피부"],
        "kproducts": ["토리든 다이브인 세럼", "아이소이 히아루로닉 토너"]
    },
    "판테놀": {
        "concerns": ["민감/홍조", "건조/장벽"],
        "desc": "비타민 B5. 진정/보습/장벽 강화.",
        "pairs": ["알란토인", "마데카소사이드", "센텔라"],
        "avoid_with": [],
        "usage": "AM/PM 어디서나.",
        "strength": "2–10%",
        "pregnancy_safe": True,
        "skin": ["모든 피부"],
        "kproducts": ["라운드랩 자작나무 로션", "닥터자르트 시카페어 세럼"],
    },
    # 안티에이징
    "레티놀": {
        "concerns": ["탄력/주름", "모공/결", "여드름"],
        "desc": "비타민A 유도체. 콜라겐/턴오버. 자극 주의.",
        "pairs": ["세라마이드", "판테놀", "펩타이드"],
        "avoid_with": ["벤조일퍼옥사이드", "고농도 AHA/BHA 동시", "임신/수유"],
        "usage": "주 2회 밤부터, 완전 건조 피부 위에 소량. 적응 후 증량.",
        "strength": "0.1–0.3% (초보) / 0.5–1% (숙련)",
        "pregnancy_safe": False,
        "skin": ["건성", "복합성", "중성"],
        "kproducts": ["더랩바이블랑두 레티놀 크림", "코스알엑스 레티놀 0.1"],
    },
    "레티날": {
        "concerns": ["탄력/주름", "모공/결"],
        "desc": "레티놀보다 한 단계 활성에 가까운 비타민A. 빠른 체감, 자극도 존재.",
        "pairs": ["세라마이드", "펩타이드"],
        "avoid_with": ["벤조일퍼옥사이드", "강산성 각질제거제"],
        "usage": "주 2회 밤. 저농도에서 시작.",
        "strength": "0.05–0.1%",
        "pregnancy_safe": False,
        "skin": ["복합성", "중성"],
        "kproducts": ["아이소이 레티날 크림 (성분 유사 제품 참고)"],
    },
    "펩타이드": {
        "concerns": ["탄력/주름", "장벽/보습"],
        "desc": "신호/구조 펩타이드. 탄력 및 보습 보조.",
        "pairs": ["나이아신아마이드", "히알루론산"],
        "avoid_with": [],
        "usage": "AM/PM 어디서나. 자극 적음.",
        "strength": "배합형",
        "pregnancy_safe": True,
        "skin": ["모든 피부"],
        "kproducts": ["비플레인 펩타이드 앰플", "메디힐 펩타이드 크림"],
    },
    # 피지/유분 & 모공
    "징크 PCA": {
        "concerns": ["피지/유분", "여드름"],
        "desc": "피지 조절 및 진정 보조.",
        "pairs": ["나이아신아마이드", "BHA"],
        "avoid_with": [],
        "usage": "AM/PM 가벼운 세럼/토너.",
        "strength": "0.3–1%",
        "pregnancy_safe": True,
        "skin": ["지성", "복합성", "중성"],
        "kproducts": ["더페이스샵 더테라피 토너 (성분 유사)"]
    },
    # 민감/홍조
    "센텔라 아시아티카(시카)": {
        "concerns": ["민감/홍조", "장벽/보습"],
        "desc": "트리터펜 성분이 진정/복구 보조.",
        "pairs": ["판테놀", "알란토인", "세라마이드"],
        "avoid_with": [],
        "usage": "AM/PM 어디서나.",
        "strength": "배합형",
        "pregnancy_safe": True,
        "skin": ["모든 피부"],
        "kproducts": ["닥터자르트 시카페어 크림", "아비브 어성초 토너(진정 계열)"],
    },
}

concern_options = [
    "여드름", "블랙헤드", "피지/유분", "모공/결", "미백/잡티",
    "건조/장벽", "수분부족", "민감/홍조", "탄력/주름", "항산화"
]

skin_types = ["건성", "지성", "복합성", "민감성", "중성"]

# ---------------------------
# 사이드바 - 사용자 입력
# ---------------------------
st.sidebar.header("나의 피부 정보")
selected_skin = st.sidebar.selectbox("피부 타입", options=skin_types, index=2)
selected_concerns = st.sidebar.multiselect(
    "해결하고 싶은 피부 고민 (복수 선택)", options=concern_options, default=["모공/결"]
)
pregnancy_mode = st.sidebar.toggle("임신/수유 중 (레티노이드 자동 제외)", value=False)
sensitive_mode = st.sidebar.toggle("예민함/따가움이 쉽게 생김", value=False)
level = st.sidebar.slider("루틴 강도(적용 성분 수)", min_value=1, max_value=6, value=3)

st.sidebar.info("항상 자외선 차단제(SPF 30+)는 아침 루틴의 필수 단계입니다 ☀️")

# ---------------------------
# 추천 로직
# ---------------------------
def score_ingredient(name, meta):
    score = 0
    # 고민 일치 가중치
    for c in selected_concerns:
        if c in meta["concerns"]:
            score += 3
    # 피부 타입 적합성
    if selected_skin in meta["skin"] or "모든 피부" in meta["skin"]:
        score += 2
    # 민감 모드면 산/레티노이드 감점
    if sensitive_mode and any(key in name for key in ["AHA", "BHA", "레티" ]):
        score -= 2
    return score

# 필터링
filtered = {}
for k, v in ingredients_db.items():
    if pregnancy_mode and v.get("pregnancy_safe") is False:
        continue
    # 민감 모드에서 아주 자극적인 조합을 1차 제외
    if sensitive_mode and any(x in v.get("avoid_with", []) for x in ["강산성 각질제거제", "고농도 AHA/BHA 동시"]):
        pass
    filtered[k] = v

# 점수 부여 및 정렬
scored = sorted([(k, v, score_ingredient(k, v)) for k, v in filtered.items()], key=lambda x: x[2], reverse=True)

# 상위 N개 선택 (레벨)
recommended = [(k, v) for k, v, s in scored if s > 0][:level]

# 상호작용 체크
def find_conflicts(selected_items):
    names = [n for n, _ in selected_items]
    conflicts = []
    for n, meta in selected_items:
        for aw in meta.get("avoid_with", []):
            # 간단 매칭
            for other in names:
                if other == n:
                    continue
                if aw.split("(")[0].strip() in other:
                    conflicts.append((n, other, aw))
    # 대표적인 추가 규칙
    pairs = set([p for _, m in selected_items for p in m.get("pairs", [])])
    return conflicts

conflicts = find_conflicts(recommended)

# ---------------------------
# 출력 영역
# ---------------------------
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("맞춤 성분 추천 결과")
    if not selected_concerns:
        st.warning("왼쪽에서 고민을 하나 이상 선택해 주세요.")
    elif not recommended:
        st.info("조건에 맞는 성분이 없어요. 필터를 조금 완화해 보세요.")
    else:
        for name, meta in recommended:
            with st.container(border=True):
                st.markdown(f"### ✅ {name}")
                st.write(meta["desc"])
                tags = ", ".join(meta["concerns"]) if meta.get("concerns") else ""
                st.caption(f"주요 타겟: {tags}")
                c1, c2, c3 = st.columns(3)
                c1.metric("권장 농도/범위", meta.get("strength", "배합형"))
                c2.metric("임신/수유", "가능" if meta.get("pregnancy_safe", True) else "비권장")
                c3.metric("적합 피부", ", ".join(meta.get("skin", [])))
                st.markdown("**사용 팁**: " + meta.get("usage", ""))
                if meta.get("pairs"):
                    st.markdown("**함께 쓰면 좋은 성분**: " + ", ".join(meta["pairs"]))
                if meta.get("avoid_with"):
                    st.markdown("**주의/피해야 할 조합**: " + ", ".join(meta["avoid_with"]))
                if meta.get("kproducts"):
                    with st.expander("🇰🇷 추천 한국 제품 ‘예시’ (참고용)"):
                        for p in meta["kproducts"]:
                            st.write("• " + p)

    if conflicts:
        with st.expander("⚠️ 선택된 성분 간 주의 조합"):
            for a, b, why in conflicts:
                st.write(f"- {a} ↔ {b}: {why}")

with col2:
    st.subheader("루틴 빌더")
    st.caption("초보자는 단계 수를 줄이고, 자극 성분은 격일/밤에!")
    am_steps = ["클렌저(저자극)", "항산화/진정", "보습제", "선크림(SPF 30+)" ]
    pm_steps = ["클렌저", "액티브", "보습제"]

    st.markdown("**아침(AM)**")
    am_list = []
    # 항산화 후보: 비타민C, 나이아신아마이드, 펩타이드, 진정류
    for n, m in recommended:
        if any(c in m["concerns"] for c in ["항산화", "진정/붉은기", "장벽/보습", "미백/잡티"]) and n not in ["레티놀", "레티날", "글리콜릭산(AHA)", "살리실산(BHA)"]:
            am_list.append(n)
    st.write(" → ".join(am_steps))
    st.write("AM 액티브 제안: " + (", ".join(am_list[:2]) if am_list else "나이아신아마이드, 펩타이드 등"))

    st.markdown("**저녁(PM)**")
    pm_list = []
    for n, m in recommended:
        if n in ["레티놀", "레티날", "글리콜릭산(AHA)", "살리실산(BHA)", "아젤라익산"]:
            pm_list.append(n)
    st.write(" → ".join(pm_steps))
    st.write("PM 액티브 제안: " + (", ".join(pm_list[:2]) if pm_list else "진정/보습 위주"))

    st.divider()
    st.subheader("내보내기")
    # 테이블 생성
    if recommended:
        df = pd.DataFrame([
            {
                "성분": n,
                "타겟": ", ".join(m.get("concerns", [])),
                "권장 범위": m.get("strength", ""),
                "임신/수유": "가능" if m.get("pregnancy_safe", True) else "비권장",
                "사용 팁": m.get("usage", ""),
            }
            for n, m in recommended
        ])
        st.dataframe(df, hide_index=True, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("CSV로 저장", data=csv, file_name="ingredient_recommendations.csv", mime="text/csv")
    else:
        st.caption("추천이 생성되면 표와 함께 다운로드 버튼이 나타납니다")

# ---------------------------
# 푸터/안내
# ---------------------------
st.divider()
st.markdown(
    """
**주의**  
- 본 앱은 일반적인 코스메틱 가이드이며, 질환/약물 치료는 전문가 상담이 필요합니다.  
- 민감 피부/임신·수유 중에는 신중하게 테스트하고, 자극 시 즉시 중단하세요.  
- 제품 성분/배합은 브랜드 리뉴얼로 변경될 수 있습니다.
"""
)

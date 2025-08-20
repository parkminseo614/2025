import streamlit as st
import numpy as np
from PIL import Image

# 퍼스널 컬러 데이터 정의
personal_color_data = {
    "봄 웜톤 🌸": {
        "desc": "밝고 따뜻한 파스텔톤이 잘 어울려요!",
        "good_colors": ["#FFD700", "#FFA07A", "#FF69B4", "#98FB98", "#FF8C00"],
        "bad_colors": ["#000080", "#2F4F4F", "#4B0082", "#708090", "#800080"],
        "makeup": "코랄, 피치, 오렌지 레드 계열 립 & 블러셔 / 골드 펄 아이섀도우 추천"
    },
    "여름 쿨톤 🌊": {
        "desc": "부드럽고 차분한 파스텔 쿨톤이 잘 어울려요!",
        "good_colors": ["#87CEEB", "#BA55D3", "#AFEEEE", "#FFB6C1", "#4682B4"],
        "bad_colors": ["#FF4500", "#8B0000", "#A0522D", "#FFD700", "#228B22"],
        "makeup": "로즈, 라일락, 핑크 계열 립 & 블러셔 / 실버 펄 아이섀도우 추천"
    },
    "가을 웜톤 🍂": {
        "desc": "깊고 따뜻한 어스톤 컬러가 잘 어울려요!",
        "good_colors": ["#8B4513", "#D2691E", "#B22222", "#FF7F50", "#DAA520"],
        "bad_colors": ["#1E90FF", "#4169E1", "#C71585", "#00CED1", "#E0FFFF"],
        "makeup": "브릭, 카멜, 테라코타 계열 립 & 블러셔 / 골드·브론즈 섀도우 추천"
    },
    "겨울 쿨톤 ❄️": {
        "desc": "선명하고 차가운 컬러가 잘 어울려요!",
        "good_colors": ["#000000", "#800080", "#FF1493", "#00CED1", "#1E90FF"],
        "bad_colors": ["#FFDAB9", "#F4A460", "#CD853F", "#DAA520", "#BC8F8F"],
        "makeup": "버건디, 푸시아, 와인 계열 립 / 차가운 블루·실버 섀도우 추천"
    }
}

# 퍼스널 컬러 판별 함수
def classify_personal_color(avg_color):
    r, g, b = avg_color

    if r > g and r > b:  # 빨강 계열이 강할 때
        if r > 160:
            return "봄 웜톤 🌸"
        else:
            return "가을 웜톤 🍂"
    else:
        if b > r and b > g:  # 파랑 계열이 강할 때
            return "겨울 쿨톤 ❄️"
        else:
            return "여름 쿨톤 🌊"

# Streamlit UI
st.title("🎨 AI 퍼스널 컬러 진단")
st.write("📸 사진을 업로드하면 퍼스널 컬러와 어울리는 색, 피해야 할 색, 색조 화장품까지 추천해드려요!")

uploaded_file = st.file_uploader("사진을 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 이미지 표시
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="업로드한 사진", use_column_width=True)

    # NumPy 배열 변환
    img_array = np.array(image)

    # 얼굴 대신 중앙 영역(사진 가운데 50%)만 추출
    h, w, _ = img_array.shape
    face_region = img_array[h//4: 3*h//4, w//4: 3*w//4]

    # 평균 색상 계산
    avg_color = face_region.mean(axis=(0,1))  # RGB 평균
    avg_color_rgb = tuple(map(int, avg_color))  # 정수 변환

    # 결과 판정
    tone = classify_personal_color(avg_color_rgb)
    data = personal_color_data[tone]

    # 출력
    st.markdown(f"## 결과: **{tone}**")
    st.write(data["desc"])

    # 대표 피부톤 컬러 표시
    hex_color = "#{:02x}{:02x}{:02x}".format(*avg_color_rgb)
    st.write("📍 피부톤 평균 색상")
    st.color_picker("피부톤 평균", hex_color, disabled=True)

    # 잘 어울리는 색
    st.subheader("✅ 잘 어울리는 색 5가지")
    cols = st.columns(5)
    for i, color in enumerate(data["good_colors"]):
        with cols[i]:
            st.color_picker(f"추천 {i+1}", color, disabled=True)

    # 피해야 하는 색
    st.subheader("❌ 피해야 하는 색 5가지")
    cols = st.columns(5)
    for i, color in enumerate(data["bad_colors"]):
        with cols[i]:
            st.color_picker(f"주의 {i+1}", color, disabled=True)

    # 색조 화장품 추천
    st.subheader("💄 색조 화장품 추천")
    st.write(data["makeup"])

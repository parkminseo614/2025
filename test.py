import streamlit as st
import numpy as np
from PIL import Image

# 퍼스널 컬러 판별 함수
def classify_personal_color(avg_color):
    r, g, b = avg_color

    # 단순 규칙 기반 (데모용)
    if r > g and r > b:  # 빨강 계열이 강할 때
        if r > 160:
            return "봄 웜톤 🌸", "밝고 따뜻한 파스텔톤이 잘 어울려요!"
        else:
            return "가을 웜톤 🍂", "깊고 따뜻한 어스톤 컬러가 잘 어울려요!"
    else:
        if b > r and b > g:  # 파랑 계열이 강할 때
            return "겨울 쿨톤 ❄️", "선명하고 차가운 컬러가 잘 어울려요!"
        else:
            return "여름 쿨톤 🌊", "부드럽고 차분한 파스텔 쿨톤이 잘 어울려요!"

# Streamlit UI
st.title("🎨 퍼스널 컬러 진단 앱")
st.write("📸 사진을 업로드하면 간단한 퍼스널 컬러를 알려드려요!")

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
    tone, message = classify_personal_color(avg_color_rgb)

    # 출력
    st.markdown(f"### 결과: **{tone}**")
    st.write(message)

    # 대표 색상 미리보기
    hex_color = "#{:02x}{:02x}{:02x}".format(*avg_color_rgb)
    st.write("대표 색상:")
    st.color_picker("평균 피부톤 색상", hex_color, disabled=True)

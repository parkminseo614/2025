import streamlit as st
centers, counts = simple_kmeans(flat2.astype(np.float32), k=5)
order = np.argsort(-counts)
dom_colors = [rgb_to_hex(centers[i]) for i in order]


# Layout
col1, col2 = st.columns([1,1])
with col1:
st.image(image, caption="업로드한 사진", use_column_width=True)
with col2:
st.subheader("진단 결과")
prof = tone_profile(final_season)
st.metric("퍼스널 컬러", final_season, help=prof['desc'])
st.write(f"**측정 지표** · L*: {L_mean:.1f} / C*: {C_mean:.1f} / b*: {b_mean:.1f}")
st.caption("(L*: 명도, C*: 채도, b*: +면 노란 기(웜), -면 푸른 기(쿨))")
st.markdown("**사진 주요 색 추출(참고)**")
ccols = st.columns(5)
for i,c in enumerate(dom_colors[:5]):
with ccols[i]:
st.markdown(f"<div style='width:100%;height:48px;border-radius:12px;border:1px solid rgba(0,0,0,.06);background:{c}'></div>", unsafe_allow_html=True)
st.caption(c)


# Suggested colors
st.markdown("---")
st.subheader("✔ 잘 어울리는 색 5")
pal = curated_palettes()[final_season]
good = pal['good']
for hex_code, label in good:
reason = reason_for_color(hex_code, final_season)
show_swatch(hex_code, label, reason)


st.subheader("✖ 피해야 하는 색 5")
bad = pal['bad']
for hex_code, label in bad:
reason = reason_for_color(hex_code, final_season)
show_swatch(hex_code, label, reason)


# Cosmetics
st.markdown("---")
st.subheader("🧴 한국 색조 추천 (톤별)")
st.caption("공식/유통사 페이지 링크를 제공합니다. 시즌/개인 취향에 따라 발색은 달라질 수 있어요.")


prods = cosmetics_by_season()[final_season]
for cat, items in prods.items():
st.markdown(f"### {cat}")
for brand, product, shade, url, note in items:
st.markdown(
f"- **{brand} · {product}** — *{shade}* \\n [{url}]({url}) \
<span style='opacity:.9'>({note})</span>",
unsafe_allow_html=True
)


# Tips
st.markdown("---")
st.subheader("💡 활용 팁")
st.markdown(
"""
- **립**은 추천 색 그대로 바르되, 농도를 조절해 데일리/포인트를 나눠보세요.
- **블러셔**는 립보다 **한 톤 연하거나 같은 톤**을 고르면 쉽습니다.
- **아이섀도우**는 시즌 무드(따뜻/차갑, 밝음/그윽함)에 맞는 팔레트를 선택하면 실패 확률이 낮아요.
- 조명/필터 영향을 줄이려면, **햇빛(창가) + 흰 벽**에서 다시 시도해 보세요.
"""
)
else:
st.info("좌측에서 얼굴 사진을 올리면 분석이 시작됩니다.")

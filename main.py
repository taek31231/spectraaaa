import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 페이지 설정 ---
st.set_page_config(layout="wide", page_title="고1 통합과학 스펙트럼 가상실험실")
st.title("🔬 스펙트럼 생성 원리와 데이터 분석")
st.markdown("분광기 내부의 빛의 경로를 관찰하고, 각 스펙트럼의 데이터 특징을 분석해 봅시다.")

# --- 파장별 실제 색상 반환 함수 ---
def nm_to_rgb(wavelength):
    if wavelength < 380 or wavelength > 750: return "rgb(0,0,0)"
    if 380 <= wavelength < 440: r, g, b = -(wavelength - 440) / (440 - 380), 0.0, 1.0
    elif 440 <= wavelength < 490: r, g, b = 0.0, (wavelength - 440) / (490 - 440), 1.0
    elif 490 <= wavelength < 510: r, g, b = 0.0, 1.0, -(wavelength - 510) / (510 - 490)
    elif 510 <= wavelength < 580: r, g, b = (wavelength - 510) / (580 - 510), 1.0, 0.0
    elif 580 <= wavelength < 645: r, g, b = 1.0, -(wavelength - 645) / (645 - 580), 0.0
    elif 645 <= wavelength <= 750: r, g, b = 1.0, 0.0, 0.0
    return f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"

# --- 원소별 데이터 (지문) ---
element_data = {
    "수소 (H)": [410.2, 434.1, 486.1, 656.3],
    "헬륨 (He)": [447.1, 501.6, 587.6, 667.8, 706.5],
    "나트륨 (Na)": [589.0, 589.6],
    "아르곤 (Ar)": [415.9, 420.1, 470.2, 560.7, 603.2, 696.5],
    "네온 (Ne)": [585.2, 588.2, 614.3, 640.2, 650.7, 703.2]
}

# --- 사이드바 조작 ---
st.sidebar.header("🛠️ 가상 분광기 설정")
spectrum_type = st.sidebar.radio("1. 관찰할 스펙트럼", ("연속 스펙트럼", "방출 스펙트럼", "흡수 스펙트럼"))
selected_element = None
if spectrum_type != "연속 스펙트럼":
    selected_element = st.sidebar.selectbox("2. 관찰할 원소 기체", list(element_data.keys()))

# --- 1. 분광기 내부 구조 및 빛의 경로 시각화 ---
st.subheader("1. 분광기 내부의 빛의 경로")
setup_fig = go.Figure()

# 고정 장치: 슬릿, 프리즘, 스크린
setup_fig.add_shape(type="rect", x0=3, y0=0.6, x1=3.1, y1=1.4, fillcolor="black", line_width=0) # 슬릿
setup_fig.add_trace(go.Scatter(x=[5], y=[1], mode="markers", marker=dict(size=65, symbol="triangle-up", color="lightgray"), showlegend=False)) # 프리즘
setup_fig.add_shape(type="rect", x0=8, y0=0.2, x1=8.1, y1=1.8, fillcolor="gray", opacity=0.2) # 스크린

# 모드별 광원 및 빛의 경로 시각화
if spectrum_type == "연속 스펙트럼":
    setup_fig.add_trace(go.Scatter(x=[0.5], y=[1], mode="markers+text", marker=dict(size=40, color="orange", symbol="star"), text=["고온의 별"], textposition="bottom center"))
    # 경로: 광원 -> 슬릿 -> 프리즘
    setup_fig.add_trace(go.Scatter(x=[0.7, 3, 5], y=[1, 1, 1], mode="lines", line=dict(color="orange", width=3, dash="solid")))
    # 경로: 프리즘 -> 스크린 (분산)
    for i, color in enumerate(['violet', 'blue', 'green', 'yellow', 'red']):
        setup_fig.add_trace(go.Scatter(x=[5, 8], y=[1, 0.4 + i*0.3], mode="lines", line=dict(color=color, width=2, opacity=0.6)))

elif spectrum_type == "방출 스펙트럼":
    setup_fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers+text", marker=dict(size=40, color="cyan", symbol="circle"), text=[f"고온의 {selected_element}"], textposition="bottom center"))
    # 경로: 기체 방출 -> 슬릿 -> 프리즘
    setup_fig.add_trace(go.Scatter(x=[1.2, 3, 5], y=[1, 1, 1], mode="lines", line=dict(color="cyan", width=2, dash="dash")))
    # 경로: 프리즘 -> 스크린 (특정 선)
    setup_fig.add_trace(go.Scatter(x=[5, 8], y=[1, 1], mode="lines", line=dict(color="cyan", width=2)))

else: # 흡수 스펙트럼
    setup_fig.add_trace(go.Scatter(x=[0.3], y=[1], mode="markers", marker=dict(size=30, color="orange", symbol="star"))) # 광원
    setup_fig.add_trace(go.Scatter(x=[1.5], y=[1], mode="markers+text", marker=dict(size=45, color="lightblue", symbol="circle-open", line=dict(width=4)), text=[f"저온의 {selected_element}"], textposition="bottom center"))
    # 경로: 광원 -> 기체 -> 슬릿 -> 프리즘
    setup_fig.add_trace(go.Scatter(x=[0.5, 1.5, 3, 5], y=[1, 1, 1, 1], mode="lines", line=dict(color="orange", width=4)))
    setup_fig.add_trace(go.Scatter(x=[5, 8], y=[1, 1], mode="lines", line=dict(color="orange", width=1, dash="dot")))

setup_fig.update_layout(xaxis=dict(range=[0, 9], visible=False), yaxis=dict(range=[0, 2], visible=False), height=220, margin=dict(l=0, r=0, t=0, b=0), template="plotly_white", showlegend=False)
st.plotly_chart(setup_fig, use_container_width=True)

# --- 2. 스펙트럼 관찰 및 에너지 그래프 ---
st.subheader("2. 관찰 결과 및 에너지 데이터 분석")

wavelengths = np.linspace(380, 750, 1000)
intensity = np.zeros_like(wavelengths)

if spectrum_type == "연속 스펙트럼":
    intensity = np.ones_like(wavelengths) * 0.85
elif spectrum_type == "방출 스펙트럼":
    for p in element_data[selected_element]:
        intensity += 0.85 * np.exp(-0.5 * ((wavelengths - p) / 1.5)**2)
elif spectrum_type == "흡수 스펙트럼":
    intensity = np.ones_like(wavelengths) * 0.85
    for p in element_data[selected_element]:
        intensity -= 0.75 * np.exp(-0.5 * ((wavelengths - p) / 1.5)**2)

intensity = np.clip(intensity, 0, 1)

fig = make_subplots(rows=2, cols=1, row_heights=[0.35, 0.65], shared_xaxes=True, vertical_spacing=0.1)

# [상단 스펙트럼 띠]
if spectrum_type == "방출 스펙트럼":
    fig.add_shape(type="rect", x0=380, y0=-0.5, x1=750, y1=0.5, fillcolor="black", line_width=0, row=1, col=1)
    for p in element_data[selected_element]:
        fig.add_shape(type="line", x0=p, y0=-0.5, x1=p, y1=0.5, line=dict(color=nm_to_rgb(p), width=5), row=1, col=1)
else:
    fig.add_trace(go.Heatmap(z=[np.linspace(0, 1, 1000)], x=wavelengths, colorscale='Rainbow', showscale=False, hoverinfo='skip'), row=1, col=1)
    if spectrum_type == "흡수 스펙트럼":
        for p in element_data[selected_element]:
            fig.add_shape(type="line", x0=p, y0=-0.5, x1=p, y1=0.5, line=dict(color="black", width=5), row=1, col=1)

# [하단 에너지 그래프] 선명한 검은색
fig.add_trace(go.Scatter(x=wavelengths, y=intensity, mode='lines', line=dict(color='black', width=3), name='에너지 세기'), row=2, col=1)

fig.update_layout(
    template="plotly_white", height=500, showlegend=False,
    xaxis2=dict(title="파장 (nm)", range=[380, 750]),
    yaxis2=dict(title="빛의 에너지 세기", range=[-0.1, 1.1]),
    margin=dict(l=60, r=60, t=20, b=50)
)
fig.update_yaxes(range=[-0.5, 0.5], row=1, col=1, visible=False)
st.plotly_chart(fig, use_container_width=True)

# --- 3. 상세 학습 가이드 섹션 ---
st.divider()
st.subheader("📖 스펙트럼 핵심 개념 가이드")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🌈 연속 스펙트럼")
    st.write("**원리:** 고온의 고체나 액체, 또는 고밀도 기체(별의 광구 등)가 모든 파장의 빛을 방출할 때 나타납니다.")
    st.write("**특징:** 무지개처럼 모든 파장에서 끊김 없는 색의 띠가 나타나며, 에너지 그래프도 전 구간에서 높게 유지됩니다.")

with col2:
    st.markdown("### ✨ 방출 스펙트럼")
    st.write(f"**원리:** 에너지를 얻어 가열된 **고온의 저밀도 기체({selected_element if selected_element else '원소'})**가 안정한 상태로 돌아오며 빛을 내보낼 때 나타납니다.")
    st.write("**특징:** 검은색 배경에 몇 개의 밝은 선(휘선)이 나타나며, 그래프에서는 특정 파장에서 에너지가 솟구친 '산(Peak)'이 관찰됩니다.")

with col3:
    st.markdown("### 🌑 흡수 스펙트럼")
    st.write(f"**원리:** 고온의 별빛이 상대적으로 온도가 낮은 **저온의 기체({selected_element if selected_element else '원소'})**를 통과할 때, 특정 파장의 에너지를 흡수하며 나타납니다.")
    st.write("**특징:** 연속 스펙트럼(무지개) 위에 검은색 선이 나타나며, 그래프에서는 특정 파장의 에너지가 푹 꺼진 '골(Drip)'이 관찰됩니다.")

st.success("📝 **결론:** 같은 원소라면 방출 선의 위치와 흡수 선의 위치가 정확히 일치합니다. 이를 통해 우리는 멀리 떨어진 별의 대기 성분을 알아낼 수 있습니다.")

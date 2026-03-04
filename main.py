import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 페이지 설정 ---
st.set_page_config(layout="wide", page_title="고1 통합과학 스펙트럼 가상실험")
st.title("🔬 스펙트럼 생성 원리 및 빛의 굴절 탐구")

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

# --- 원소 데이터 ---
element_data = {
    "수소 (H)": [410.2, 434.1, 486.1, 656.3],
    "헬륨 (He)": [447.1, 501.6, 587.6, 667.8, 706.5],
    "나트륨 (Na)": [589.0, 589.6],
    "아르곤 (Ar)": [415.9, 420.1, 470.2, 560.7, 603.2, 696.5]
}

# --- 사이드바 설정 ---
st.sidebar.header("🛠️ 실험 장치 설정")
spectrum_type = st.sidebar.radio("1. 스펙트럼 종류", ("연속 스펙트럼", "방출 스펙트럼", "흡수 스펙트럼"))
selected_element = st.sidebar.selectbox("2. 기체 선택", list(element_data.keys())) if spectrum_type != "연속 스펙트럼" else None

# --- 1. 분광기 내부 경로 시각화 (물리적 굴절 반영) ---
st.subheader("1. 분광기 내부의 빛의 경로 (굴절과 분산)")
setup_fig = go.Figure()

# 기본 장치 (슬릿, 프리즘, 스크린)
setup_fig.add_shape(type="rect", x0=3, y0=0.8, x1=3.1, y1=1.2, fillcolor="black") # 슬릿
setup_fig.add_trace(go.Scatter(x=[5], y=[1], mode="markers", marker=dict(size=60, symbol="triangle-up", color="lightgray"), showlegend=False)) # 프리즘
setup_fig.add_shape(type="rect", x0=8, y0=0, x1=8.1, y1=1, fillcolor="gray", opacity=0.2) # 스크린 (아래쪽에 배치)

if spectrum_type == "연속 스펙트럼":
    setup_fig.add_trace(go.Scatter(x=[0.5], y=[1], mode="markers+text", marker=dict(size=40, color="orange", symbol="star"), text=["고온의 별"], textposition="bottom center"))
    # 광원 -> 프리즘 (수평)
    setup_fig.add_trace(go.Scatter(x=[0.7, 5], y=[1, 1], mode="lines", line=dict(color="orange", width=3)))
    
    # [핵심 수정] 프리즘 -> 스크린 (모두 아래로 꺾임)
    # y축 1.0에서 시작해서 모두 1.0보다 낮은 곳으로 도착
    rainbow_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'violet']
    y_arrivals = [0.9, 0.75, 0.6, 0.45, 0.3, 0.15] # 보라색(0.15)이 가장 많이 꺾임
    for color, y_end in zip(rainbow_colors, y_arrivals):
        setup_fig.add_trace(go.Scatter(x=[5, 8], y=[1, y_end], mode="lines", line=dict(color=color, width=2.5), opacity=0.8))

elif spectrum_type == "방출 스펙트럼":
    setup_fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers+text", marker=dict(size=40, color="cyan", symbol="circle"), text=[f"고온의 {selected_element}"]))
    setup_fig.add_trace(go.Scatter(x=[1.2, 5, 8], y=[1, 1, 0.5], mode="lines", line=dict(color="cyan", width=2, dash="dash")))

else: # 흡수 스펙트럼
    setup_fig.add_trace(go.Scatter(x=[0.3], y=[1], mode="markers", marker=dict(size=30, color="orange", symbol="star")))
    setup_fig.add_trace(go.Scatter(x=[1.5], y=[1], mode="markers+text", marker=dict(size=45, color="lightblue", symbol="circle-open", line=dict(width=4)), text=[f"저온의 {selected_element}"]))
    setup_fig.add_trace(go.Scatter(x=[0.5, 5, 8], y=[1, 1, 0.5], mode="lines", line=dict(color="orange", width=2, dash="dot")))

setup_fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False, range=[0, 1.5]), height=280, template="plotly_white", showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(setup_fig, use_container_width=True)

# --- 2. 결과 분석 (스펙트럼 및 검은색 에너지 그래프) ---
st.subheader("2. 관찰 결과 및 에너지 데이터 분석")

wavelengths = np.linspace(380, 750, 1000)
intensity = np.zeros_like(wavelengths)

if spectrum_type == "연속 스펙트럼":
    intensity = np.ones_like(wavelengths) * 0.8
elif spectrum_type == "방출 스펙트럼":
    for p in element_data[selected_element]:
        intensity += 0.8 * np.exp(-0.5 * ((wavelengths - p) / 1.5)**2)
else: # 흡수 스펙트럼
    intensity = np.ones_like(wavelengths) * 0.8
    for p in element_data[selected_element]:
        intensity -= 0.7 * np.exp(-0.5 * ((wavelengths - p) / 1.5)**2)

intensity = np.clip(intensity, 0, 1)

fig = make_subplots(rows=2, cols=1, row_heights=[0.35, 0.65], shared_xaxes=True, vertical_spacing=0.1)

# 상단 스펙트럼 띠
if spectrum_type == "방출 스펙트럼":
    fig.add_shape(type="rect", x0=380, y0=-0.5, x1=750, y1=0.5, fillcolor="black", line_width=0, row=1, col=1)
    for p in element_data[selected_element]:
        fig.add_shape(type="line", x0=p, y0=-0.5, x1=p, y1=0.5, line=dict(color=nm_to_rgb(p), width=4), row=1, col=1)
else:
    fig.add_trace(go.Heatmap(z=[np.linspace(0, 1, 1000)], x=wavelengths, colorscale='Rainbow', showscale=False, hoverinfo='skip'), row=1, col=1)
    if spectrum_type == "흡수 스펙트럼":
        for p in element_data[selected_element]:
            fig.add_shape(type="line", x0=p, y0=-0.5, x1=p, y1=0.5, line=dict(color="black", width=4), row=1, col=1)

# 하단 에너지 그래프 (검은색 선)
fig.add_trace(go.Scatter(x=wavelengths, y=intensity, mode='lines', line=dict(color='black', width=3)), row=2, col=1)

fig.update_layout(template="plotly_white", height=500, xaxis2=dict(title="파장 (nm)", range=[380, 750]), yaxis2=dict(title="에너지 세기", range=[-0.1, 1.1]), showlegend=False)
fig.update_yaxes(range=[-0.5, 0.5], row=1, col=1, visible=False)
st.plotly_chart(fig, use_container_width=True)

# --- 3. 교과 개념 상세 설명 ---
st.divider()
st.subheader("📖 오늘의 핵심 과학 개념")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("### 🌈 연속 스펙트럼\n고온의 물체가 모든 파장의 빛을 낼 때 나타납니다. **굴절률 차이**로 인해 보라색 쪽으로 갈수록 빛이 더 크게 굴절되어 무지개 띠가 생깁니다.")
with c2:
    st.markdown(f"### ✨ 방출 스펙트럼\n가열된 고온의 **{selected_element if selected_element else '기체'}**가 안정한 상태로 돌아가며 특정 에너지를 방출합니다. 그래프에 솟은 '산'이 곧 밝은 선입니다.")
with c3:
    st.markdown(f"### 🌑 흡수 스펙트럼\n백색광이 저온의 **{selected_element if selected_element else '기체'}**를 지날 때 특정 에너지가 흡수됩니다. 무지개의 '골' 부분에 검은 선이 나타납니다.")

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 페이지 설정 ---
st.set_page_config(layout="wide", page_title="고1 스펙트럼 탐구소")
st.title("🔬 고1 통합과학: 스펙트럼 생성 원리 탐구소")

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

# --- 데이터 ---
element_data = {
    "수소 (H)": [410.2, 434.1, 486.1, 656.3],
    "헬륨 (He)": [447.1, 501.6, 587.6, 667.8, 706.5],
    "나트륨 (Na)": [589.0, 589.6],
    "아르곤 (Ar)": [415.9, 420.1, 470.2, 560.7, 603.2, 696.5],
    "네온 (Ne)": [585.2, 588.2, 614.3, 640.2, 650.7, 703.2]
}

# --- 사이드바 조작 ---
st.sidebar.header("🛠️ 실험 장치 설정")
spectrum_type = st.sidebar.radio("1. 스펙트럼 종류 선택", ("연속 스펙트럼", "방출 스펙트럼", "흡수 스펙트럼"))
selected_element = None
if spectrum_type != "연속 스펙트럼":
    selected_element = st.sidebar.selectbox("2. 기체 종류 선택", list(element_data.keys()))

# --- 1. 분광기 내부 모식도 ---
st.subheader("1. 분광기 내부 구조")
setup_fig = go.Figure()
setup_fig.add_shape(type="rect", x0=3, y0=0.5, x1=3.2, y1=1.5, fillcolor="black") # 슬릿
setup_fig.add_trace(go.Scatter(x=[5], y=[1], mode="markers", marker=dict(size=60, symbol="triangle-up", color="lightgray"), showlegend=False)) # 프리즘
setup_fig.add_shape(type="rect", x0=8, y0=0, x1=8.2, y1=2, fillcolor="white") # 스크린

if spectrum_type == "연속 스펙트럼":
    setup_fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers+text", marker=dict(size=40, color="yellow", symbol="star"), text=["광원(별)"], textposition="bottom center"))
    setup_fig.add_trace(go.Scatter(x=[1.2, 2.9], y=[1, 1], mode="lines", line=dict(color="yellow", width=4)))
elif spectrum_type == "방출 스펙트럼":
    setup_fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers+text", marker=dict(size=40, color="cyan", symbol="circle"), text=[f"고온의 {selected_element}"], textposition="bottom center"))
else: # 흡수 스펙트럼
    setup_fig.add_trace(go.Scatter(x=[0.5], y=[1], mode="markers", marker=dict(size=30, color="yellow", symbol="star")))
    setup_fig.add_trace(go.Scatter(x=[2], y=[1], mode="markers+text", marker=dict(size=40, color="lightblue", symbol="circle-open", line=dict(width=3)), text=[f"저온의 {selected_element}"], textposition="bottom center"))

setup_fig.update_layout(xaxis=dict(range=[0, 9], visible=False), yaxis=dict(range=[0, 2], visible=False), height=180, margin=dict(l=0, r=0, t=0, b=0), template="plotly_white", showlegend=False)
st.plotly_chart(setup_fig, use_container_width=True)

# --- 2. 분석 결과 시각화 ---
st.subheader("2. 관찰 결과 분석")

wavelengths = np.linspace(380, 750, 1000)
intensity = np.zeros_like(wavelengths)

if spectrum_type == "연속 스펙트럼":
    intensity = np.ones_like(wavelengths) * 0.9
elif spectrum_type == "방출 스펙트럼":
    for p in element_data[selected_element]:
        intensity += 0.9 * np.exp(-0.5 * ((wavelengths - p) / 1.5)**2)
elif spectrum_type == "흡수 스펙트럼":
    intensity = np.ones_like(wavelengths) * 0.9
    for p in element_data[selected_element]:
        intensity -= 0.8 * np.exp(-0.5 * ((wavelengths - p) / 1.5)**2)

intensity = np.clip(intensity, 0, 1)

fig = make_subplots(rows=2, cols=1, row_heights=[0.3, 0.7], shared_xaxes=True, vertical_spacing=0.08)

# 상단: 스펙트럼 바 구현
if spectrum_type == "방출 스펙트럼":
    # 완벽한 검은 배경
    fig.add_shape(type="rect", x0=380, y0=0, x1=750, y1=1, fillcolor="black", line_width=0, row=1, col=1)
    for p in element_data[selected_element]:
        fig.add_shape(type="line", x0=p, y0=0.1, x1=p, y1=0.9, line=dict(color=nm_to_rgb(p), width=5), row=1, col=1)
else:
    # 무지개 배경 (Heatmap)
    fig.add_trace(go.Heatmap(z=[np.linspace(0, 1, 1000)], x=wavelengths, colorscale='Rainbow', showscale=False, hoverinfo='skip'), row=1, col=1)
    if spectrum_type == "흡수 스펙트럼":
        for p in element_data[selected_element]:
            # 검은 선을 무지개 배경 내부에 정확히 그림
            fig.add_shape(type="line", x0=p, y0=0, x1=p, y1=1, line=dict(color="black", width=5), row=1, col=1)

# 하단: 에너지 그래프 (흰색 굵은 선)
fig.add_trace(go.Scatter(x=wavelengths, y=intensity, mode='lines', line=dict(color='white', width=4), name='에너지 세기'), row=2, col=1)

fig.update_layout(
    template="plotly_dark", height=550, showlegend=False,
    xaxis2=dict(title="파장 (nm)", range=[380, 750], showgrid=True),
    yaxis2=dict(title="빛의 세기", range=[-0.05, 1.1], showgrid=True), # 0 이하 범위를 살짝 주어 선이 잘 보이게 함
    margin=dict(l=50, r=50, t=30, b=50)
)

st.plotly_chart(fig, use_container_width=True)

# 학생용 탐구 가이드
st.info(f"🔎 **데이터 리터러시 활동:** 하단 그래프에서 값이 변하는 지점과 상단 스펙트럼 선의 위치를 대조해 보세요. " + 
        ("에너지가 솟구친 곳에 밝은 선이 있나요?" if spectrum_type == "방출 스펙트럼" else "에너지가 푹 꺼진 곳에 검은 선이 있나요?"))

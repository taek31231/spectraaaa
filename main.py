import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 페이지 설정 ---
st.set_page_config(layout="wide", page_title="고1 스펙트럼 탐구소")
st.title("🔬 고1 통합과학: 스펙트럼 생성 원리 탐구소")
st.markdown("분광기 내부를 조작하며 연속, 방출, 흡수 스펙트럼의 원리를 알아봅시다.")

# --- 파장별 실제 가시광선 색상 반환 함수 ---
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
    "아르곤 (Ar)": [415.9, 420.1, 470.2, 560.7, 603.2, 696.5],
    "네온 (Ne)": [585.2, 588.2, 614.3, 640.2, 650.7, 703.2]
}

# --- 사이드바 설정 ---
st.sidebar.header("🛠️ 실험 장치 설정")
spectrum_type = st.sidebar.radio("1. 스펙트럼 종류 선택", ("연속 스펙트럼", "방출 스펙트럼", "흡수 스펙트럼"))
selected_element = None
if spectrum_type != "연속 스펙트럼":
    selected_element = st.sidebar.selectbox("2. 기체 종류 선택", list(element_data.keys()))

# --- 1. 분광기 내부 모식도 시각화 ---
st.subheader("1. 분광기 내부 구조")
setup_fig = go.Figure()

# 기본 구성 요소 (슬릿, 프리즘, 스크린)
setup_fig.add_shape(type="rect", x0=3, y0=0.5, x1=3.2, y1=1.5, fillcolor="black") # 슬릿
setup_fig.add_trace(go.Scatter(x=[5], y=[1], mode="markers", marker=dict(size=60, symbol="triangle-up", color="lightgray"), showlegend=False)) # 프리즘
setup_fig.add_shape(type="rect", x0=8, y0=0, x1=8.2, y1=2, fillcolor="white") # 스크린

# 광원 및 기체 배치 로직
if spectrum_type == "연속 스펙트럼":
    setup_fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers+text", marker=dict(size=40, color="yellow", symbol="star"), text=["고온의 별"], textposition="bottom center", name="광원"))
    setup_fig.add_trace(go.Scatter(x=[1.2, 2.9], y=[1, 1], mode="lines", line=dict(color="yellow", width=4), showlegend=False))
elif spectrum_type == "방출 스펙트럼":
    setup_fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers+text", marker=dict(size=40, color="cyan", symbol="circle"), text=[f"고온의 {selected_element}"], textposition="bottom center", name="고온 기체"))
    setup_fig.add_trace(go.Scatter(x=[1.2, 2.9], y=[1, 1], mode="lines", line=dict(color="cyan", width=2, dash="dash"), showlegend=False))
else: # 흡수 스펙트럼
    setup_fig.add_trace(go.Scatter(x=[0.5], y=[1], mode="markers", marker=dict(size=30, color="yellow", symbol="star"), name="광원"))
    setup_fig.add_trace(go.Scatter(x=[2], y=[1], mode="markers+text", marker=dict(size=40, color="lightblue", symbol="circle-open", line=dict(width=3)), text=[f"저온의 {selected_element}"], textposition="bottom center", name="저온 기체"))
    setup_fig.add_trace(go.Scatter(x=[0.7, 1.8], y=[1, 1], mode="lines", line=dict(color="yellow", width=4), showlegend=False))
    setup_fig.add_trace(go.Scatter(x=[2.2, 2.9], y=[1, 1], mode="lines", line=dict(color="yellow", width=2, dash="dot"), showlegend=False))

setup_fig.update_layout(xaxis=dict(range=[0, 9], visible=False), yaxis=dict(range=[0, 2], visible=False), height=200, margin=dict(l=0, r=0, t=0, b=0), template="plotly_white")
st.plotly_chart(setup_fig, use_container_width=True)

# --- 2. 스펙트럼 및 그래프 시각화 ---
st.subheader("2. 관찰 결과 분석")

wavelengths = np.linspace(380, 750, 1000)
intensity = np.zeros_like(wavelengths)

if spectrum_type == "연속 스펙트럼":
    intensity = np.ones_like(wavelengths) * 0.9
elif spectrum_type == "방출 스펙트럼":
    for p in element_data[selected_element]:
        intensity += np.exp(-0.5 * ((wavelengths - p) / 1.2)**2)
    intensity = np.clip(intensity, 0, 1)
else: # 흡수 스펙트럼
    intensity = np.ones_like(wavelengths) * 0.9
    for p in element_data[selected_element]:
        intensity -= 0.7 * np.exp(-0.5 * ((wavelengths - p) / 1.2)**2)

fig = make_subplots(rows=2, cols=1, row_heights=[0.3, 0.7], shared_xaxes=True, vertical_spacing=0.05)

# 상단: 스펙트럼 바
if spectrum_type == "방출 스펙트럼":
    fig.add_shape(type="rect", x0=380, y0=0, x1=750, y1=1, fillcolor="black", line_width=0, row=1, col=1)
    for p in element_data[selected_element]:
        fig.add_shape(type="line", x0=p, y0=0, x1=p, y1=1, line=dict(color=nm_to_rgb(p), width=4), row=1, col=1)
else:
    fig.add_trace(go.Heatmap(z=[np.linspace(0, 1, 1000)], x=wavelengths, colorscale='Rainbow', showscale=False, hoverinfo='skip'), row=1, col=1)
    if spectrum_type == "흡수 스펙트럼":
        for p in element_data[selected_element]:
            fig.add_shape(type="line", x0=p, y0=0, x1=p, y1=1, line=dict(color="black", width=4), row=1, col=1)

# 하단: 에너지 그래프 (흰색 선으로 확실히 표현)
fig.add_trace(go.Scatter(x=wavelengths, y=intensity, mode='lines', line=dict(color='white', width=3), name='에너지 세기'), row=2, col=1)

fig.update_layout(template="plotly_dark", height=500, showlegend=False, 
                  xaxis2=dict(title="파장 (nm)", range=[380, 750]), 
                  yaxis2=dict(title="빛의 세기 (에너지)", range=[0, 1.1]))
st.plotly_chart(fig, use_container_width=True)

# 원리 설명 안내
with st.expander("💡 과학적 원리 보기"):
    if spectrum_type == "연속 스펙트럼":
        st.write("고온의 물체는 모든 파장의 빛을 내보냅니다. 그래프가 끊김 없이 높게 유지되는 것을 확인하세요.")
    elif spectrum_type == "방출 스펙트럼":
        st.write(f"고온의 {selected_element} 기체는 특정 파장의 에너지만 방출합니다. 그래프의 '산(Peak)' 위치와 위쪽의 밝은 선의 위치가 일치합니다.")
    else:
        st.write(f"별빛이 저온의 {selected_element} 기체를 통과할 때 특정 에너지가 흡수됩니다. 그래프의 '골(Drip)' 위치와 위쪽의 검은 선의 위치가 일치합니다.")

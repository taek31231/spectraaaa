import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 페이지 설정 ---
st.set_page_config(layout="wide", page_title="고1 스펙트럼 탐구소")
st.title("🔬 고1 통합과학: 스펙트럼 생성 원리 탐구소")
st.markdown("분광기 내부를 조작하며 연속, 방출, 흡수 스펙트럼의 원리를 알아봅시다.")

# --- 데이터 영역: 원소별 고유 파장 (unit: nm) ---
# 실제 NIST 데이터를 기반으로 한 주요 가시광선 영역 파장
element_data = {
    "수소 (H)": [410.2, 434.1, 486.1, 656.3],
    "헬륨 (He)": [388.9, 447.1, 501.6, 587.6, 667.8, 706.5],
    "나트륨 (Na)": [589.0, 589.6], # D-line
    "아르곤 (Ar)": [415.9, 420.1, 470.2, 560.7, 603.2, 696.5, 763.5],
    "네온 (Ne)": [540.1, 585.2, 588.2, 609.6, 614.3, 640.2, 650.7, 692.9, 703.2]
}

# --- 사이드바: 조작 및 설명 섹션 ---
st.sidebar.header("🛠️ 실험 장치 설정")

# 1. 스펙트럼 종류 선택
spectrum_type = st.sidebar.radio(
    "1. 스펙트럼 종류를 선택하세요.",
    ("연속 스펙트럼", "방출 스펙트럼", "흡수 스펙트럼")
)

# 2. 원소 선택 (방출/흡수 모드에서만 활성화)
selected_element = None
if spectrum_type != "연속 스펙트럼":
    selected_element = st.sidebar.selectbox(
        "2. 기체의 종류를 선택하세요.",
        list(element_data.keys())
    )

st.sidebar.markdown("---")
st.sidebar.header("💡 원리 쏙쏙!")

# 원리 설명 매핑
if spectrum_type == "연속 스펙트럼":
    st.sidebar.info(
        "**[고온의 별/백색광]**\n\n"
        "뜨거운 물체는 모든 에너지 영역의 빛을 내보내요. "
        "그래서 프리즘을 통과하면 빈틈없는 무지개색 띠가 나타납니다.\n\n"
        "👉 그래프를 보면 모든 파장에서 에너지가 높죠?"
    )
elif spectrum_type == "방출 스펙트럼":
    st.sidebar.success(
        f"**[고온의 {selected_element} 기체]**\n\n"
        "에너지를 받아 불안정해진 기체 원자가 다시 안정해지면서, "
        "**자신만의 고유한 에너지**를 빛으로 내보냅니다.\n\n"
        "👉 검은 배경에 밝은색 선으로 나타나며, 원소의 '지문'과 같아요."
    )
else: # 흡수 스펙트럼
    st.sidebar.warning(
        f"**[백색광 + 저온의 {selected_element} 기체]**\n\n"
        "백색광이 차가운 기체를 통과할 때, 기체 원자가 "
        "**자기가 방출할 수 있는 특정 에너지**만 쏙 빼앗아(흡수) 갑니다.\n\n"
        "👉 무지개 띠에 검은색 선이 나타나며, 방출 선의 위치와 정확히 일치해요."
    )


# --- 메인 화면: 시각화 영역 ---

# 1. 분광기 내부 모식도 (간단한 도형으로 이미지화)
st.subheader("1. 분광기 내부 모습")

setup_fig = go.Figure()

# 기본 장치 (슬릿, 프리즘, 스크린)
setup_fig.add_shape(type="rect", x0=3, y0=0.5, x1=3.2, y1=1.5, fillcolor="black", line_color="black") # 슬릿
setup_fig.add_trace(go.Scatter(x=[3.1, 3.1], y=[0.5, 1.5], mode="text", text=["슬릿"], textposition="top center", showlegend=False))

setup_fig.add_trace(go.Scatter(x=[5], y=[1], mode="markers", marker=dict(size=60, symbol="triangle-up", color="lightgray"), name="프리즘", showlegend=False)) # 프리즘
setup_fig.add_trace(go.Scatter(x=[5], y=[1], mode="text", text=["프리즘"], textposition="bottom center", showlegend=False))

setup_fig.add_shape(type="rect", x0=8, y0=0, x1=8.2, y1=2, fillcolor="white", line_color="black") # 스크린
setup_fig.add_trace(go.Scatter(x=[8.1, 8.1], y=[0, 2], mode="text", text=["스크린"], textposition="top center", showlegend=False))

# 모드별 광원 및 기체 배치
if spectrum_type == "연속 스펙트럼":
    setup_fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers", marker=dict(size=50, color="yellow", symbol="star"), name="고온의 별 (백색광)", showlegend=True))
    setup_fig.add_trace(go.Scatter(x=[1, 3], y=[1, 1], mode="lines", line=dict(color="yellow", width=4), showlegend=False)) # 광선

elif spectrum_type == "방출 스펙트럼":
    setup_fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers", marker=dict(size=40, color="cyan", symbol="circle"), name=f"고온의 {selected_element}", showlegend=True))
    setup_fig.add_trace(go.Scatter(x=[1, 3], y=[1, 1], mode="lines", line=dict(color="cyan", width=3, dash="dash"), showlegend=False)) # 광선 (점선)

else: # 흡수 스펙트럼
    setup_fig.add_trace(go.Scatter(x=[0.5], y=[1], mode="markers", marker=dict(size=40, color="yellow", symbol="star"), name="고온의 별 (백색광)", showlegend=True))
    setup_fig.add_trace(go.Scatter(x=[2], y=[1], mode="markers", marker=dict(size=40, color="lightblue", symbol="circle-open", line=dict(width=3)), name=f"저온의 {selected_element}", showlegend=True))
    setup_fig.add_trace(go.Scatter(x=[0.5, 1.8], y=[1, 1], mode="lines", line=dict(color="yellow", width=4), showlegend=False)) # 별빛
    setup_fig.add_trace(go.Scatter(x=[2.2, 3], y=[1, 1], mode="lines", line=dict(color="yellow", width=2, dash="dot"), showlegend=False)) # 통과한 빛

setup_fig.update_layout(
    xaxis=dict(range=[0, 9], showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(range=[0, 2], showgrid=False, zeroline=False, showticklabels=False),
    height=250, margin=dict(l=0, r=0, t=0, b=0),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    template="plotly_white"
)
st.plotly_chart(setup_fig, use_container_width=True)


# --- 데이터 영역: 스펙트럼 및 그래프 생성 ---
st.subheader("2. 관찰 결과 (스펙트럼 및 에너지 그래프)")

wavelengths = np.linspace(380, 780, 1000) # 가시광선 파장 영역
intensity = np.zeros_like(wavelengths)

# 가시광선 영역을 실제 무지개색으로 매핑하기 위한 컬러 스케일
rainbow_scale = [
    [0.00, 'rgb(120, 0, 140)'],  # Violet
    [0.15, 'rgb(0, 0, 255)'],    # Blue
    [0.35, 'rgb(0, 255, 0)'],    # Green
    [0.60, 'rgb(255, 255, 0)'],  # Yellow
    [0.80, 'rgb(255, 140, 0)'],  # Orange
    [1.00, 'rgb(255, 0, 0)']     # Red
]

# 스펙트럼 데이터 로직
if spectrum_type == "연속 스펙트럼":
    intensity = np.ones_like(wavelengths) * 0.8
    chart_title = "연속 스펙트럼"
    
elif spectrum_type == "방출 스펙트럼":
    peaks = element_data[selected_element]
    for p in peaks:
        intensity += np.exp(-0.5 * ((wavelengths - p) / 1.5)**2) # 가우시안 피크
    intensity = np.clip(intensity, 0, 1) # 세기 제한
    chart_title = f"{selected_element} 방출 스펙트럼"

else: # 흡수 스펙트럼
    intensity = np.ones_like(wavelengths) * 0.8
    peaks = element_data[selected_element]
    for p in peaks:
        intensity -= 0.6 * np.exp(-0.5 * ((wavelengths - p) / 1.5)**2) # 가우시안 골
    intensity = np.clip(intensity, 0, 1) # 세기 제한
    chart_title = f"{selected_element} 흡수 스펙트럼"


# --- 시각화 영역: 서브플롯 (Heatmap + Line) ---

fig = make_subplots(rows=2, cols=1, row_heights=[0.3, 0.7], shared_xaxes=True, vertical_spacing=0.05)

# 1. 상단: 스펙트럼 띠 (Heatmap)
# 방출 모드일 때는 배경을 검게 만들기 위해 특별한 처리
heatmap_intensity = intensity if spectrum_type != "방출 스펙트럼" else intensity * 10
colorscale = rainbow_scale if spectrum_type != "방출 스펙트럼" else 'Hot' # Hot 스케일이 어두운 배경에 밝은 선 표현에 좋음

fig.add_trace(go.Heatmap(
    z=[heatmap_intensity],
    x=wavelengths,
    colorscale=rainbow_scale if spectrum_type != "방출 스펙트럼" else 'Rainbow', # 임시로 Rainbow 사용
    showscale=False,
    hoverinfo='x'
), row=1, col=1)

# 방출 모드일 때 무지개색 선만 남기고 배경을 검게 만드는 요술
if spectrum_type == "방출 스펙트럼":
    # 검은색 배경 레이어 추가
    fig.add_shape(type="rect", x0=380, y0=0, x1=780, y1=1, fillcolor="black", line_color="black", opacity=0.9, row=1, col=1)
    # 실제 원소 파장 위치에만 무지개색 선 추가
    for p in element_data[selected_element]:
        p_norm = (p - 380) / (780 - 380) # 파장을 0~1로 정규화
        # 정규화된 파장에 해당하는 무지개 색상 가져오기 (간단한 매핑)
        line_color = f'rgb({int(255*np.clip(2*(p_norm-0.5),0,1))}, {int(255*(1-2*abs(p_norm-0.5)))}, {int(255*np.clip(2*(0.5-p_norm),0,1))})'
        
        # 헬륨/나트륨 등 노란색 영역 색상 보정
        if 560 < p < 600: line_color = 'rgb(255, 255, 0)'
        elif 600 <= p < 630: line_color = 'rgb(255, 165, 0)'

        fig.add_shape(type="line", x0=p, y0=0, x1=p, y1=1, line=dict(color=line_color, width=3), row=1, col=1)


# 2. 하단: 에너지 그래프 (Line)
fig.add_trace(go.Scatter(
    x=wavelengths,
    y=intensity,
    mode='lines',
    line=dict(color='white', width=2.5),
    name='빛의 세기',
    hovertemplate='파장: %{x:.1f} nm<br>세기: %{y:.2f}'
), row=2, col=1)


# --- 그래프 레이아웃 설정 (데이터 리터러시 강조) ---
fig.update_layout(
    title=chart_title,
    template="plotly_dark",
    xaxis2_title="파장 (nm)",
    yaxis2_title="빛의 세기 (에너지)",
    yaxis_showticklabels=False, # 상단 히트맵 Y축 라벨 숨김
    xaxis_range=[380, 780],
    yaxis2_range=[0, 1.1],
    height=550, margin=dict(l=50, r=50, t=50, b=50),
    hovermode='x'
)

st.plotly_chart(fig, use_container_width=True)


# --- 데이터 해석 연습 (수업 활용 팁) ---
with st.expander("🧐 데이터 해석 연습 (클릭해서 확인)"):
    st.markdown(
        f"현재 관찰하는 **{chart_title}**의 그래프 모양을 잘 보세요.\n\n"
    )
    if spectrum_type == "방출 스펙트럼":
        st.markdown(
            "1. 에너지 그래프의 **솟구친 부분(Peak)**의 파장 값을 마우스로 확인해 보세요.\n"
            f"2. 위에 보이는 **{selected_element} 원소의 고유 지문**인 밝은색 선의 위치와 일치하나요?\n"
            "3. 이 원소는 이 파장대의 에너지를 내보내고(방출) 있다는 뜻입니다."
        )
    elif spectrum_type == "흡수 스펙트럼":
        st.markdown(
            "1. 에너지 그래프의 **푹 파인 부분(Drip)**의 파장 값을 마우스로 확인해 보세요.\n"
            f"2. 위에 보이는 **{selected_element} 원소의 지문**인 검은색 선의 위치와 일치하나요?\n"
            "3. 차가운 기체가 백색광에서 이 파장대의 에너지 만 쏙 빼앗아(흡수) 갔다는 뜻입니다."
        )
    else: # 연속 스펙트럼
        st.markdown(
            "1. 에너지 그래프가 어떤가요? 모든 파장에서 **끊김 없이 높은 에너지**를 보여주나요?\n"
            "2. 위에 보이는 무지개 띠가 빈틈없이 연결된 것과 데이터가 일치하나요?"
        )

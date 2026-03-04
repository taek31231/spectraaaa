import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("🌟 통합과학: 스펙트럼 생성 원리 탐구")

# 1. 사이드바 조작 설정
st.sidebar.header("실험 설정")
setup = st.sidebar.radio("어떤 관찰을 할까요?", 
    ["무지개 별 관찰 (연속)", "뜨거운 기체 관찰 (방출)", "별빛과 차가운 기체 (흡수)"])

# 2. 데이터 생성 (고1 수준의 직관적 모델링)
x = np.linspace(400, 750, 800) # 가시광선 파장 영역
y = np.zeros_like(x)

if setup == "무지개 별 관찰 (연속)":
    y = np.ones_like(x) * 0.8 # 모든 파장에서 에너지가 높음
    info = "고온의 물체에서 모든 파장의 빛이 방출되어 연속적인 무지개가 나타납니다."
    
elif setup == "뜨거운 기체 관찰 (방출)":
    # 수소 원자의 특정 에너지 방출 예시
    y = np.exp(-0.5 * ((x-656)/2)**2) + np.exp(-0.5 * ((x-486)/2)**2)
    info = "고온의 기체가 특정 파장의 에너지만 방출하여 밝은 선이 나타납니다."

else: # 흡수 스펙트럼
    y = 0.8 - (np.exp(-0.5 * ((x-656)/2)**2) + np.exp(-0.5 * ((x-486)/2)**2))
    info = "연속 스펙트럼의 빛이 저온의 기체를 통과할 때 특정 파장이 흡수되어 검은 선이 나타납니다."

# 3. 그래프 시각화 (데이터 리터러시 강조)
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='white', width=2)))

fig.update_layout(
    title=f"현재 관찰 결과: {setup}",
    xaxis_title="파장 (nm)", yaxis_title="빛의 세기 (에너지)",
    template="plotly_dark",
    yaxis=dict(range=[0, 1.1])
)

st.plotly_chart(fig, use_container_width=True)
st.success(info)

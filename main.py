import streamlit as st
import pandas as pd
import numpy as np
from datetime import time

# 페이지 기본 설정
st.set_page_config(page_title="글로벌 MBTI 분석 대시보드", layout="wide")

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    return pd.read_csv('countries_mbti.csv')

try:
    df = load_data()
except FileNotFoundError:
    st.error("🚨 'countries_mbti.csv' 파일을 찾을 수 없습니다. 전처리 코드를 먼저 실행해 주세요!")
    st.stop()

# 사이드바 메뉴 구성 (4번째 메뉴 추가)
st.sidebar.title("📌 네비게이션")
menu = st.sidebar.radio(
    "이동할 페이지를 선택하세요:",
    [
        "1) 대시보드 설명 (main)", 
        "2) 국가별 MBTI 현황", 
        "3) MBTI 유형별 국가 비교",
        "4) MBTI 퀴즈 & 팩트체크 (New)"
    ]
)

# =========================================================================
# 1) main.py 대시보드 설명 화면
# =========================================================================
if menu == "1) 대시보드 설명 (main)":
    st.title("🗺️ 글로벌 MBTI 데이터 분석 대시보드")
    st.markdown("---")
    st.subheader("📊 데이터셋 안내")
    st.write("본 대시보드는 전 세계 국가들의 MBTI 유형별 분포 비율 데이터를 시각화하고 비교 분석합니다.")
    st.write(f"현재 로드된 데이터에는 총 **{len(df)}개 국가**와 **16가지 핵심 MBTI 유형**의 비율 정보가 포함되어 있습니다.")
    st.markdown("### 🔍 전처리된 데이터 미리보기 (`countries_mbti.csv`)")
    st.dataframe(df.head(10), use_container_width=True)

# =========================================================================
# 2) 국가별MBTI.py 화면
# =========================================================================
elif menu == "2) 국가별 MBTI 현황":
    st.title("📍 국가별 MBTI 현황 조회")
    st.markdown("---")
    countries = sorted(df['Country'].unique())
    selected_country = st.selectbox("조회할 국가를 선택하세요:", countries)
    
    country_data = df[df['Country'] == selected_country].drop(columns=['Country']).iloc[0]
    country_df = pd.DataFrame({
        'MBTI': country_data.index,
        '비율 (%)': country_data.values * 100
    }).sort_values(by='비율 (%)', ascending=False)
    
    st.subheader(f"✨ {selected_country}의 MBTI 특징")
    top_mbti = country_df.iloc[0]['MBTI']
    top_val = country_df.iloc[0]['비율 (%)']
    st.write(f"{selected_country}에서 가장 높은 비율을 차지하는 MBTI 유형은 **{top_mbti}**입니다. (약 {top_val:.2f}%)")
    
    st.markdown("### 📊 MBTI 분포 차트")
    st.bar_chart(country_df.set_index('MBTI'), y='비율 (%)', color="#4A90E2")

# =========================================================================
# 3) MBTI비교.py 화면
# =========================================================================
elif menu == "3) MBTI 유형별 국가 비교":
    st.title("🔀 MBTI 유형별 국가 비교")
    st.markdown("---")
    mbti_types = list(df.columns)
    mbti_types.remove('Country')
    selected_mbti = st.selectbox("비교할 MBTI 유형을 선택하세요:", sorted(mbti_types))
    
    compare_df = df[['Country', selected_mbti]].copy()
    compare_df['비율 (%)'] = compare_df[selected_mbti] * 100
    compare_df = compare_df.sort_values(by='비율 (%)', ascending=False)
    
    top_n = st.slider("확인할 상위 국가 수를 조절하세요:", min_value=5, max_value=30, value=15)
    top_countries = compare_df.head(top_n)
    
    st.subheader(f"👑 {selected_mbti} 비율이 가장 높은 상위 {top_n}개국")
    st.line_chart(top_countries.set_index('Country')[['비율 (%)']], color="#FF4B4B")
    st.dataframe(top_countries[['Country', '비율 (%)']].reset_index(drop=True), use_container_width=True)

# =========================================================================
# 4) MBTI 퀴즈 & 팩트체크 화면 (요청하신 기능 반영)
# =========================================================================
elif menu == "4) MBTI 퀴즈 & 팩트체크 (New)":
    st.title("❓ 데이터로 보는 MBTI 퀴즈")
    st.write("데이터 속에 숨겨진 재미있는 흥미 요소를 퀴즈로 풀어보세요!")
    st.markdown("---")

    # --- Q1. ISFJ 상위 10개 나라 ---
    st.subheader("💡 Q1. 전 세계에서 'ISFJ' 비율이 가장 높은 나라는 어디일까요?")
    q1_answer = st.button("정답 확인하기 (Q1)")
    
    if q1_answer:
        # 데이터에서 ISFJ 상위 10개국 정렬 및 추출
        isfj_top10 = df[['Country', 'ISFJ']].copy()
        isfj_top10['비율 (%)'] = isfj_top10['ISFJ'] * 100
        isfj_top10 = isfj_top10.sort_values(by='비율 (%)', ascending=False).head(10).reset_index(drop=True)
        
        # 1위 국가 강조
        top_1_country = isfj_top10.iloc[0]['Country']
        top_1_val = isfj_top10.iloc[0]['비율 (%)']
        
        st.success(f"🎉 정답은 **{top_1_country}** ({top_1_val:.2f}%) 입니다!")
        
        # 상위 10개국 차트 시각화
        st.write("📊 **ISFJ 비율 상위 10개국 현황:**")
        st.bar_chart(isfj_top10.set_index('Country')[['비율 (%)']], color="#2ECC71")
    
    st.markdown("---")

    # --- Q2. 전 세계 평균 1위 MBTI (자체 추가) ---
    st.subheader("💡 Q2. 전 세계 모든 국가를 통틀어 '평균 비율이 가장 높은' MBTI 유형은 무엇일까요?")
    q2_choice = st.selectbox("예상하는 MBTI를 골라보세요:", ["선택하세요", "INFP", "ENFP", "INFJ", "ISFJ"])
    
    if q2_choice != "선택하세요":
        # 전 세계 평균 구하기
        mbti_cols = df.drop(columns=['Country'])
        global_mean = (mbti_cols.mean() * 100).sort_values(ascending=False)
        global_top1 = global_mean.index[0]
        
        if q2_choice == global_top1:
            # --- Q2. 전 세계 평균 1위 MBTI ---
    st.subheader("💡 Q2. 전 세계 모든 국가를 통틀어 '평균 비율이 가장 높은' MBTI 유형은 무엇일까요?")
    q2_choice = st.selectbox("예상하는 MBTI를 골라보세요
            
        # 전체 평균 분포도 슬쩍 보여주기
        with st.expander("🌐 전 세계 MBTI 평균 비율 순위 보기"):
            st.dataframe(pd.DataFrame({"평균 비율 (%)": global_mean}), use_container_width=True)

    st.markdown("---")

    # --- Q3. 대한민국의 1위 MBTI (자체 추가) ---
    st.subheader("💡 Q3. 그렇다면 우리 나라, '대한민국(South Korea)'에서 가장 많은 1위 MBTI는 무엇일까요?")
    q3_answer = st.button("정답 확인하기 (Q3)")
    
    if q3_answer:
        # 대한민국 데이터 추출
        korea_data = df[df['Country'] == 'South Korea']
        
        if not korea_data.empty:
            korea_mbti = korea_data.drop(columns=['Country']).iloc[0] * 100
            korea_mbti = korea_mbti.sort_values(ascending=False)
            
            kr_top1 = korea_mbti.index[0]
            kr_top1_val = korea_mbti.values[0]
            kr_top2 = korea_mbti.index[1]
            kr_top2_val = korea_mbti.values[1]
            
            st.info(f"🇰🇷 대한민국의 1위 MBTI 유형은 **{kr_top1}** ({kr_top1_val:.2f}%) 입니다!")
            st.write(f"참고로 2위는 **{kr_top2}** ({kr_top2_val:.2f}%)가 바짝 뒤를 잇고 있습니다.")
            
            # 대한민국 탑 5 유형 가로 차트
            st.bar_chart(pd.DataFrame(korea_mbti.head(5)), color="#F1C40F")
        else:
            st.warning("데이터셋에 'South Korea' 정보가 존재하지 않습니다.")

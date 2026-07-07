import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="글로벌 MBTI 분석 대시보드", layout="wide")

# 데이터 불러오기 함수 (캐싱 처리로 속도 최적화)
@st.cache_data
def load_data():
    return pd.read_csv('countries_mbti.csv')

try:
    df = load_data()
except FileNotFoundError:
    st.error("🚨 'countries_mbti.csv' 파일을 찾을 수 없습니다. 전처리 코드를 먼저 실행해 주세요!")
    st.stop()

# 사이드바 메뉴 구성
st.sidebar.title("📌 네비게이션")
menu = st.sidebar.radio(
    "이동할 페이지를 선택하세요:",
    ["1) 대시보드 설명 (main)", "2) 국가별 MBTI 현황", "3) MBTI 유형별 국가 비교"]
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
    
    # 데이터 미리보기 제공
    st.markdown("### 🔍 전처리된 데이터 미리보기 (`countries_mbti.csv`)")
    st.dataframe(df.head(10), use_container_width=True)
    
    # 활용 팁
    st.info("""
    💡 **이용 가이드**
    * 사이드바 메뉴에서 **'2) 국가별 MBTI 현황'**을 선택하면 특정 국가 내의 16가지 MBTI 분포를 가로 바 차트로 확인할 수 있습니다.
    * 사이드바 메뉴에서 **'3) MBTI 유형별 국가 비교'**를 선택하면 특정 MBTI 성향이 가장 높은 국가 순위를 라인 차트 및 막대 그래프로 한눈에 비교할 수 있습니다.
    """)

# =========================================================================
# 2) 국가별MBTI.py 화면
# =========================================================================
elif menu == "2) 국가별 MBTI 현황":
    st.title("📍 국가별 MBTI 현황 조회")
    st.markdown("---")
    
    # 국가 선택 드롭다운 (알파벳 순 정렬)
    countries = sorted(df['Country'].unique())
    selected_country = st.selectbox("조회할 국가를 선택하세요:", countries)
    
    # 선택된 국가의 데이터 추출
    country_data = df[df['Country'] == selected_country].drop(columns=['Country']).iloc[0]
    
    # 시각화를 위해 데이터프레임 형태로 가공 (비율을 백분율 %로 변환)
    country_df = pd.DataFrame({
        'MBTI': country_data.index,
        '비율 (%)': country_data.values * 100
    }).sort_values(by='비율 (%)', ascending=False)
    
    # 결과 요약 문구
    st.subheader(f"✨ {selected_country}의 MBTI 특징")
    top_mbti = country_df.iloc[0]['MBTI']
    top_val = country_df.iloc[0]['비율 (%)']
    st.write(f"{selected_country}에서 가장 높은 비율을 차지하는 MBTI 유형은 **{top_mbti}**입니다. (약 {top_val:.2f}%)")
    
    # 가로 바 차트 시각화
    st.markdown("### 📊 MBTI 분포 차트")
    # 인덱스를 MBTI로 설정하여 차트 축 이름을 깔끔하게 만듭니다.
    chart_data = country_df.set_index('MBTI')
    st.bar_chart(chart_data, y='비율 (%)', color="#4A90E2")

# =========================================================================
# 3) MBTI비교.py 화면
# =========================================================================
elif menu == "3) MBTI 유형별 국가 비교":
    st.title("🔀 MBTI 유형별 국가 비교")
    st.markdown("---")
    
    # MBTI 유형 선택 (Country 열 제외한 나머지 열 이름들)
    mbti_types = list(df.columns)
    mbti_types.remove('Country')
    selected_mbti = st.selectbox("비교할 MBTI 유형을 선택하세요:", sorted(mbti_types))
    
    # 선택된 MBTI를 기준으로 상위 국가 정렬 (비율 % 변환)
    compare_df = df[['Country', selected_mbti]].copy()
    compare_df['비율 (%)'] = compare_df[selected_mbti] * 100
    compare_df = compare_df.sort_values(by='비율 (%)', ascending=False)
    
    # 사용자 편의를 위한 상위 몇 개국을 볼지 슬라이더 추가
    top_n = st.slider("확인할 상위 국가 수를 조절하세요:", min_value=5, max_value=30, value=15)
    
    top_countries = compare_df.head(top_n)
    
    st.subheader(f"👑 {selected_mbti} 비율이 가장 높은 상위 {top_n}개국")
    
    # 라인 차트 요소를 융합하여 국가별 트렌드 라인/바 시각화
    # 스트림릿에서 X축에 국가명이 이쁘게 나오도록 인덱스 설정
    chart_data = top_countries.set_index('Country')[['비율 (%)']]
    
    # 요청하신 연속성 비교 및 경향을 파악하기 좋은 라인 차트 출력
    st.line_chart(chart_data, color="#FF4B4B")
    
    # 상세 데이터 테이블
    st.markdown("### 📋 상세 데이터 테이블")
    st.dataframe(top_countries[['Country', '비율 (%)']].reset_index(drop=True), use_container_width=True)

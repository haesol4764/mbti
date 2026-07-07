import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="안산시 인구 대시보드", layout="wide", initial_sidebar_state="expanded")

st.title("📊 안산시 인구 변화 인터랙티브 대시보드")
st.markdown("슬라이더와 필터를 조절하여 안산시의 인구 흐름을 다각도로 분석해보세요.")

# 1. 데이터 로드
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('population.csv')
        # 데이터 정제: 연도를 정수형으로 변환
        df['연도'] = df['연도'].astype(int)
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("⚠️ 'population.csv' 파일을 찾을 수 없습니다. GitHub 저장소에 데이터 파일이 올바르게 포함되어 있는지 확인해 주세요.")
    st.stop()

# --- 사이드바 콘트롤러 (슬라이더 및 필터) ---
st.sidebar.header("🎛️ 데이터 컨트롤러")

# 1. 연도 범위 슬라이더 (직접 좌우로 움직이는 슬라이더)
min_year = int(df['연도'].min())
max_year = int(df['연도'].max())

start_year, end_year = st.sidebar.slider(
    "📆 분석할 연도 범위를 선택하세요",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year), # 초기값: 전체 범위
    step=1
)

# 2. 행정동 멀티 선택 박스
all_dong = sorted(df['행정구역_동'].unique())
selected_dongs = st.sidebar.multiselect(
    "🏘️ 특정 동을 선택하여 비교해보세요 (미선택 시 전체 조회)",
    options=all_dong,
    default=[]
)

# --- 데이터 필터링 적용 ---
# 1. 슬라이더 기반 연도 필터링
df_filtered = df[(df['연도'] >= start_year) & (df['연도'] <= end_year)]

# 2. 멀티셀렉트 기반 동 필터링
if selected_dongs:
    df_filtered = df_filtered[df_filtered['행정구역_동'].isin(selected_dongs)]


# --- 메인 화면 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["📈 연도별 성별 추이", "🔥 인구 변동 극대화 동", "❄️ 인구 변동 최소화 동"])

# ==========================================
# TAB 1: 연도별 남성 여성 인구 변화 차이 비교
# ==========================================
with tab1:
    st.header(f"✨ {start_year}년 ~ {end_year}년 성별 인구 추이")
    
    # 연도별 남녀 인구 합계 계산
    annual_pop = df_filtered.groupby('연度')[['남자_인구수', '여자_인구수', '총인구수']].sum().reset_index()
    
    # 지표 요약(Metric) 시각화
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=f"{end_year}년 총인구 수", value=f"{int(annual_pop['총인구수'].iloc[-1]):,} 명

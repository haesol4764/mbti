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

# 1. 연도 범위 슬라이더
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
    annual_pop = df_filtered.groupby('연도')[['남자_인구수', '여자_인구수', '총인구수']].sum().reset_index()
    
    # 지표 요약(Metric) 시각화
    if not annual_pop.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label=f"{end_year}년 총인구 수", value=f"{int(annual_pop['총인구수'].iloc[-1]):,} 명")
        with col2:
            st.metric(label="남성 인구 비율", value=f"{annual_pop['남자_인구수'].iloc[-1] / annual_pop['총인구수'].iloc[-1] * 100:.1f} %")
        with col3:
            st.metric(label="여성 인구 비율", value=f"{annual_pop['여자_인구수'].iloc[-1] / annual_pop['총인구수'].iloc[-1] * 100:.1f} %")
            
        # 인터랙티브 라인 차트 생성
        st.subheader("📊 연도별 남녀 인구 추이 라인 차트")
        chart_data = annual_pop.set_index('연도')[['남자_인구수', '여자_인구수']]
        st.line_chart(chart_data, width='stretch')
        
        st.subheader("📋 데이터 상세 테이블")
        st.dataframe(annual_pop, width='stretch')
    else:
        st.warning("선택한 조건에 맞는 데이터가 없습니다.")


# --- 동별 변화량 계산 로직 (선택된 연도 기준) ---
# 안전한 필터링 및 병합 처리 (오타 전면 수정)
df_start = df_filtered[df_filtered['연도'] == start_year].groupby('행정구역_동')['총인구수'].sum().reset_index().rename(columns={'총인구수': '시작인구'})
df_end = df_filtered[df_filtered['연도'] == end_year].groupby('행정구역_동')['총인구수'].sum().reset_index().rename(columns={'총인구수': '종료인구'})

df_change = pd.merge(df_start, df_end, on='행정구역_동')

if not df_change.empty:
    df_change['순증감량'] = df_change['종료인구'] - df_change['시작인구']
    df_change['변화량_절댓값'] = df_change['순증감량'].abs()
    df_change['구분'] = df_change['순증감량'].apply(lambda x: "🔺 증가" if x > 0 else "🔻 감소")

    # ==========================================
    # TAB 2: 가장 많은 인구 변화가 일어난 동
    # ==========================================
    with tab2:
        st.header(f"🔥 {start_year}년 대비 인구 변화가 가장 컸던 동 (상위 5개)")
        most_changed = df_change.sort_values(by='변화량_절댓값', ascending=False).head(5)
        
        st.subheader("동별 순증감량 비교 (절댓값 기준 상위)")
        bar_chart_data = most_changed.set_index('행정구역_동')[['순증감량']]
        st.bar_chart(bar_chart_data, width='stretch')
        
        st.dataframe(most_changed[['행정구역_동', '시작인구', '종료인구', '순증감량', '구분']], width='stretch')

    # ==========================================
    # TAB 3: 가장 적은 인구 변화가 일어난 동
    # ==========================================
    with tab3:
        st.header(f"❄️ {start_year}년 대비 인구 변화가 가장 적었던 동 (상위 5개)")
        least_changed = df_change.sort_values(by='변화량_절댓값', ascending=True).head(5)
        
        st.subheader("동별 순증감량 비교 (절댓값 기준 하위)")
        bar_chart_data_least = least_changed.set_index('행정구역_동')[['순증감량']]
        st.bar_chart(bar_chart_data_least, width='stretch')
        
        st.dataframe(least_changed[['행정구역_동', '시작인구', '종료인구', '순증감량', '구분']], width='stretch')
else:
    with tab2:
        st.warning("동별 변화를 비교하기 위해 슬라이더의 시작 연도와 종료 연도를 다르게 설정해 주세요.")
    with tab3:
        st.warning("동별 변화를 비교하기 위해 슬라이더의 시작 연도와 종료 연도를 다르게 설정해 주세요.")

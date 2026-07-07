import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="글로벌 MBTI 데이터 분석", layout="wide")

st.title("📊 글로벌 MBTI 데이터 분석 대시보드")
st.write("`countries_mbti.csv` 데이터를 기반으로 한 분석 결과입니다.")

# 1. 데이터 불러오기
try:
    df = pd.read_csv('countries_mbti.csv')
    df_mbti = df.set_index('Country')
except FileNotFoundError:
    st.error("❌ 'countries_mbti.csv' 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
    st.stop()

# 탭 구조로 질문 나누기
tab1, tab2, tab3 = st.tabs(["질문 1: ISFJ 상위 10개국", "질문 2: 전 세계 가장 흔한 MBTI", "질문 3: 대한민국 1위 MBTI"])

# -------------------------------------------------------------------------
# TAB 1: ISFJ가 가장 많은 상위 10개 나라는?
# -------------------------------------------------------------------------
with tab1:
    st.header("📌 ISFJ 비율이 가장 높은 상위 10개 나라")
    
    # ISFJ 컬럼 기준 내림차순 정렬 후 상위 10개 추출
    top10_isfj = df_mbti['ISFJ'].sort_values(ascending=False).head(10)
    
    # 데이터프레임 변환 (보기 좋게 포맷팅)
    top10_df = top10_isfj.reset_index()
    top10_df.columns = ['국가 (Country)', 'ISFJ 비율']
    top10_df['ISFJ 비율'] = top10_df['ISFJ 비율'].map(lambda x: f"{x * 100:.2f}%")
    
    # Streamlit 표 및 차트 출력
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(top10_df, use_container_width=True)
    with col2:
        st.bar_chart(data=top10_isfj)

# -------------------------------------------------------------------------
# TAB 2: 전 세계에서 가장 흔하게 나타나는 MBTI 유형은?
# -------------------------------------------------------------------------
with tab2:
    st.header("📌 전 세계 평균 비율이 가장 높은 MBTI 유형")
    
    # ⚠️ [문법 오류 수정 반영 부분]
    # selectbox에 들어갈 MBTI 16가지 선택지 정의
    mbti_options = ["ENFJ", "ENFP", "ENTJ", "ENTP", "ESFJ", "ESFP", "ESTJ", "ESTP",
                    "INFJ", "INFP", "INTJ", "INTP", "ISFJ", "ISFP", "ISTJ", "ISTP"]
    
    # 기존에 따옴표가 닫히지 않아 에러가 났던 selectbox 수정 완료
    q2_choice = st.selectbox("정답을 보기 전에 예상하는 MBTI를 골라보세요!", options=mbti_options)
    st.write(f"선택하신 유형: **{q2_choice}**")
    
    # 실제 데이터 계산
    global_mbti_avg = df_mbti.mean().sort_values(ascending=False)
    most_common_mbti = global_mbti_avg.idxmax()
    most_common_value = global_mbti_avg.max()
    
    st.markdown("---")
    st.subheader("📊 실제 데이터 분석 결과")
    st.success(f"전 세계에서 가장 흔한 MBTI 유형은 **{most_common_mbti}** 입니다! (평균 비율: **{most_common_value * 100:.2f}%**)")
    
    # 전체 MBTI 평균 순위 차트
    st.write("  **전 세계 MBTI 평균 비율 순위**")
    st.bar_chart(global_mbti_avg)

# -------------------------------------------------------------------------
# TAB 3: 대한민국(South Korea)에서 가장 높은 비율을 차지하는 1위 MBTI 유형은?
# -------------------------------------------------------------------------
with tab3:
    st.header("📌 대한민국(South Korea) 내 1위 MBTI 유형")
    
    # 데이터셋 내의 국가명 매칭 처리 ('South Korea' 또는 유사 명칭)
    korea_row_name = 'South Korea'
    
    if korea_row_name in df_mbti.index:
        korea_mbti = df_mbti.loc[korea_row_name].sort_values(ascending=False)
        top_korea_mbti = korea_mbti.idxmax()
        top_korea_value = korea_mbti.max()
        
        st.success(f"대한민국에서 가장 높은 비율을 차지하는 1위 MBTI는 **{top_korea_mbti}** 입니다! (비율: **{top_korea_value * 100:.2f}%**)")
        
        # 한국인 MBTI 전체 분포 시각화
        korea_df = korea_mbti.reset_index()
        korea_df.columns = ['MBTI 유형', '비율']
        korea_df['비율'] = korea_df['비율'].map(lambda x: f"{x * 100:.2f}%")
        
        st.write("  **대한민국 MBTI 유형별 전체 비율 순위**")
        st.dataframe(korea_df, use_container_width=True)
        
    else:
        st.warning(f"⚠️ 데이터셋에서 '{korea_row_name}' 국가를 찾을 수 없습니다.")
        # 유사한 이름이 있는지 검색해서 보여줌
        possible_names = [name for name in df_mbti.index if 'Korea' in str(name)]
        if possible_names:
            st.info(f"💡 데이터에 다음과 같은 유사한 이름이 존재합니다: {possible_names}. 코드의 `korea_row_name` 변수를 이 중 하나로 수정해보세요.")

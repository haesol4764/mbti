import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (데이터 시각화 시 한글 깨짐 방지)
# 운영체제나 서버 환경에 따라 폰트 경로가 다를 수 있습니다.
plt.rcParams['font.family'] = 'Malgun Gothic' # Windows 기준
plt.rcParams['axes.unicode_minus'] = False

st.title("📊 안산시 인구 변화 데이터 분석 앱")

# 1. 데이터 불러오기
try:
    df = pd.read_csv('population.csv')
    st.success("데이터를 성공적으로 불러왔습니다!")
except FileNotFoundError:
    st.error("보유하신 'population.csv' 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
    st.stop()

# --- 1. 연도별 남성 여성 인구 변화 차이 비교 ---
st.header("1. 연도별 남성 및 여성 인구 변화 차이")

# 연도별 남녀 인구 합계 계산
annual_pop = df.groupby('연도')[['남자_인구수', '여자_인구수', '총인구수']].sum().reset_index()

# Streamlit 데이터프레임 출력 (use_container_width 대신 width='stretch' 사용)
st.subheader("연도별 인구 데이터 테이블")
st.dataframe(annual_pop, width='stretch')

# 간단한 시각화 차트 추가
st.subheader("연도별 남녀 인구 추이 그래프")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(annual_pop['연도'], annual_pop['남자_인구수'], marker='o', label='남자 인구수', color='blue')
ax.plot(annual_pop['연도'], annual_pop['여자_인구수'], marker='o', label='여자 인구수', color='red')
ax.set_title("안산시 연도별 남녀 인구 변화")
ax.set_xlabel("연도")
ax.set_ylabel("인구 수 (명)")
ax.legend()
ax.grid(True)
st.pyplot(fig)


# --- 동별 인구 변화량 계산을 위한 데이터 정제 ---
# 가장 과거 연도(2016)와 가장 최근 연도(2024) 데이터 추출
df_2016 = df[df['연도'] == 2016][['행정구역_동', '총인구수']].rename(columns={'총인구수': '인구_2016'})
df_2024 = df[df['연도'] == 2024][['행정구역_동', '총인구수']].rename(columns={'총인구수': '인구_2024'})

# 두 데이터를 '행정구역_동' 기준으로 병합
df_change = pd.merge(df_2016, df_2024, on='행정구역_동')

# 변화량(절댓값)과 실제 증감량 계산
df_change['변화량_절댓값'] = (df_change['인구_2024'] - df_change['인구_2016']).abs()
df_change['순증감량'] = df_change['인구_2024'] - df_change['인구_2016']


# --- 2. 가장 많은 인구 변화가 일어난 동 ---
st.header("2. 가장 많은 인구 변화가 일어난 동 (상위 5개)")
most_changed = df_change.sort_values(by='변화량_절댓값', ascending=False).head(5)

# 가독성을 위해 포맷팅된 데이터프레임 생성
most_changed_display = most_changed.copy()
most_changed_display['구분'] = most_changed_display['순증감량'].apply(lambda x: "🔺 증가" if x > 0 else "🔻 감소")
most_changed_display = most_changed_display[['행정구역_동', '인구_2016', '인구_2024', '변화량_절댓값', '구분']]

st.dataframe(most_changed_display, width='stretch')


# --- 3. 가장 적은 인구 변화가 일어난 동 ---
st.header("3. 가장 적은 인구 변화가 일어난 동 (상위 5개)")
least_changed = df_change.sort_values(by='변화량_절댓값', ascending=True).head(5)

least_changed_display = least_changed.copy()
least_changed_display['구분'] = least_changed_display['순증감량'].apply(lambda x: "🔺 증가" if x > 0 else "🔻 감소")
least_changed_display = least_changed_display[['행정구역_동', '인구_2016', '인구_2024', '변화량_절댓값', '구분']]

st.dataframe(least_changed_display, width='stretch')

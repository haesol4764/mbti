import pandas as pd

# 1. 데이터 불러오기
# 파일 경로가 다를 경우 경로를 수정해주세요 (예: 'population.csv')
df = pd.read_csv('population.csv')

# --- 1. 연도별 남성 및 여성 인구 변화 차이 비교 ---
print("## 1. 연도별 남성/여성 인구 합계 변화")
annual_pop = df.groupby('연도')[['남자_인구수', '여자_인구수', '총인구수']].sum().reset_index()
print(annual_pop.to_string(index=False))
print("-" * 50)


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
print("## 2. 가장 많은 인구 변화가 일어난 동 (상위 3개)")
most_changed = df_change.sort_values(by='변화량_절댓값', ascending=False).head(3)
for idx, row in most_changed.iterrows():
    direction = "증가" if row['순증감량'] > 0 else "감소"
    print(f"동: {row['행정구역_동']} | 변화량: {int(row['변화량_절댓값'])}명 ({direction})")
print("-" * 50)


# --- 3. 가장 적은 인구 변화가 일어난 동 ---
print("## 3. 가장 적은 인구 변화가 일어난 동 (상위 3개)")
least_changed = df_change.sort_values(by='변화량_절댓값', ascending=True).head(3)
for idx, row in least_changed.iterrows():
    direction = "증가" if row['순증감량'] > 0 else "감소"
    print(f"동: {row['행정구역_동']} | 변화량: {int(row['변화량_절댓값'])}명 ({direction})")

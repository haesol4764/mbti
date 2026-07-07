import pandas as pd

# 1. 데이터 불러오기
# 파일 경로가 다를 경우 'countries_mbti.csv' 부분을 실제 경로로 수정해주세요.
df = pd.read_csv('countries_mbti.csv')

# 국가명을 인덱스로 설정하고, MBTI 비율 데이터만 추출
df_mbti = df.set_index('Country')

print("="*50)
print(" 데이터 분석 결과")
print("="*50)

# -------------------------------------------------------------------------
# 질문 1: ISFJ가 가장 많은 상위 10개 나라는?
# -------------------------------------------------------------------------
# ISFJ 컬럼을 기준으로 내림차순 정렬 후 상위 10개 선택
top10_isfj = df_mbti['ISFJ'].sort_values(ascending=False).head(10)

print("[질문 1] ISFJ 비율이 가장 높은 상위 10개 나라")
for i, (country, value) in enumerate(top10_isfj.items(), 1):
    print(f"{i}위. {country}: {value * 100:.2f}%")
print("-"*50)

# -------------------------------------------------------------------------
# 질문 2: 전 세계에서 가장 흔하게(평균 비율이 가장 높게) 나타나는 MBTI 유형은?
# -------------------------------------------------------------------------
# 각 MBTI 유형(컬럼)별 전 세계 평균 계산 후 가장 높은 유형 선택
global_mbti_avg = df_mbti.mean().sort_values(ascending=False)
most_common_mbti = global_mbti_avg.idxmax()
most_common_value = global_mbti_avg.max()

print("[질문 2] 전 세계에서 가장 흔한 MBTI 유형")
print(f"👉 결과: {most_common_mbti} (전 세계 평균 비율: {most_common_value * 100:.2f}%)")
print("-"*50)

# -------------------------------------------------------------------------
# 질문 3: 대한민국(South Korea)에서 가장 높은 비율을 차지하는 1위 MBTI 유형은?
# -------------------------------------------------------------------------
# 'South Korea' 행 데이터를 가져와서 가장 높은 값을 가진 컬럼 선택
# 데이터셋에 국가명이 'South Korea' 또는 'Korea, South' 등으로 되어 있을 수 있으므로 확인 필요
korea_row_name = 'South Korea' 

if korea_row_name in df_mbti.index:
    korea_mbti = df_mbti.loc[korea_row_name].sort_values(ascending=False)
    top_korea_mbti = korea_mbti.idxmax()
    top_korea_value = korea_mbti.max()
    
    print("[질문 3] 대한민국에서 가장 높은 비율을 차지하는 1위 MBTI")
    print(f"👉 결과: {top_korea_mbti} (대한민국 내 비율: {top_korea_value * 100:.2f}%)")
else:
    # 혹시 국가명이 다르게 표기되어 있을 경우를 위한 예외 처리
    print("[질문 3] 대한민국 데이터 확인 불가")
    print(f"'{korea_row_name}' 이름으로 된 국가를 찾을 수 없습니다. 데이터셋의 정확한 명칭을 확인해주세요.")
    # 'Korea'가 포함된 국가명 검색 예시
    possible_names = [name for name in df_mbti.index if 'Korea' in str(name)]
    print(f"참고(데이터 내 유사 이름): {possible_names}")

print("="*50)

"""뉴스레터 구독자 관심 분야와 AI 업무 자동화 선호도 설문 결과 페이지."""


import pandas as pd
import streamlit as st


st.title("📊 설문조사 결과")
st.info(
    "관심 인원은 복수 선택 결과를 분야별로 합산한 임시 값이므로 "
    "합계가 실제 응답자 수와 다를 수 있습니다."
)

survey_result = {
    "관심 분야": [
        "📣마케팅",
        "💻IT·개발",
        "🎮게임",
        "✈️여행",
        "💵경제",
    ],
    "관심 인원": [32, 28, 26, 21, 18],
    "AI 자동화 선호도": [4.6, 4.8, 4.1, 3.9, 4.3],
}

result_df = pd.DataFrame(survey_result)

total_respondents = 100
popular_row = result_df.loc[result_df["관심 인원"].idxmax()]
preferred_row = result_df.loc[
    result_df["AI 자동화 선호도"].idxmax()
]
average_score = result_df["AI 자동화 선호도"].mean()

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric("설문 참여자 인원", f"{total_respondents}명")

with metric2:
    st.metric("가장 관심도가 높은 분야", popular_row["관심 분야"])

with metric3:
    st.metric(
        "AI 자동화 선호도 1위",
        preferred_row["관심 분야"],
    )

with metric4:
    st.metric("평균 AI자동화 선호도", f"{average_score:.1f}점")

st.subheader("설문 결과")
st.dataframe(
    result_df,
    hide_index=True,
    use_container_width=True,
)

people_chart_df = result_df.set_index("관심 분야")[["관심 인원"]]
score_chart_df = result_df.set_index("관심 분야")[
    ["AI 자동화 선호도"]
]

st.subheader("관심 분야별 인원수 분포 비교")
st.bar_chart(people_chart_df)

st.subheader("관심 분야별 AI 업무 자동화 선호도")
st.line_chart(
    score_chart_df,
    y="AI 자동화 선호도",
)

st.caption("아래 결과는 화면 구성을 확인하기 위한 임시 데이터입니다.")

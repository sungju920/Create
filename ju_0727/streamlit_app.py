"""뉴스레터 설문 프로젝트의 Streamlit 멀티페이지 메인 앱."""

import streamlit as st


st.set_page_config(
    page_title="Newsletter Survey",
    page_icon="📝",
    layout="wide",
)

survey_page = st.Page(
    "survey.py",
    title="SURVEY",
    icon="📝",
    default=True,
)

select_page = st.Page(
    "select.py",
    title="SELECT",
    icon="📊",
)

request_page = st.Page(
    "request.py",
    title="REQUEST",
    icon="🤖",
)

pages = [survey_page, select_page, request_page]
navigation = st.navigation(pages, position="hidden")

with st.sidebar:
    st.header("메뉴")
    st.caption("메뉴를 선택해 페이지를 이동하세요.")
    st.divider()
    st.page_link(survey_page, use_container_width=True)
    st.page_link(select_page, use_container_width=True)
    st.page_link(request_page, use_container_width=True)

navigation.run()

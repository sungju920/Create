"""뉴스레터 구독자 관심 분야와 AI 업무 자동화 선호도 설문조사 페이지."""

import streamlit as st


INTEREST_OPTIONS = ["📣마케팅", "💻IT·개발", "🎮게임", "✈️여행","💵경제"]
FREQUENCY_OPTIONS = ["매일", "주 1회", "주 2~3회", "월 1~2회"]

SURVEY_DEFAULTS = {
    "newsletter_nickname": "",
    "newsletter_age": 20,
    "newsletter_interests": [],
    "newsletter_frequency": "주 1회",
    "newsletter_automation_score": 3,
    "newsletter_content_request": "",
    "newsletter_subscribe": True,
    "newsletter_survey_submitted": False,
    "newsletter_survey_result": {},
}


def initialize_survey_state():
    """설문 페이지에서 사용하는 세션 상태의 기본값을 준비한다."""
    for key, value in SURVEY_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value.copy() if isinstance(value, (list, dict)) else value


def reset_survey():
    """현재 설문 입력값과 제출 결과를 모두 초기화한다."""
    for key, value in SURVEY_DEFAULTS.items():
        st.session_state[key] = value.copy() if isinstance(value, (list, dict)) else value


def get_missing_fields():
    """입력되지 않은 필수 항목의 이름을 반환한다."""
    missing_fields = []

    if not st.session_state.newsletter_interests:
        missing_fields.append("관심 분야")
    if not st.session_state.newsletter_frequency:
        missing_fields.append("뉴스레터 수신 주기")

    return missing_fields


def save_survey_result():
    """현재 입력값을 설문 결과로 저장한다."""
    st.session_state.newsletter_survey_result = {
        "닉네임": st.session_state.newsletter_nickname.strip() or "익명",
        "나이": st.session_state.newsletter_age,
        "관심 분야": st.session_state.newsletter_interests.copy(),
        "수신 주기": st.session_state.newsletter_frequency,
        "AI 업무 자동화 선호도": st.session_state.newsletter_automation_score,
        "받고 싶은 콘텐츠": (
            st.session_state.newsletter_content_request.strip()
            or "입력하지 않음"
        ),
        "뉴스레터 구독": (
            "신청"
            if st.session_state.newsletter_subscribe
            else "신청하지 않음"
        ),
    }
    st.session_state.newsletter_survey_submitted = True


def show_survey_form():
    """설문 입력 화면을 출력한다."""
    st.title("📝 뉴스레터 구독 설문")
    st.info(
        "관심 분야와 AI 업무 자동화 선호도를 알려주세요. "
        "별표(*)가 있는 항목은 필수 입력 항목입니다."
    )

    with st.form("newsletter_survey_form"):
        st.text_input(
            "닉네임",
            key="newsletter_nickname",
            placeholder="사용할 닉네임을 입력하세요.",
        )

        st.number_input(
            "나이를 입력하세요",
            min_value=0,
            max_value=120,
            key="newsletter_age",
        )

        st.multiselect(
            "관심 분야 *",
            INTEREST_OPTIONS,
            key="newsletter_interests",
            placeholder="한 개 이상 선택하세요.",
        )

        st.selectbox(
            "뉴스레터 수신 주기 *",
            FREQUENCY_OPTIONS,
            key="newsletter_frequency",
        )

        st.slider(
            "AI 업무 자동화 선호도 ",
            min_value=1,
            max_value=5,
            key="newsletter_automation_score",
            help="1점은 전혀 선호하지 않음, 5점은 매우 선호함입니다.",
        )

        st.text_area(
            "받고 싶은 뉴스레터 콘텐츠",
            key="newsletter_content_request",
            placeholder="예: 개발 자동화 도구와 실제 업무 적용 사례",
        )

        st.checkbox(
            "뉴스레터를 구독하겠습니다.",
            key="newsletter_subscribe",
        )

        submit_col, reset_col = st.columns(2)

        with submit_col:
            submitted = st.form_submit_button(
                "설문 제출",
                type="primary",
                use_container_width=True,
            )

        with reset_col:
            st.form_submit_button(
                "초기화",
                on_click=reset_survey,
                use_container_width=True,
            )

    if submitted:
        missing_fields = get_missing_fields()

        if missing_fields:
            st.warning(
                "다음 필수 항목을 입력해 주세요: "
                + ", ".join(missing_fields)
            )
        else:
            save_survey_result()
            st.rerun()


def show_survey_result():
    """제출된 설문 결과를 출력한다."""
    result = st.session_state.newsletter_survey_result

    if not result:
        st.warning("표시할 설문 결과가 없습니다.")
        if st.button("설문으로 돌아가기", use_container_width=True):
            reset_survey()
            st.rerun()
        return

    st.title("✅ 설문 결과")
    st.success(f"{result['닉네임']}님의 설문이 제출되었습니다.")

    st.subheader("입력 내용")
    st.write(f"**닉네임:** {result['닉네임']}")
    st.write(f"**나이:** {result['나이']}세")
    st.write(f"**관심 분야:** {', '.join(result['관심 분야'])}")
    st.write(f"**수신 주기:** {result['수신 주기']}")
    st.write(
        "**AI 업무 자동화 선호도:** "
        f"{result['AI 업무 자동화 선호도']}점"
    )
    st.write(f"**받고 싶은 콘텐츠:** {result['받고 싶은 콘텐츠']}")
    st.write(f"**뉴스레터 구독:** {result['뉴스레터 구독']}")

    if st.button(
        "새 설문 작성하기",
        type="primary",
        use_container_width=True,
    ):
        reset_survey()
        st.rerun()


initialize_survey_state()

if st.session_state.newsletter_survey_submitted:
    show_survey_result()
else:
    show_survey_form()

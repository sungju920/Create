"""프리셋을 이용해 AI 뉴스레터 요청문을 만드는 페이지."""

import streamlit as st


REQUEST_DEFAULTS = {
    "request_type": "",
    "request_interest": "",
    "request_purpose": "",
    "request_content": "",
    "final_prompt": "",
}

REQUEST_PRESETS = {
    "실무 활용형": {
        "icon": "🛠️",
        "summary": "현업 사례, 적용 절차, 프롬프트·템플릿",
        "interest": "IT·개발, 마케팅",
        "purpose": "반복 업무를 줄이고 업무 생산성을 높이기",
        "content": "실무 자동화 사례, 추천 도구, 단계별 적용 방법",
    },
    "초보자 학습형": {
        "icon": "🌱",
        "summary": "핵심 용어, 초급 예제, 단계별 실습, 오류 해결",
        "interest": "게임",
        "purpose": "AI 활용 기초를 쉽게 학습하기",
        "content": "쉬운 용어 설명, 기초 예제, 단계별 따라 하기",
    },
    "최신 트렌드형": {
        "icon": "🚀",
        "summary": "최신 AI 동향과 산업 변화 분석",
        "interest": "여행, 경제",
        "purpose": "최신 AI 서비스와 시장 변화를 확인하기",
        "content": "최근 활용 사례, 주요 AI 도구, 향후 전망",
    },
}


def initialize_request_state():
    """요청문 페이지에서 사용하는 세션 상태의 기본값을 준비한다."""
    for key, value in REQUEST_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def clear_request():
    """선택한 프리셋, 입력값, 생성된 요청문을 초기화한다."""
    for key, value in REQUEST_DEFAULTS.items():
        st.session_state[key] = value


def select_preset(preset_name):
    """선택한 프리셋의 임시값을 입력란에 반영한다."""
    preset = REQUEST_PRESETS[preset_name]

    st.session_state.request_type = preset_name
    st.session_state.request_interest = preset["interest"]
    st.session_state.request_purpose = preset["purpose"]
    st.session_state.request_content = preset["content"]
    st.session_state.final_prompt = ""
    st.toast(f"{preset['icon']} {preset_name} 프리셋을 선택했습니다.")


def build_prompt(request_type, interest, purpose, content):
    """사용자가 확인한 입력값을 최종 AI 뉴스레터 요청문으로 조합한다."""
    return f"""
저는 {interest} 분야에 관심이 있습니다.

AI를 활용해 {purpose}를 원합니다.

{content}을 중심으로
{request_type} 뉴스레터를 작성해 주세요.

각 주제에는 추천 AI 도구, 구체적인 적용 방법,
기대 효과와 사용 시 주의사항을 포함해 주세요.
초보자도 이해할 수 있도록 한국어로 작성해 주세요.
""".strip()


def show_preset_card(column, preset_name):
    """프리셋 하나의 설명과 선택 버튼을 출력한다."""
    preset = REQUEST_PRESETS[preset_name]

    with column:
        with st.container(border=True):
            st.button(
                f"{preset['icon']} {preset_name}",
                key=f"select_{preset_name}",
                on_click=select_preset,
                args=(preset_name,),
                use_container_width=True,
            )
            st.markdown(
                f"""
                <div class="preset-card">
                    <p>{preset['summary']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


initialize_request_state()

st.markdown(
    """
    <style>
        .request-title {
            text-align: center;
            margin-bottom: 0.25rem;
        }

        .preset-card {
            min-height: 100px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center;
        }

        .preset-card p {
            margin: 0 0 0.5rem;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] button p {
            font-size: 1.1rem;
            font-weight: 700;
        }

    </style>
    <h1 class="request-title">🤖 AI 뉴스레터 요청문 생성</h1>
    """,
    unsafe_allow_html=True,
)
st.info(
    "프리셋을 선택하면 예시 내용이 자동으로 입력됩니다. "
    "내용을 원하는 대로 수정한 뒤 요청문을 생성해 보세요."
)
practical_col, beginner_col, trend_col = st.columns(3, gap="large")

show_preset_card(
    practical_col,
    "실무 활용형",
)
show_preset_card(
    beginner_col,
    "초보자 학습형",
)
show_preset_card(
    trend_col,
    "최신 트렌드형",
)

if st.session_state.request_type:
    st.success(f"선택한 프리셋: {st.session_state.request_type}")
else:
    st.warning("요청문을 만들 프리셋을 먼저 선택해 주세요.")

with st.form("newsletter_request_form"):
    st.text_input(
        "관심 분야 *",
        key="request_interest",
        placeholder="예: 마케팅, IT·개발, 경제",
    )

    st.text_input(
        "AI 자동화 활용 목적 *",
        key="request_purpose",
        placeholder="예: 반복 업무를 줄이고 생산성을 높이기",
    )

    st.text_area(
        "받고 싶은 뉴스레터 콘텐츠 *",
        key="request_content",
        placeholder="예: 실제 업무 자동화 사례와 단계별 적용 방법",
    )

    create_col, reset_col = st.columns(2)

    with create_col:
        create_prompt = st.form_submit_button(
            "요청문 생성",
            type="primary",
            use_container_width=True,
        )

    with reset_col:
        st.form_submit_button(
            "초기화",
            on_click=clear_request,
            use_container_width=True,
        )

if create_prompt:
    missing_fields = []

    if not st.session_state.request_type:
        missing_fields.append("프리셋")
    if not st.session_state.request_interest.strip():
        missing_fields.append("관심 분야")
    if not st.session_state.request_purpose.strip():
        missing_fields.append("AI 자동화 활용 목적")
    if not st.session_state.request_content.strip():
        missing_fields.append("받고 싶은 콘텐츠")

    if missing_fields:
        st.warning(
            "다음 필수 항목을 입력해 주세요: "
            + ", ".join(missing_fields)
        )
    else:
        st.session_state.final_prompt = build_prompt(
            st.session_state.request_type,
            st.session_state.request_interest.strip(),
            st.session_state.request_purpose.strip(),
            st.session_state.request_content.strip(),
        )
        st.toast("요청문이 생성되었습니다.")

if st.session_state.final_prompt:
    st.divider()
    st.subheader("최종 AI 뉴스레터 요청문")
    st.code(st.session_state.final_prompt, language=None)

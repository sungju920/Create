#로그인 화면
#로그인 시 아래 다양한 컴포넌트를 이용한 설문지 작성
#설문 화면이 사자리고 결과를 화면에 출력
#다음 설문 -> 입력 결과
#st.number_input, st.text_input, st.text_area,st.selectbox,st.multiselect,st.checkbox,st.slider
#로그인 비정상 시 다시 로그인 화면으로 진행

import streamlit as st


# 학습용 로그인 정보입니다.
# 실제 서비스에서는 비밀번호를 코드에 직접 저장하지 않고 DB와 암호화를 사용합니다.
LOGIN_ID = "1234"
LOGIN_PASSWORD = "1234"


def initialize_state():
    """앱에서 사용할 세션 상태의 기본값을 준비합니다."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "login_id" not in st.session_state:
        st.session_state.login_id = ""
    if "login_password" not in st.session_state:
        st.session_state.login_password = ""
    if "survey_submitted" not in st.session_state:
        st.session_state.survey_submitted = False
    if "survey_result" not in st.session_state:
        st.session_state.survey_result = {}


def login():
    """로그인에 성공하면 설문 화면으로 이동합니다."""
    if (
        st.session_state.login_id == LOGIN_ID
        and st.session_state.login_password == LOGIN_PASSWORD
    ):
        st.session_state.logged_in = True
        st.session_state.survey_submitted = False
        st.session_state.survey_result = {}
        st.rerun()

    # 로그인 실패 시 로그인 상태를 유지하지 않고 현재 화면에 머뭅니다.
    st.session_state.logged_in = False
    st.error("아이디 또는 비밀번호가 올바르지 않습니다. 다시 로그인해 주세요.")


def logout():
    """로그인과 설문 상태를 모두 초기화합니다."""
    st.session_state.logged_in = False
    st.session_state.survey_submitted = False
    st.session_state.survey_result = {}
    st.rerun()


def start_next_survey():
    """현재 결과를 지우고 새 설문지를 표시합니다."""
    st.session_state.survey_submitted = False
    st.session_state.survey_result = {}
    st.rerun()


def show_login():
    st.title("🔐 로그인")
    st.caption("설문에 참여하려면 로그인해 주세요.")

    with st.form("login_form"):
        st.text_input("아이디", key="login_id")
        st.text_input("비밀번호", type="password", key="login_password")
        login_submitted = st.form_submit_button("로그인", use_container_width=True)

    if login_submitted:
        login()

    st.info("학습용 계정: 1234 / 1234")


def show_survey():
    # 제출 성공 시 설문 영역만 지우기 위한 빈 영역입니다.
    survey_area = st.empty()

    with survey_area.container():
        st.title("📝 관심 주제 설문")
        st.write("아래 항목을 작성한 뒤 제출해 주세요.")

        with st.form("survey_form", clear_on_submit=False):
            name = st.text_input("이름")
            age = st.number_input("나이", min_value=0, max_value=100, value=20)
            category = st.selectbox(
                "좋아하는 분야",
                ["💻 개발·IT", "📣 마케팅", "💰 경제·금융", "⚽ 스포츠"],
            )
            hobbies = st.multiselect(
                "취미",
                ["🎮 게임", "🎬 영화/OTT", "✈️ 여행", "🏃 운동", "☕ 카페 탐방"],
            )
            satisfaction = st.slider(
                "관심도", min_value=1, max_value=100, value=10
            )
            comment = st.text_area("관심 가는 이유")
            newsletter = st.checkbox("뉴스레터를 받아보겠습니다.")

            submitted = st.form_submit_button("제출", use_container_width=True)

    if submitted:
        st.session_state.survey_result = {
            "이름": name.strip() or "익명",
            "나이": int(age),
            "취미": hobbies,
            "좋아하는 분야": category,
            "관심도": satisfaction,
            "관심 가는 이유": comment.strip() or "입력하지 않음",
            "뉴스레터 수신": "동의" if newsletter else "동의하지 않음",
        }
        st.session_state.survey_submitted = True

        # 설문 화면을 즉시 없애고 같은 실행에서 결과를 출력합니다.
        survey_area.empty()
        show_result()


def show_result():
    result = st.session_state.survey_result
    # 코드 변경 전에 제출된 기존 세션 데이터도 오류 없이 표시합니다.
    category = result.get("좋아하는 분야", "선택하지 않음")
    hobbies = result.get("취미", [])

    # 이전에 단일 선택으로 저장된 취미 데이터도 목록으로 변환합니다.
    if isinstance(hobbies, str):
        hobbies = [hobbies]

    # 이전에 복수 선택으로 저장된 분야 데이터도 표시할 수 있게 변환합니다.
    if isinstance(category, list):
        category = ", ".join(category) or "선택하지 않음"

    st.title("✅ 설문 결과")
    st.success(f"{result['이름']}님의 설문이 제출되었습니다.")

    st.subheader("입력 결과")
    st.write(f"**이름:** {result['이름']}")
    st.write(f"**나이:** {result['나이']}세")
    st.write(f"**취미:** {', '.join(hobbies) or '선택하지 않음'}")
    st.write(
        f"**좋아하는 분야:** "
        f"{category}"
    )
    st.write(f"**관심도:** {result['관심도']}점")
    st.write(f"**관심 가는 이유:** {result['관심 가는 이유']}")
    st.write(f"**뉴스레터 수신:** {result['뉴스레터 수신']}")

    if st.button("다시 설문 제출하기", type="primary", use_container_width=True):
        start_next_survey()


st.set_page_config(page_title="관심 주제 설문", page_icon="📝")
initialize_state()

if not st.session_state.logged_in:
    show_login()
else:
    with st.sidebar:
        login_id = st.session_state.get("login_id", "사용자")
        st.success(f"{login_id or '사용자'}님, 로그인되었습니다.")
        st.button("로그아웃", on_click=logout, use_container_width=True)

    if st.session_state.survey_submitted:
        show_result()
    else:
        show_survey()

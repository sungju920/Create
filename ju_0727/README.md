# 계획서

## 1. 프로젝트 목표

Streamlit으로 다음 세 가지 독립 기능을 제공하는 뉴스레터 설문 프로젝트를 완성한다.

- 뉴스레터 구독자의 관심 분야와 AI 업무 자동화 선호도를 조사하고 입력 결과를 출력하는 설문
- 임시 설문 데이터를 이용해 관심 분야별 인원수와 선호도를 테이블·차트로 조회하는 대시보드
- 미리 준비한 프리셋을 선택하고 내용을 수정해 최종 AI 뉴스레터 요청문을 생성하는 화면

세 화면은 반드시 데이터를 연동하지 않아도 된다. `select.py`는 코드에 작성한 임시 데이터를 사용하고, `request.py`는 설문 결과 대신 미리 작성한 프리셋 데이터를 사용한다.

각 화면에서 입력값을 유지하거나 초기화해야 하는 경우 해당 파일 안에서 `st.session_state`를 사용한다.

## 2. 범위와 완료 기준

| 구분 | 완료 기준 |
| --- | --- |
| 설문 | — 구독자 정보, 관심 분야, 수신 주기, AI 자동화 선호도를 입력하고 제출 결과를 확인할 수 있다. |
| 설문 초기화 | 초기화 버튼을 누르면 현재 설문 입력값이 기본값으로 돌아간다. |
| 조회 | 코드에 작성된 임시 데이터를 테이블과 막대그래프로 확인할 수 있다. |
| 선호도 | 마케팅, IT·개발, 게임, 여행, 경제 분야의 임시 AI 업무 자동화 선호도를 비교할 수 있다. |
| 프리셋 | 실무 활용형, 초보자 학습형, 최신 트렌드형 중 하나를 선택하면 기본값이 입력된다. |
| 요청문 | 프리셋 결과를 수정한 뒤 생성 버튼을 눌러 최종 AI 뉴스레터 요청문을 출력할 수 있다. |
| 요청문 초기화 | 초기화 버튼을 누르면 프리셋과 요청문 입력값이 기본값으로 돌아간다. |
| 예외 처리 | 필수 입력값이나 조회 데이터가 없을 때 오류 대신 안내 메시지를 출력한다. |

## 3. 목표 디렉터리 구조

```text
ju/
├── streamlit_app.py  # Survey·Select 화면을 연결하는 멀티페이지 메인
├── survey.py   # 뉴스레터 설문, 설문 제출·초기화, 현재 설문 결과 출력
├── select.py   # 임시 설문 데이터 테이블 및 차트 조회
└── request.py  # 프리셋 선택·수정, 최종 요청문 생성
```

각 화면의 데이터 기능은 독립적으로 구현하고 `ju/streamlit_app.py`에서
`st.Page`와 `st.navigation`을 사용해 Survey, Select, Request 화면을
연결한다. 세 페이지는 메인 앱의 `layout="wide"` 설정을 함께 사용한다.

### `survey.py`

- 뉴스레터 구독 설문 화면 출력
- 설문 입력에 필요한 세션 기본값 생성
- 필수 입력값 검사
- 설문 제출 처리
- 현재 사용자가 입력한 설문 결과 출력
- 현재 설문 입력값 초기화

### `select.py`

- 코드 안에 임시 설문 데이터 작성
- 임시 데이터를 Pandas DataFrame으로 변환
- 관심 분야별 인원수 테이블 출력
- 관심 분야별 AI 자동화 평균 선호도 출력
- 인원수 막대그래프와 자동화 선호도 선 그래프 출력

### `request.py`

- 요청문 입력에 필요한 세션 기본값 생성
- 실무 활용형, 초보자 학습형, 최신 트렌드형 프리셋 제공
- 선택한 프리셋의 임시값을 입력 위젯에 반영
- 자동 입력된 값 직접 수정
- 최종 AI 요청문 생성
- 요청문 입력값 초기화

## 4. 데이터 계획

### Survey 데이터

`survey.py`는 현재 사용자가 입력한 값을 해당 화면의 `st.session_state`로 관리한다.

| 세션 키 | 기본값 | 용도 |
| --- | --- | --- |
| `newsletter_nickname` | `""` | 닉네임 |
| `newsletter_age` | `20` | 나이 |
| `newsletter_interests` | `[]` | 관심 분야 복수 선택 |
| `newsletter_frequency` | `"주 1회"` | 뉴스레터 수신 주기 |
| `newsletter_automation_score` | `3` | AI 업무 자동화 선호도 |
| `newsletter_content_request` | `""` | 받고 싶은 콘텐츠 |
| `newsletter_subscribe` | `True` | 뉴스레터 구독 여부 |

설문 제출 후에는 별도 파일이나 데이터베이스에 저장하지 않고 현재 입력 결과를 화면에 출력한다.

### Select 임시 데이터

`select.py`는 다음과 같은 임시 집계 데이터를 코드 안에 작성한다.

```python
survey_result = {
    "interest": ["📣마케팅", "💻IT·개발", "🎮게임", "✈️여행", "💵경제"],
    "people": [32, 28, 26, 21, 18],
    "automation_score": [4.6, 4.8, 4.1, 3.9, 4.3],
}
```

임시 데이터를 DataFrame으로 변환해 테이블과 차트에 공통으로 사용한다.

```python
result_df = pd.DataFrame(survey_result)
```

### Request 프리셋 데이터

`request.py`는 다음 세 가지 임시 프리셋을 사용한다.

| 프리셋 | 관심 분야 | 목적 | 원하는 콘텐츠 |
| --- | --- | --- | --- |
| 🛠️ 실무 활용형 | IT·개발, 마케팅 | 반복 업무를 줄이고 업무 생산성을 높이기 | 현업 사례, 적용 절차, 프롬프트·템플릿 |
| 🌱 초보자 학습형 | 게임 | 게임 분야의 AI 활용 기초를 쉽게 학습하기 | 핵심 용어, 초급 예제, 단계별 실습, 오류 해결 |
| 🚀 최신 트렌드형 | 여행, 경제 | 최신 AI 서비스와 시장 변화를 확인하기 | 최신 AI 동향과 산업 변화 분석 |

| 세션 키 | 기본값 | 용도 |
| --- | --- | --- |
| `request_type` | `""` | 선택한 프리셋 |
| `request_interest` | `""` | 관심 분야 |
| `request_purpose` | `""` | AI 자동화 활용 목적 |
| `request_content` | `""` | 받고 싶은 콘텐츠 |
| `final_prompt` | `""` | 생성된 최종 요청문 |

## 5. 화면 및 기능 계획

| 화면 | 주요 입력 또는 데이터 | 출력 |
| --- | --- | --- |
| Survey | 사용자가 직접 입력한 뉴스레터 설문 | 현재 사용자의 설문 결과 |
| Select | 코드에 작성한 임시 집계 데이터 | 결과 테이블, 막대그래프 |
| Request | 코드에 작성한 프리셋과 사용자의 수정값 | 최종 AI 뉴스레터 요청문 |

### Survey 계획

화면 순서는 다음과 같이 구성한다.

1. 페이지 제목과 설문 안내
2. 닉네임 입력
3. 나이 입력
4. 관심 분야 복수 선택
5. 뉴스레터 수신 주기 선택
6. AI 업무 자동화 선호도 입력
7. 받고 싶은 콘텐츠 입력
8. 뉴스레터 구독 여부 선택
9.  제출 및 초기화 버튼
10. 현재 설문 결과 출력

관심 분야는 다음 다섯 가지로 구성한다.

- 📣마케팅
- 💻IT·개발
- 🎮게임
- ✈️여행
- 💵경제

필수 항목은 관심 분야와 뉴스레터 수신 주기이다. 닉네임과 받고 싶은
콘텐츠를 입력하지 않은 경우 결과 화면에 각각 `익명`, `입력하지 않음`으로
표시한다.

설문 제출 결과 예시:

```text
닉네임: 홍길동
나이: 20세
관심 분야: 마케팅, IT·개발
수신 주기: 주 1회
AI 업무 자동화 선호도: 5점
받고 싶은 콘텐츠: 개발 자동화 도구와 실제 사례
뉴스레터 구독: 신청
```

### Select 계획

상단에는 임시 집계 데이터 테이블을 출력하고, 테이블 아래에는 분야별 비교에 적합한 막대그래프를 세로로 배치한다.

임시 결과 테이블:

| interest | people | automation_score |
| --- | ---: | ---: |
| 📣마케팅 | 32 | 4.6 |
| 💻IT·개발 | 28 | 4.8 |
| 🎮게임 | 26 | 4.1 |
| ✈️여행 | 21 | 3.9 |
| 💵경제 | 18 | 4.3 |

화면 구성:

1. `CHART` 또는 `Survey Dashboard` 제목
2. 전체 임시 응답자 수 100명
3. 가장 관심도가 높은 분야
4. 가장 자동화 선호도가 높은 분야
5. 임시 결과 테이블
6. 관심 분야별 인원수 막대그래프
7. 관심 분야별 자동화 선호도 그래프

예정 차트:

```python
st.bar_chart(result_df, x="interest", y="people")
st.line_chart(result_df, x="interest", y="automation_score")
```

### Request 계획

뉴스레터 요청문 생성 화면은 세 개의 프리셋 버튼과 하나의 수정 폼으로 구성한다. 다른 예제의 변수명이나 화면 구성을 가져오지 않고 뉴스레터 기능에 맞는 이름을 사용한다.

화면 순서는 다음과 같이 구성한다.

1. 페이지 제목
2. 선택한 프리셋 안내
3. 3개 칼럼에 배치한 프리셋 버튼
4. 관심 분야 입력란
5. AI 자동화 활용 목적 입력란
6. 받고 싶은 콘텐츠 입력란
7. 요청문 생성 및 초기화 버튼
8. 최종 AI 요청문 출력

프리셋 버튼을 누르면 해당 프리셋의 임시 데이터가 세 입력란에 자동으로 채워진다. 사용자는 입력된 값을 직접 수정할 수 있다.
선택 직후에는 어떤 프리셋을 눌렀는지 토스트 메시지로 안내한다. Request
페이지는 메인 앱의 `layout="wide"` 설정을 동일하게 사용한다.
프리셋은 테두리가 있는 3개의 카드로 배치한다. 클릭 버튼은 카드 맨 위에
`아이콘 + 프리셋명`으로 표시하고, 중복 제목은 두지 않으며 설명은 가운데
정렬한다.

프리셋 영역은 다음과 같이 3개 칼럼으로 배치한다.

| 첫 번째 칼럼 | 두 번째 칼럼 | 세 번째 칼럼 |
| --- | --- | --- |
| 실무 활용형 | 초보자 학습형 | 최신 트렌드형 |
| 업무 자동화 사례 중심 | 기초 개념과 쉬운 예제 중심 | 최근 AI 활용 동향 중심 |
| IT·개발, 마케팅 | 게임 | 여행, 경제 |

예정 칼럼 구성:

```python
practical_col, beginner_col, trend_col = st.columns(3)

with practical_col:
    st.subheader("실무 활용형")
    st.caption("업무 자동화 사례와 적용 단계 중심")
    st.button(
        "실무 활용형 선택",
        on_click=select_practical,
        use_container_width=True,
    )

with beginner_col:
    st.subheader("초보자 학습형")
    st.caption("기초 개념과 따라 하기 예제 중심")
    st.button(
        "초보자 학습형 선택",
        on_click=select_beginner,
        use_container_width=True,
    )

with trend_col:
    st.subheader("최신 트렌드형")
    st.caption("최근 AI 활용 사례와 변화 중심")
    st.button(
        "최신 트렌드형 선택",
        on_click=select_trend,
        use_container_width=True,
    )
```

각 프리셋 버튼이 입력할 임시값은 다음과 같다.

```python
def select_practical():
    st.session_state.request_type = "실무 활용형"
    st.session_state.request_interest = "IT·개발, 마케팅"
    st.session_state.request_purpose = (
        "반복 업무를 줄이고 업무 생산성을 높이기"
    )
    st.session_state.request_content = (
        "실제 업무 자동화 사례, 추천 도구, 단계별 적용 방법"
    )


def select_beginner():
    st.session_state.request_type = "초보자 학습형"
    st.session_state.request_interest = "게임"
    st.session_state.request_purpose = (
        "AI 업무 자동화의 기초 개념을 쉽게 학습하기"
    )
    st.session_state.request_content = (
        "쉬운 용어 설명, 기초 예제, 단계별 따라 하기"
    )


def select_trend():
    st.session_state.request_type = "최신 트렌드형"
    st.session_state.request_interest = "여행, 경제"
    st.session_state.request_purpose = (
        "분야별 최신 AI 활용 동향과 변화를 확인하기"
    )
    st.session_state.request_content = (
        "최근 활용 사례, 주요 AI 도구, 향후 예상 변화"
    )
```

프리셋 아래에는 선택된 값을 수정할 수 있는 폼을 배치한다.

```python
with st.form("request_form"):
    interest = st.text_input(
        "관심 분야",
        key="request_interest",
    )
    purpose = st.text_input(
        "AI 자동화 활용 목적",
        key="request_purpose",
    )
    content = st.text_area(
        "받고 싶은 뉴스레터 콘텐츠",
        key="request_content",
    )

    create_col, reset_col = st.columns(2)

    with create_col:
        create_prompt = st.form_submit_button(
            "요청문 생성",
            use_container_width=True,
        )

    with reset_col:
        st.form_submit_button(
            "초기화",
            on_click=clear_request,
            use_container_width=True,
        )
```

최종 출력 예시:

```text
저는 마케팅과 IT·개발 분야에 관심이 있습니다.

AI를 활용해 반복 업무를 줄이고
업무 생산성을 높이고 싶습니다.

실제 업무 자동화 사례와 적용 단계를 중심으로
뉴스레터를 작성해 주세요.

각 주제에는 추천 AI 도구, 적용 방법,
기대 효과와 주의사항을 포함해 주세요.
```

## 6. 진행 순서

1. `survey.py`, `select.py`, `request.py`의 독립적인 역할을 확정한다.
2. ✅ `survey.py`에 세션 초기화 함수와 설문 입력 화면을 구현한다.
3. ✅ 설문 제출, 필수값 검사, 설문 결과 출력, 초기화를 구현한다.
4. `select.py`에 관심 분야별 인원수와 자동화 선호도 임시 데이터를 작성한다.
5. 임시 데이터를 DataFrame으로 변환하고 결과 테이블을 출력한다.
6. 임시 데이터로 인원수 막대그래프와 자동화 선호도 선 그래프를 출력한다.
7. `request.py`에 요청문 세션 초기화 함수를 구현한다.
8. 세 가지 프리셋 버튼과 임시 기본값을 구현한다.
9. 프리셋 입력값 수정, 요청문 생성, 요청문 초기화를 구현한다.
10. 세 화면을 각각 실행해 입력, 출력, 초기화 동작을 확인한다.

## 7. 테스트 체크리스트

- 설문: 정상 제출, 관심 분야 미선택, 수신 주기 미선택
- 설문 결과: 사용자가 입력한 값과 출력값 일치
- 설문 초기화: 모든 입력값이 기본값으로 복원
- 조회 테이블: 임시 데이터와 출력 데이터 일치
- 인원수 차트: 테이블의 `people` 값과 차트 값 일치
- 선호도 차트: 테이블의 `automation_score` 값과 차트 값 일치
- 프리셋: 세 버튼이 서로 다른 임시값 입력
- 프리셋 수정: 자동 입력된 값을 사용자가 직접 수정 가능
- 요청문 생성: 수정된 입력값이 최종 요청문에 반영
- 요청문 초기화: 프리셋, 입력값, 최종 요청문 삭제

## 8. 보안 및 운영 원칙

- 화면 구현 파일은 `survey.py`, `select.py`, `request.py`로 구분하고,
  `streamlit_app.py`를 멀티페이지 진입점으로 사용한다.
- 세 화면은 데이터 연동을 필수 조건으로 두지 않는다.
- `select.py`와 `request.py`의 임시 데이터는 실제 조사 결과가 아닌 예시임을 화면에 표시한다.
- 모든 세션 키는 화면에서 사용하기 전에 초기화한다.
- `on_click`에는 함수 실행 결과가 아니라 함수 자체를 전달한다.
- 초기화 함수에서 관련된 모든 입력값을 빠짐없이 기본값으로 변경한다.
- 실제 이메일 주소, 전화번호 등 불필요한 개인정보는 수집하지 않는다.
- 코드에 API 키, 비밀번호 또는 개인 식별 정보를 작성하지 않는다.
- 입력값이 부족한 경우 예외 대신 사용자 안내 메시지를 표시한다.
- 실제 누적 설문이나 운영 기능이 필요해질 때 별도의 저장소 연동을 검토한다.

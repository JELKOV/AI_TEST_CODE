# TVCF AI-TDD Harness 발표 대본

## 이 문서의 목적

이 문서는 청중에게 공유하는 웹페이지가 아니라 발표자용 대본이다. 발표 화면은
`http://127.0.0.1:8000`이고, 이 문서에는 시간 배분, 실제로 말할 문장, 화면 조작,
라이브 시연 명령과 실패 대응을 함께 적는다.

대본의 표시는 다음 의미다.

- **[화면]** 브라우저나 IDE에서 보여줄 위치
- **[말하기]** 실제 발표 문장
- **[행동]** 클릭하거나 실행할 작업
- **[확인]** 다음 단계로 가기 전에 눈으로 확인할 결과
- **[주의]** 과장하거나 오해를 만들지 않기 위해 지킬 범위
- **[시간 부족]** 발표가 밀릴 때 줄일 부분

오늘 발표의 핵심 문장은 하나다.

> AI가 코드를 빨리 만들수록, 무엇이 맞는지 판단하는 기준은 더 작고 명확하며 반복 가능해야 한다.

마지막에는 다음 문장으로 닫는다.

> AI 시대의 TDD는 테스트 대필 기술이 아니라, 사람의 의도를 실행 가능한 완료 기준으로 만드는 방법입니다.

---

## 발표 범위와 표현 원칙

1. 기존 테스트 작성자나 특정 프로젝트를 평가하지 않는다.
2. 테스트 개수, Coverage 또는 Frontend와 Backend의 점수를 비교하지 않는다.
3. 회사 전체의 테스트 현황은 도구와 역할 수준에서만 설명한다.
4. 직접 시연하는 코드는 발표자가 설명할 수 있는 Backend 계약 규칙의 축약본이다.
5. 실습 API는 운영 endpoint 전체가 아니라 validator 동작만 분리한 FastAPI 데모다.
6. 운영 `PaymentTermsCommand`에는 이미 음수 방지 조건이 있다. 현재 RED는 학습용 복제본에서
   그 조건 한 줄을 의도적으로 뺀 상태이며, 운영 코드의 결함을 주장하는 사례가 아니다.
7. Kent Beck이 만든 것은 현재 저장소의 하네스가 아니다. Kent Beck에게서는 테스트 목록에서
   하나씩 진행하는 TDD 흐름을 가져왔다.
8. OpenAI의 Harness Engineering 역시 이 저장소의 `harness.toml`이나 Python 스크립트를 만든
   제품명이 아니다. 저장소 문서, 도구와 피드백을 AI가 직접 사용할 수 있게 환경을 설계한다는
   아이디어를 참고했다.
9. `harness.toml`, `scripts/tdd_harness.py`, JSON 실행 기록은 이 발표를 위해 만든 최소 구현이다.

---

## 현재 라이브 데모 시작 상태

현재 작업 디렉터리는 일부러 RED 상태다. 발표 직전에 이 상태를 유지해야 한다.

`app/main.py`의 시작 코드:

~~~python
class ContractPaymentTerms(BaseModel):
    advance_payment_percentage: int
    interim_payment_percentage: int = Field(..., ge=0)
    final_payment_percentage: int = Field(..., ge=0)
~~~

`plan.md`의 현재 항목:

~~~text
- [ ] 합계가 100이어도 선금 지급 비율이 음수이면 422로 거절한다.
~~~

이미 존재하는 테스트의 기대 결과:

~~~python
def test_rejects_negative_payment_percentage_even_when_sum_is_100() -> None:
    # -10 + 50 + 60 = 100
    response = client.post("/contracts/payment-terms/validate", json=payload)
    assert response.status_code == 422
~~~

현재 실제 결과는 `200`이므로 다음 focused test가 실패해야 정상이다.

~~~bash
uv run pytest tests/test_contract_payment_terms.py::test_rejects_negative_payment_percentage_even_when_sum_is_100 -vv
~~~

예상 핵심 출력:

~~~text
FAILED
E assert 200 == 422
~~~

GREEN에서 기대하는 제품 코드 변경은 한 줄뿐이다.

~~~diff
-    advance_payment_percentage: int
+    advance_payment_percentage: int = Field(..., ge=0)
~~~

발표 전에는 `git restore app/main.py plan.md`를 실행하거나 현재 변경을 커밋하지 않는다.

---

## 발표 전 준비

### 1. 전날 또는 발표 30분 전

Git Bash 첫 번째 창에서 의존성을 확인한다.

~~~bash
cd /c/Users/gram/tvcf/AI_TEST_CODE
uv sync
uv run python scripts/tdd_harness.py check
~~~

정상 출력에서 다음 연결을 확인한다.

~~~text
agreement: AGENTS.md
plan: plan.md
focused: uv run pytest {focused} -vv
full: uv run pytest -vv
lint: uv run ruff check .
type: uvx pyright
evidence: .harness/latest-run.json
~~~

현재 RED를 반복해서 연습하려면 먼저 RED 차이를 패치로 보관할 수 있다. `.harness/`는 Git에서
제외되는 폴더다.

~~~bash
mkdir -p .harness
git diff -- app/main.py plan.md > .harness/live-demo-red.patch
test -s .harness/live-demo-red.patch && echo "RED patch ready"
~~~

리허설 후 코드가 GREEN으로 돌아왔을 때 다음 명령으로 RED를 다시 적용한다.

~~~bash
git apply .harness/live-demo-red.patch
~~~

패치를 두 번 적용하면 실패하므로 `git diff -- app/main.py plan.md`가 비어 있을 때만 실행한다.

### 2. 발표용 창 구성

Git Bash 첫 번째 창은 서버 전용으로 둔다.

~~~bash
cd /c/Users/gram/tvcf/AI_TEST_CODE
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
~~~

Git Bash 두 번째 창은 테스트와 하네스 전용으로 둔다.

~~~bash
cd /c/Users/gram/tvcf/AI_TEST_CODE
clear
~~~

브라우저 탭은 다음 순서로 준비한다.

1. 발표 화면: `http://127.0.0.1:8000/#top`
2. 필요할 때만 보여줄 OpenAPI: `http://127.0.0.1:8000/docs`
3. 영상 장애에 대비한 세 YouTube 원본 링크

IDE에는 다음 파일을 미리 열어 둔다.

1. `plan.md`
2. `AGENTS.md`
3. `tests/test_contract_payment_terms.py`
4. `app/main.py`
5. `harness.toml`
6. `.harness/latest-run.json`

AI 도구는 현재 저장소를 연 상태로 준비하되, 아래의 실습 프롬프트는 아직 실행하지 않는다.

### 3. 발표 10분 전 최종 확인

1. 브라우저를 새로고침하고 페이지가 정상 표시되는지 확인한다.
2. 세 영상 탭을 한 번씩 눌러 회사 네트워크에서 재생되는지 확인한다.
3. 브라우저 배율은 90~100%, 터미널 글자는 16px 안팎으로 둔다.
4. 서버 터미널에 `Application startup complete`가 보이는지 확인한다.
5. `Payment Terms` 버튼을 한 번 눌러 `FAIL`, `Expected 422`, `Actual 200`이 나오는지 확인한다.
6. 발표 시작 전 페이지를 다시 새로고침해 Live Request 상태를 `READY`로 돌린다.
7. focused test를 미리 확인했다면 터미널은 `clear`로 비운다.
8. 현재 RED인 `app/main.py`와 `plan.md`를 커밋하지 않는다.

---

## 40분 전체 동선

| 시간 | 화면 | 목적 |
| --- | --- | --- |
| 0:00~5:00 | Hero + Start Here | 질문, 목표, 장점과 비용을 제시한다. |
| 5:00~11:30 | 3 External Video Briefings | 질문, 위험 사례, 공식 TDD 사례를 비교한다. |
| 11:30~16:30 | 01 · 테스트 구성 | Frontend와 Backend의 역할과 공유 기준을 설명한다. |
| 16:30~24:00 | 02 · 작업 흐름 | TDD 원칙과 최소 Repository Harness의 역할을 구분한다. |
| 24:00~35:30 | 03 · 실습 | 브라우저 FAIL부터 AI 수정, 전체 GREEN, API PASS까지 시연한다. |
| 35:30~39:00 | 04 · 적용 | 회사에서 효과적인 지점과 과도한 기대를 구분한다. |
| 39:00~40:00 | Closing | 핵심 문장을 반복하고 질문으로 넘긴다. |

영상 재생이나 AI 응답이 지연될 수 있으므로 실제 설명은 38~39분에 끝내는 것을 목표로 한다.

---

## 0:00~5:00 - 문제 제기와 오늘의 목표

### 0:00~0:50 - 첫 질문

**[화면]** Hero의 `AI에게 TDD를 시키는 것만으로 충분할까?`

**[말하기]**

> 안녕하세요. 오늘은 테스트 도구를 새로 소개하거나 테스트를 많이 만들자는 이야기부터
> 시작하지 않겠습니다. 먼저 한 가지 질문으로 시작하겠습니다.
>
> Claude나 Codex가 코드를 수정한 뒤 "완료했습니다"라고 말하면, 우리는 무엇을 근거로
> 그 변경이 실제 업무 규칙까지 지켰다고 판단할 수 있을까요?

청중을 보고 2초 정도 멈춘다.

> AI는 구현 속도를 크게 높였습니다. 그런데 코드가 빨리 생길수록 사람이 모든 줄을 읽고
> 업무 정답을 다시 추론하는 방식은 더 어려워집니다. 오늘은 테스트를 AI의 코드 생성 기능이
> 아니라, 사람의 의도와 완료 기준을 전달하는 실행 환경으로 보는 방법을 이야기하겠습니다.

### 0:50~2:30 - Hero의 네 문장

**[행동]** Hero의 네 요점을 위에서 아래로 천천히 짚는다.

**[말하기]**

> 첫째, AI가 코드를 빨리 만들수록 무엇이 맞는지 판단하는 기준이 더 중요해집니다.
>
> 둘째, 테스트는 단순히 오류를 찾는 코드가 아니라 "이 입력에는 이 결과가 맞다"라는 업무
> 의도와 "여기까지 확인해야 완료다"라는 기준을 AI에게 전달할 수 있습니다.
>
> 셋째, Frontend와 Backend가 같은 테스트 파일을 관리하자는 뜻은 아닙니다. 각자 자기 코드의
> 테스트를 소유하되 API 계약과 중요한 시나리오는 같이 볼 수 있다는 의미입니다.
>
> 넷째, 오늘은 이 주장을 말로만 하지 않고 작은 계약 API와 Repository Harness로 직접
> 확인하겠습니다. 마지막 실습은 처음에 실패하고, 같은 테스트를 유지한 채 AI가 최소 코드만
> 수정하고, 전체 검증과 실제 HTTP 응답까지 통과시키는 순서로 진행합니다.

Hero 아래 세 역할을 짚는다.

> 역할도 세 가지로 나눴습니다. 사람은 업무 정답과 경계값을 승인합니다. AI는 승인된 다음
> 테스트 하나를 구현합니다. 완료 여부는 AI의 설명이 아니라 focused test와 full gate의
> 실행 결과로 판단합니다.

### 2:30~5:00 - 목표, 장점과 고려사항

**[화면]** `Start Here · 먼저 볼 기준`

**[말하기]**

> 오늘의 목표는 AI가 변경한 코드가 기대한 업무 규칙을 지키는지 재현 가능한 테스트와 실제
> HTTP 응답으로 증명하는 것입니다. 여기서 중요한 단어는 "재현 가능"입니다. 담당자가 바뀌어도
> 같은 명령과 입력으로 다시 확인할 수 있어야 합니다.

`Strengths`를 짚는다.

> 테스트의 장점은 세 가지로 보겠습니다. 작은 입력 오류는 DB 작업 전에 빠르게 발견할 수 있고,
> unit, integration, e2e와 harness는 서로 다른 위험을 보호합니다. 그리고 지급 비율이나 예산
> 조합처럼 말로만 전달되던 규칙이 실행 가능한 명세가 됩니다.

`Trade-offs`를 짚는다.

> 반대로 테스트에는 비용이 있습니다. DB, 인증과 외부 연동이 들어가면 준비와 실행이 느려지고,
> Mock만 사용하면 실제 연동 차이를 놓칠 수 있습니다. 테스트가 많아질수록 이번 변경과 가까운
> 테스트를 찾는 일도 중요해집니다.
>
> 그래서 오늘의 제안은 모든 코드를 무조건 Test-first로 만들자는 것이 아닙니다. 실패 비용이 큰
> 업무 규칙과 입력 경계부터 focused test로 빠르게 확인하고, 마지막에 전체 회귀를 확인하자는
> 방식입니다.

**전환 문장**

> 이 방식이 AI 시대의 정답이라고 단정할 수는 없습니다. 먼저 최근 논의에서 어떤 질문과 위험,
> 실천 사례가 나오는지 세 영상의 짧은 구간만 비교해 보겠습니다.

---

## 5:00~11:30 - 세 영상으로 질문, 위험과 공식 사례 비교

**[화면]** `세 관점으로 비교하는 AI 시대 TDD`

### 5:00~6:40 - Video 1: 문제 제기

**[행동]** `01 · 문제 제기` 탭을 선택하고 `0:24~1:16` 구간을 재생한다. 실제 영상은 52초다.

**[재생 전 말하기]**

> 첫 영상은 Kent Beck의 YOW! 2025 발표입니다. 여기서는 특정 정답을 외우기보다, AI가 보강된
> 개발에서 기존 TDD 순서를 그대로 적용하면 되는지 질문을 던지는 장면에 집중하겠습니다.

**[재생 후 말하기]**

> 이 구간에서 가져갈 요점은 세 가지입니다. 프로그래밍 방식은 빠르게 변하고 있고, AI와 TDD를
> 결합하는 하나의 정답은 아직 정립되지 않았으며, 결국 팀이 직접 실험하면서 기준을 찾아야 한다는
> 점입니다.

**전환 문장**

> 하지만 정답이 없다는 말만으로는 실제 작업 기준을 만들 수 없습니다. 다음 영상에서는 테스트를
> AI와 함께 사용할 때 생기는 구체적인 위험을 보겠습니다.

### 6:40~8:55 - Video 2: 테스트를 바꾸는 위험

**[행동]** `02 · 위험 확인` 탭을 선택하고 `50:24~51:58` 구간을 재생한다. 실제 영상은 94초다.

**[재생 전 말하기]**

> The Pragmatic Engineer의 Kent Beck 인터뷰입니다. 테스트는 AI가 놓친 기대값을 전달하는 좋은
> 수단이지만, AI가 제품 코드를 고치는 대신 실패한 테스트를 바꾸려고 하면 어떤 문제가 생기는지
> 보겠습니다.

**[재생 후 말하기]**

> 여기서 핵심은 AI가 테스트를 작성할 수 있느냐가 아닙니다. 제품 코드와 채점 기준을 AI가 동시에
> 움직이면 검증이 약해진다는 점입니다. 그래서 사람이 승인한 expected value는 GREEN 단계에서
> 임의로 움직이지 않는 경계가 되어야 합니다.

**전환 문장**

> 그러면 실제 AI 코딩 도구의 공식 예시는 요구조건, 테스트와 구현의 순서를 어떻게 보여줄까요?

### 8:55~10:55 - Video 3: GitHub 공식 사례

**[행동]** `03 · GitHub 공식 사례` 탭을 선택하고 `6:06~7:24` 구간을 재생한다. 실제 영상은 78초다.

**[재생 전 말하기]**

> GitHub 공식 채널의 2025년 Copilot TDD 사례입니다. 아직 존재하지 않는 username validator를
> 예로 들어 개발자가 요구조건을 먼저 주고, 테스트가 실패한 뒤 구현을 만드는 순서를 보여줍니다.

**[재생 중 짚을 지점]**

1. `6:06`: 개발자가 기능 요구조건을 먼저 설명한다.
2. `6:45`: Copilot이 아직 없는 기능에 대한 테스트를 만든다.
3. `6:49`: 구현이 없어 테스트가 실패하는 RED를 확인한다.
4. `6:55`: 구현 생성을 요청한다.
5. `7:11`: 테스트를 다시 실행해 GREEN을 확인한다.

### 10:55~11:30 - 세 영상 정리

**[말하기]**

> 세 영상을 한 문장으로 묶으면 이렇습니다. AI와 TDD의 유일한 정답은 아직 없고, AI가 실패를
> 피하려고 테스트를 바꾸는 위험도 있습니다. 그래도 공통으로 가져갈 수 있는 기준은 사람이
> 요구조건과 기대값을 정하고, 실제 test runner의 RED와 GREEN이 다음 단계를 결정하게 만드는
> 것입니다.

**[주의]** 영상 내용을 Kent Beck 또는 GitHub의 직접 명령처럼 확대하지 않는다. 현재 저장소의
10개 규칙과 하네스는 이 원칙을 발표용으로 구체화한 로컬 구현이라고 설명한다.

**[시간 부족]** 영상 재생이 지연되면 각 영상의 첫 20~30초만 보여주고 화면의 한글 요점 세 줄을
읽는다. 원본 링크를 새로 찾느라 발표를 멈추지 않는다.

---

## 11:30~16:30 - Frontend와 Backend 테스트 구성

**[행동]** 상단 내비게이션의 `01 · 테스트 구성`을 선택한다.

### 11:30~12:20 - 설명 범위

**[말하기]**

> 이제 회사에서 이미 사용하는 테스트를 역할 기준으로 보겠습니다. 특정 프로젝트의 테스트가
> 좋다거나 부족하다고 평가하지 않고, Frontend와 Backend가 각각 어떤 위험을 보호하는지만
> 포괄적으로 보겠습니다. 직접 코드와 API로 시연하는 부분은 제가 설명 가능한 Backend 계약
> 규칙을 축약한 데모입니다.

### 12:20~14:10 - Frontend

**[화면]** `Frontend 테스트 · Jest · Vitest · Playwright`

**[말하기]**

> Frontend의 Jest와 Vitest는 상태 계산, 데이터 변환과 조건 분기처럼 브라우저 없이 빠르게
> 확인할 수 있는 로직에 적합합니다. 예를 들어 API가 `qualifies: true`를 반환했을 때 무료 배송
> 상태를 만드는 계산이나, 오류 응답을 화면 상태로 바꾸는 로직을 빠르게 확인할 수 있습니다.
>
> Playwright는 실제 브라우저에서 렌더링, 버튼 상태, 오류 UI와 여러 화면으로 이어지는 사용자
> 흐름을 확인합니다. 화면 동작이 바뀐 작업은 빠른 unit test만 통과했다고 끝내지 않고 필요한
> 브라우저 흐름까지 확인할 수 있습니다.

### 14:10~15:30 - Backend

**[화면]** `Backend 테스트 · pytest`

**[말하기]**

> Backend의 pytest는 계산 규칙, 입력 경계, 상태 전이와 권한 같은 업무 규칙을 빠르게 확인합니다.
> integration과 e2e는 API 상태 코드, 응답 계약, DB와 외부 경계를 확인합니다. 저장소의 architecture
> 또는 OpenAPI 규칙은 별도의 harness 검사로 보호할 수도 있습니다.
>
> 여기서 FastAPI는 테스트 도구가 아니라 오늘 데모 API를 실행하는 프레임워크입니다. 테스트를
> 판정하는 도구는 pytest이고, 브라우저 실습에서는 Uvicorn으로 실행 중인 FastAPI에 실제 HTTP
> 요청을 보냅니다.

### 15:30~16:30 - 공통 품질 기준

**[화면]** `공통 품질 기준`

**[말하기]**

> Frontend와 Backend가 같은 테스트 파일을 관리할 필요는 없습니다. Frontend는 UI 상태와 사용자
> 흐름을, Backend는 업무 규칙과 API·DB 경계를 각자 소유합니다.
>
> 함께 공유할 것은 API 계약, 중요한 실패 시나리오와 재현 가능한 실행 결과입니다. 예를 들어
> "음수 지급 비율은 거절한다"는 업무 시나리오를 함께 합의하고, Backend는 422 계약을 검증하며,
> Frontend는 그 오류 응답을 올바른 UI로 표시하는지를 자기 저장소에서 검증할 수 있습니다.

**전환 문장**

> 그렇다면 AI에게 이 테스트들을 실행하라고 말하는 것만으로 충분할까요? 다음 장에서는 사람의
> 기대값, 저장소 규칙과 실제 명령을 어떻게 한 흐름으로 연결했는지 보겠습니다.

---

## 16:30~24:00 - AI와 TDD를 연결하는 실제 작업 순서

**[행동]** 상단 내비게이션의 `02 · 작업 흐름`을 선택한다.

### 16:30~18:10 - 두 아이디어의 출처 구분

**[화면]** `Kent Beck · TDD`, `OpenAI · Harness Engineering`

**[말하기]**

> 이 화면에는 서로 다른 두 아이디어가 있습니다. 먼저 Kent Beck의 Canon TDD에서는 테스트할
> 시나리오 목록을 만들고, 그중 정확히 하나를 실행 가능한 테스트로 만든 뒤, 모든 기존 테스트와
> 함께 통과시키고, 필요하면 GREEN에서 리팩터링하는 흐름을 가져왔습니다.
>
> OpenAI의 Harness Engineering은 TDD 방법론이 아닙니다. 사람이 의도를 제시하고 AI가 저장소의
> 문서, 표준 개발 도구와 피드백을 직접 사용할 수 있도록 작업 환경을 구성한다는 아이디어입니다.
>
> 지금 보시는 하네스는 두 자료의 공식 제품이나 복사본이 아닙니다. 이 발표 저장소에서 두 원칙을
> 실제 명령으로 연결해 보기 위해 만든 최소 예시입니다.

### 18:10~20:10 - Markdown 문서의 역할

**[화면]** `현재 저장소의 Markdown 문서`

**[말하기]**

> `plan.md`는 무엇을 할지 정합니다. 사람이 승인한 테스트 목록 중 이번에 진행할 항목 하나만
> 미완료로 두고, focused와 전체 테스트가 모두 통과한 뒤 완료 처리합니다.
>
> `AGENTS.md`는 어떻게 작업할지 정합니다. 현재 저장소에는 10개 규칙이 있습니다. 그중 오늘
> 시연에서 중요한 규칙은 유효한 동작 실패인지 확인할 것, 실패한 테스트를 삭제하거나 기대값을
> 낮추지 않을 것, 현재 테스트를 통과시키는 최소 제품 코드만 작성할 것, focused 다음에 전체
> 검증을 실행할 것입니다.
>
> Markdown 문서는 업무를 자동 실행하는 프로그램이 아닙니다. 사람과 AI가 같은 작업 순서를
> 읽기 위한 저장소 안의 계약입니다.

### 20:10~21:45 - 실행 가능한 최소 하네스

**[화면]** `harness.toml`, `scripts/tdd_harness.py`, `.harness/latest-run.json`

**[말하기]**

> `harness.toml`은 `AGENTS.md`와 `plan.md`의 위치, 그리고 focused, full, lint, type 네 명령의
> 실행 순서를 선언합니다.
>
> `scripts/tdd_harness.py`가 이 설정을 읽고 명령을 실제로 실행합니다. focused가 실패하면 바로
> 멈추고, 통과할 때만 전체 pytest, Ruff, Pyright로 넘어갑니다.
>
> `.harness/latest-run.json`에는 어떤 명령을 실행했고 종료 코드와 소요 시간이 얼마였는지
> 기록됩니다. 이것은 기계 실행 증거입니다. 반면 422가 정말 올바른 업무 기대값인지, RED가
> import 오류가 아니라 기능 부재로 실패했는지, diff가 적절한지는 사람이 판단합니다.

### 21:45~22:30 - 연결 확인 실행

**[행동]** 테스트용 Git Bash 창으로 전환하고 실행한다.

~~~bash
uv run python scripts/tdd_harness.py check
~~~

**[확인]** 두 문서, 네 gate와 evidence 경로가 출력되어야 한다.

**[말하기]**

> 이 명령은 테스트를 실행하지 않습니다. 문서와 명령, 결과 경로가 실제로 연결되어 있는지만
> 확인합니다. 즉 `AGENTS.md`만 적어 둔 것이 아니라 다음 실행 경로까지 저장소에 둔 상태입니다.

### 22:30~24:00 - 네 단계와 실습으로 전환

**[화면]** 브라우저로 돌아와 `EXPECTED → RED → GREEN → VERIFY` 네 단계를 짚는다.

**[말하기]**

> 첫째, 사람이 기대 결과를 정합니다. 둘째, 테스트가 아직 없는 동작 때문에 실패하는지
> 확인합니다. 셋째, 테스트를 바꾸지 않고 최소 제품 코드로 통과시킵니다. 넷째, 가까운 테스트만
> 통과한 것으로 끝내지 않고 전체 테스트와 정적 검사를 확인합니다.
>
> 화면의 `test_contract_budget.py` 명령은 하네스 사용 형식을 보여주는 정적인 예시입니다. 오늘
> 실제로 선택한 항목은 다음 장의 지급조건 음수 경계이며, `plan.md`에도 그 항목 하나만 미완료로
> 두었습니다. 이제 같은 흐름을 처음부터 끝까지 실행해 보겠습니다.

**[주의]** `Spec Kit`이나 `TDAD`는 현재 데모에 설치되어 있지 않으므로 본 흐름의 구성요소처럼
언급하지 않는다.

---

## 24:00~35:30 - 통합 라이브 시연

**[행동]** 상단 내비게이션의 `03 · 실습`을 선택한다.

이 시연의 한 줄 흐름은 다음과 같다.

~~~text
사람이 기대 422 승인
→ 브라우저에서 실제 200 관찰
→ focused pytest로 같은 차이 재현
→ 하네스가 RED에서 중단
→ AI에게 테스트 유지와 최소 변경 요청
→ 제품 코드 한 줄 수정
→ focused · full · lint · type GREEN
→ 브라우저에서 실제 422 PASS 확인
~~~

### 24:00~25:20 - 실습이 실제 운영 버그가 아님을 밝힌다

**[화면]** `LIVE TDD · INITIAL STATE`

**[말하기]**

> 오늘 자세히 볼 것은 첫 번째 Payment Terms 사례입니다. 합계는 100이지만 선금 비율이 -10인
> 요청입니다. 운영의 원본 validator에는 이미 음수 방지 조건이 있습니다. 발표에서는 TDD 흐름을
> 재현하기 위해 그 규칙을 축약한 학습용 코드에서 제약 한 줄을 의도적으로 뺀 상태로 시작합니다.
>
> 따라서 이것은 현재 운영 코드에 이 버그가 있다는 주장이 아닙니다. 실제 장애나 요구사항이
> 들어왔을 때 먼저 실패 테스트로 재현하고 최소 수정으로 닫는 과정을 안전하게 보여주기 위한
> 사례입니다.

`Expected 422`, `Actual 200`, 현재 제품 코드 `advance_payment_percentage: int`를 짚는다.

> 사람은 음수 지급 비율을 받을 수 없으므로 기대 결과를 422로 승인합니다. 하지만 현재 서버는
> 합계가 100이라는 조건만 만족하면 요청을 받아들여 200을 반환합니다. 이 기대와 실제의 차이가
> 오늘 해결할 한 가지 동작입니다.

### 25:20~26:20 - 브라우저에서 먼저 FAIL을 관찰한다

**[행동]** 아래 `Live Request`의 `Payment Terms` 버튼을 누른다.

**[확인]** 다음이 보여야 한다.

~~~text
Status: FAIL
Expected: 422
Actual: 200
Request: advance=-10, interim=50, final=60
~~~

**[말하기]**

> 지금 브라우저가 실행 중인 FastAPI에 실제 POST 요청을 보냈습니다. 합계는 100이기 때문에 현재
> 모델은 요청을 승인했고 실제 응답은 200입니다. 화면이 FAIL이라고 표시하는 이유는 서버가
> 죽었기 때문이 아니라, 사람이 승인한 기대값 422와 실제 200이 다르기 때문입니다.

### 26:20~28:10 - 같은 차이를 pytest와 하네스로 재현한다

**[행동]** IDE에서 `tests/test_contract_payment_terms.py`의
`test_rejects_negative_payment_percentage_even_when_sum_is_100`를 잠깐 보여준다.

**[말하기]**

> 테스트도 같은 요청을 보냅니다. `-10 + 50 + 60`은 100이지만, 개별 지급 비율은 0 이상이어야
> 한다는 기대를 `status_code == 422`와 오류 문구로 고정했습니다. 이 테스트의 expected value는
> 사람이 승인한 업무 계약이므로 GREEN 단계에서 바꾸지 않습니다.

**[행동]** 테스트용 Git Bash에서 다음 명령을 실행한다.

~~~bash
uv run python scripts/tdd_harness.py verify --focused tests/test_contract_payment_terms.py::test_rejects_negative_payment_percentage_even_when_sum_is_100
~~~

**[확인]** 핵심 출력은 다음과 같아야 한다.

~~~text
[1/4] focused
FAILED
E assert 200 == 422
STOP: focused failed with exit code 1
Evidence: .harness/runs/....json
Latest: .harness/latest-run.json
~~~

**[말하기]**

> 하네스는 첫 번째 focused test에서 멈췄습니다. 전체 테스트, lint와 type을 실행하지 않은 것은
> 오류가 아니라 설계된 동작입니다. 지금은 가장 가까운 동작도 통과하지 못했기 때문에 뒤 단계를
> 실행할 이유가 없습니다.
>
> 그리고 이 실패는 import, 문법 또는 의존성 문제가 아닙니다. 서버는 정상적으로 200을
> 반환했지만 업무 기대값은 422였습니다. 따라서 기능 부재 때문에 실패한 유효한 RED라고 사람이
> 확인할 수 있습니다.

**[선택 행동]** 시간이 있으면 다음 명령으로 한 단계만 기록된 JSON을 10초 정도 보여준다.

~~~bash
grep -E '"status"|"name"|"exit_code"' .harness/latest-run.json
~~~

### 28:10~30:20 - AI에게 범위가 있는 요청을 보낸다

**[화면]** 브라우저의 `AI Request (RED 승인 후 요청)`을 다시 보여준다.

**[말하기]**

> 이제 AI에게 "알아서 고쳐줘"라고 하지 않겠습니다. 어떤 실패를 승인했는지, 무엇을 바꾸면
> 안 되는지, 어느 범위까지만 구현할지, 어떤 명령으로 완료를 확인할지를 같이 줍니다.

**[행동]** Codex 또는 Claude에 다음 프롬프트를 그대로 보낸다.

~~~text
현재 저장소의 plan.md에서 Live Demo Current Item 하나만 진행해줘.
AGENTS.md의 10개 규칙을 지켜.

방금 focused test는 환경 오류가 아니라 Expected 422 / Actual 200의
업무 동작 차이로 실패한 유효한 RED다.

tests/test_contract_payment_terms.py의 실패 테스트를 수정, 삭제, skip하거나
기대값을 낮추지 마.
선금 지급 비율이 음수이면 422로 거절하는 최소 제품 코드만 작성해.
다른 API, 모델 구조와 테스트는 변경하지 마.
PRESENTATION.md의 발표자 대본 변경도 건드리지 마.

수정 후 아래의 같은 verify 명령을 실행해 focused, full, lint, type을 확인해.
모두 통과한 뒤에만 plan.md의 현재 항목을 완료 처리해.
실제 변경 diff와 각 검증 결과를 요약하고 커밋은 하지 마.

uv run python scripts/tdd_harness.py verify --focused tests/test_contract_payment_terms.py::test_rejects_negative_payment_percentage_even_when_sum_is_100
~~~

AI가 작업하는 동안 다음을 말한다.

> 이 프롬프트의 핵심은 길이가 아닙니다. 업무 기대값은 422, 바꾸면 안 되는 것은 실패 테스트,
> 허용된 제품 변경은 현재 음수 경계, 완료 명령은 같은 verify라는 네 가지 경계가 명확하다는
> 점입니다.
>
> AI가 더 큰 구조를 제안하더라도 현재 테스트 하나를 통과시키는 데 필요하지 않으면 이번 단계에
> 넣지 않습니다. 이것이 코드 생성을 막는 규칙이 아니라, 한 번에 검토할 변경 범위를 줄이는
> 규칙입니다.

**[확인]** AI가 제안하거나 적용한 핵심 제품 diff는 다음 한 줄이어야 한다.

~~~diff
-    advance_payment_percentage: int
+    advance_payment_percentage: int = Field(..., ge=0)
~~~

`Field`는 이미 다른 필드에서 사용하고 import되어 있으므로 새 구조나 의존성이 필요하지 않다.

### 30:20~32:45 - 같은 명령으로 GREEN과 전체 gate를 확인한다

AI가 verify를 이미 실행했으면 결과를 함께 확인한다. 출력이 화면에서 잘리지 않았거나 청중에게
다시 보여줄 필요가 있으면 테스트용 Git Bash에서 같은 명령을 한 번 더 실행한다.

~~~bash
uv run python scripts/tdd_harness.py verify --focused tests/test_contract_payment_terms.py::test_rejects_negative_payment_percentage_even_when_sum_is_100
~~~

**[확인]** 현재 저장소 기준 핵심 결과는 다음과 같다.

~~~text
[1/4] focused ... 1 passed
[2/4] full    ... 28 passed
[3/4] lint    ... All checks passed!
[4/4] type    ... 0 errors, 0 warnings, 0 informations
~~~

**[말하기]**

> 같은 명령을 다시 실행했습니다. 이번에는 focused test가 통과했기 때문에 하네스가 전체 28개
> 테스트, Ruff와 Pyright까지 이어서 실행했습니다.
>
> focused는 지금 수정한 규칙에 대한 빠른 피드백이고, full suite는 주변 계약의 회귀 확인이며,
> Ruff와 Pyright는 기본 코드 오류와 타입 문제를 확인합니다. 네 단계가 모두 통과한 뒤에만
> `plan.md`의 현재 항목을 완료로 바꿉니다.
>
> 중요한 점은 AI가 "수정했습니다"라고 말한 것이 완료 근거가 아니라는 것입니다. 같은 test
> runner가 실패와 성공을 모두 보여주고, 실행 명령과 종료 코드가 JSON으로 남은 것이 완료
> 증거입니다. 업무 기대값과 한 줄 diff를 승인하는 책임은 여전히 사람에게 있습니다.

**[선택 행동]** 최신 JSON에서 네 단계가 모두 기록됐는지 짧게 보여준다.

~~~bash
grep -E '"status"|"name"|"exit_code"' .harness/latest-run.json
~~~

### 32:45~34:00 - 브라우저에서 같은 요청이 PASS로 바뀌었는지 확인한다

**[행동]** 서버 터미널에서 reload와 `Application startup complete`를 확인한 뒤 브라우저로
돌아가 `Payment Terms` 버튼을 다시 누른다.

**[확인]** 다음이 보여야 한다.

~~~text
Status: PASS
Expected: 422
Actual: 422
~~~

**[말하기]**

> 같은 HTTP 요청을 다시 보냈습니다. 이번에는 Pydantic의 `ge=0`, 즉 0 이상이라는 입력 경계에서
> 음수를 거절했고, 실제 응답이 기대한 422와 같아져 PASS가 됐습니다.
>
> pytest는 `TestClient`로 FastAPI app을 같은 프로세스에서 호출해 자동화된 회귀 증거를 만들고,
> 이 버튼은 Uvicorn으로 실행 중인 서버에 실제 HTTP 요청을 보내 청중이 요청과 응답을 직접 보게
> 합니다. 둘은 같은 업무 규칙을 서로 다른 경로에서 확인합니다.

### 34:00~35:30 - 나머지 두 규칙을 짧게 비교한다

**[행동]** `Budget Shape` 버튼을 누른다.

**[말하기]**

> 두 번째는 조건부 입력 형태입니다. `CONFIRMED_AMOUNT` 방식은 제작비와 총예산을 함께 보내는
> 정상 요청이므로 기대와 실제가 모두 200입니다.

**[확인]** `PASS`, `Expected 200`, `Actual 200`.

**[행동]** `Submission Material` 버튼을 누른다.

**[말하기]**

> 세 번째는 필드 간 의존 관계입니다. 첨부 형식을 선택했지만 실제 파일을 가리키는 `file_id`가
> 없으므로 기대와 실제가 모두 422입니다.

**[확인]** `PASS`, `Expected 422`, `Actual 422`.

세 사례를 묶는다.

> 첫 사례는 숫자 경계, 두 번째는 조건부 입력 형태, 세 번째는 필드 간 의존 관계입니다. 테스트
> 개수를 과시하는 것이 아니라, 서로 다른 종류의 업무 위험을 같은 입력과 명령으로 반복 확인할
> 수 있게 만든 것입니다.

**[시간 부족]** AI 실행이 길어지면 Budget과 Submission Material 버튼은 생략한다. Payment Terms의
FAIL → RED → 한 줄 diff → 전체 GREEN → PASS가 오늘 실습의 필수 흐름이다.

---

## 35:30~39:00 - 우리 회사에서 필요한 이유와 적용 범위

**[행동]** 상단 내비게이션의 `04 · 적용`을 선택한다.

### 35:30~37:20 - 테스트가 효과적인 세 지점

**[화면]** `WHY TDD · 필요한 이유`

**[말하기]**

> 이 흐름을 회사 상황에 연결해 보겠습니다. 서비스가 성장하면서 Frontend, Backend, SSO와 여러
> 기능이 별도 Git 저장소로 나뉘어 관리되는 것은 자연스러운 결과입니다. 이것은 하나의 Git
> 저장소에 모든 프로젝트가 있는 모노레포라기보다, 각 프로젝트가 독립된 Git 이력을 가진
> 멀티레포 구조에 가깝습니다.
>
> 첫 번째로, 멀티레포에서는 AI가 현재 연 저장소의 코드만 보고 연결된 업무 계약을 모두 안다고
> 기대하기 어렵습니다. 각 저장소가 책임지는 기대 동작과 API 경계를 테스트로 고정하면 변경의
> 완료 지점을 더 분명하게 만들 수 있습니다.
>
> 두 번째로, TVCF를 기반으로 오랫동안 축적된 데이터, 내부 validator, 상태 조합, null과 중복
> 조건은 코드 한 파일만 읽어서 모두 파악하기 어렵습니다. 이 중 코드로 재현할 수 있는 중요한
> 조건을 실제 입력과 기대 결과로 남기면 AI와 사람 모두 같은 기준으로 확인할 수 있습니다.
>
> 세 번째로, 리팩토링과 디버깅에서는 오류를 먼저 실패 테스트로 재현하면 원인의 범위를 줄일 수
> 있습니다. 수정 뒤 같은 테스트가 통과하고 전체 회귀까지 통과하면, 다음 작업자도 왜 그 조건이
> 필요한지 실행으로 확인할 수 있습니다.
>
> AI를 사용해 코드 생성량이 늘어날수록 이 기준은 더 중요해집니다. 문서 설명만으로 모든 코드를
> 통제하려 하기보다, 중요한 업무 행동 하나와 실행할 테스트 하나를 연결하면 과도한 구현이나
> 요구보다 넓어진 설계를 검토하기 쉬워집니다.

### 37:20~38:30 - 과하게 기대하지 않을 부분

**[화면]** `LIMITS · 적용 한계`

**[말하기]**

> 다만 TDD가 모든 문제를 해결하지는 않습니다. 첫째, 멀티레포의 배포 순서, 버전과 권한 연결은
> API 계약 관리와 CI가 함께 다뤄야 합니다.
>
> 둘째, 운영 DB의 실제 데이터, 네트워크와 외부 서비스 문제는 unit test만으로 재현할 수 없습니다.
> integration, E2E, 모니터링과 운영 로그가 함께 필요합니다.
>
> 셋째, 단순 DTO나 프레임워크 기본 동작까지 모두 Test-first로 강제할 필요는 없습니다. 데이터
> 제약, 핵심 업무 규칙, 재현 가능한 오류와 리팩토링처럼 실패 비용이 큰 지점부터 적용하는 것이
> 현실적입니다.

### 38:30~39:00 - 적용 제안

**[말하기]**

> 그래서 전면 도입보다 작은 기준부터 제안합니다. 운영에서 다시 만나고 싶지 않은 오류 하나를
> 고르고, 사람이 기대 결과를 한 문장으로 승인하고, 가장 가까운 테스트 하나로 RED를 재현합니다.
> AI에는 그 테스트를 바꾸지 말라는 경계와 전체 확인 명령을 같이 주고, 실제 도움이 확인된 핵심
> 규칙부터 팀의 방식으로 넓혀 가는 것입니다.

**전환 문장**

> 오늘 시연한 한 줄 검증이 회사의 모든 문제를 해결하지는 않습니다. 하지만 코드에서 재현할 수
> 있는 오류는 코드 단계에서 잡고, AI가 만든 변경의 완료를 같은 명령으로 다시 확인하는 출발점은
> 될 수 있습니다.

---

## 39:00~40:00 - Closing

**[행동]** 페이지 맨 아래 `Closing`으로 이동한다.

**[화면]**

~~~text
AI 시대의 TDD는
테스트 대필 기술이 아니다.
사람의 의도를 실행 환경으로 만든다.
~~~

**[말하기]**

> 오늘은 AI가 테스트를 얼마나 잘 만들어 주는지를 보여드린 것이 아닙니다. 사람이 업무 기대값을
> 승인하고, AI가 테스트를 함부로 바꾸지 않게 범위를 주고, 실제 runner의 RED와 GREEN으로 완료를
> 판단하는 흐름을 보여드렸습니다.
>
> Frontend와 Backend는 서로 다른 코드와 테스트를 소유합니다. 다만 API 계약, 중요한 실패
> 시나리오와 재현 가능한 완료 증거는 함께 공유할 수 있습니다.
>
> AI가 코드를 빨리 만들수록, 무엇이 맞는지 판단하는 기준은 더 작고 명확하며 반복 가능해야
> 합니다. AI 시대의 TDD는 테스트 대필 기술이 아니라, 사람의 의도를 실행 가능한 완료 기준으로
> 만드는 방법입니다. 감사합니다.

질문이 있으면 다음 문장으로 넘긴다.

> 지금 보신 하네스 구조, 실제 회사 코드에 적용할 범위, 또는 Frontend와 Backend에서 어떤
> 시나리오부터 시작할지 질문 주시면 현재 데모 기준으로 말씀드리겠습니다.

---

## 라이브 시연용 한 화면 치트시트

발표 중에는 아래 순서만 놓치지 않으면 된다.

### 1. 서버

~~~bash
cd /c/Users/gram/tvcf/AI_TEST_CODE
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
~~~

### 2. 연결 확인

~~~bash
uv run python scripts/tdd_harness.py check
~~~

### 3. 브라우저 RED

~~~text
Payment Terms 클릭
Expected 422 / Actual 200 / FAIL
~~~

### 4. 하네스 RED

~~~bash
uv run python scripts/tdd_harness.py verify --focused tests/test_contract_payment_terms.py::test_rejects_negative_payment_percentage_even_when_sum_is_100
~~~

### 5. AI 요청에서 반드시 말할 것

~~~text
기대 결과는 422다.
실패 테스트를 수정하지 않는다.
음수 선금 경계의 최소 제품 코드만 수정한다.
다른 API와 구조는 건드리지 않는다.
같은 verify 명령으로 전체 gate까지 확인한다.
커밋하지 않는다.
~~~

### 6. 예상 한 줄 diff

~~~python
advance_payment_percentage: int = Field(..., ge=0)
~~~

### 7. 하네스 GREEN

~~~text
focused: 1 passed
full: 28 passed
lint: All checks passed!
type: 0 errors
~~~

### 8. 브라우저 GREEN

~~~text
Payment Terms 다시 클릭
Expected 422 / Actual 422 / PASS
~~~

### 9. 보조 사례

~~~text
Budget Shape: Expected 200 / Actual 200 / PASS
Submission Material: Expected 422 / Actual 422 / PASS
~~~

---

## 라이브 시연 장애 대응

### 영상이 재생되지 않는다

1. 해당 탭의 `YouTube 원본 전체 영상에서 보기`를 누른다.
2. 원본도 막히면 영상별 한글 요점 세 줄만 읽고 다음 단계로 이동한다.
3. 영상 문제 해결에 30초 이상 쓰지 않는다.

### 발표 페이지가 열리지 않는다

서버 터미널에서 다음을 확인한다.

~~~bash
cd /c/Users/gram/tvcf/AI_TEST_CODE
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
~~~

포트 8000이 이미 사용 중이면 기존 서버를 종료하거나 8001로 실행하고
`http://127.0.0.1:8001`을 연다. API 버튼은 같은 origin의 상대 경로를 사용하므로 그대로 동작한다.

### 시작부터 Payment Terms가 PASS다

`app/main.py`에서 다음 줄이 이미 GREEN인지 확인한다.

~~~python
advance_payment_percentage: int = Field(..., ge=0)
~~~

발표 시작 상태로 되돌리려면 IDE에서 `= Field(..., ge=0)`만 제거하고 저장한 뒤 Uvicorn reload를
기다린다. 테스트 파일은 수정하지 않는다. `plan.md`의 Live Demo Current Item도 미완료인지 확인한다.

### focused test가 import 또는 의존성 오류로 실패한다

이 실패를 RED라고 설명하지 않는다. 다음을 먼저 실행한다.

~~~bash
cd /c/Users/gram/tvcf/AI_TEST_CODE
uv sync
uv run python scripts/tdd_harness.py check
~~~

환경이 복구된 뒤 focused test를 다시 실행한다. 유효한 RED는 서버가 200을 반환했지만 테스트가
422를 기대해 실패하는 동작 차이다.

### AI가 실패 테스트를 수정한다

AI 실행을 멈추고 다음과 같이 말한다.

> 지금 변경은 사람이 승인한 expected value를 움직였으므로 적용하지 않겠습니다. 테스트 변경을
> 되돌리고 제품 코드의 음수 경계만 최소 수정해 주세요.

IDE의 AI diff에서 테스트 변경만 거부하거나 실행 직후 Undo한다. `git restore .`처럼 발표 대본까지
함께 되돌릴 수 있는 넓은 명령은 사용하지 않는다.

### AI가 구조를 크게 바꾼다

다음 기준으로 거부한다.

> 현재 RED는 기존 Pydantic 필드 경계 한 줄로 해결할 수 있습니다. 새 추상화, API 또는 파일은
> 이번 테스트를 통과시키는 데 필요하지 않으므로 제외해 주세요.

AI 응답을 기다릴 시간이 없으면 IDE에서 다음 한 줄을 직접 입력하고 같은 verify 명령을 실행한다.

~~~python
advance_payment_percentage: int = Field(..., ge=0)
~~~

직접 입력했더라도 발표의 핵심은 유지된다. 사람의 기대값, 테스트 유지, 최소 구현과 전체 검증을
같은 순서로 보여주면 된다.

### Uvicorn reload가 늦다

서버 터미널에 변경 감지와 새 server process 시작 메시지가 나온 뒤, 다음 문장이 다시 나타날
때까지 기다린다.

~~~text
Application startup complete
~~~

Uvicorn 버전에 따라 앞의 문구는 다를 수 있다. `Application startup complete`로 reload 완료를
확인한 뒤 브라우저 버튼을 다시 누른다.

### full gate에서 예상하지 못한 테스트가 실패한다

숨기거나 PASS라고 말하지 않는다.

> focused 동작은 해결됐지만 전체 회귀에서 다른 실패가 발견됐습니다. 이 경우 하네스 기준으로는
> 완료가 아니며 `plan.md`도 완료 처리하지 않습니다. 오늘 시연의 목적대로 첫 실패에서 멈추고
> 원인을 별도 작업으로 분리하겠습니다.

발표 시간이 부족하면 준비해 둔 예상 GREEN 출력만 설명하고, 실제 결과가 완료 조건을 만족하지
않았다는 사실은 그대로 밝힌다.

### 시간이 3분 이상 밀린다

다음 순서로 줄인다.

1. JSON `grep` 확인을 생략한다.
2. Budget와 Submission Material 버튼을 생략한다.
3. Video 2와 Video 3의 재생 시간을 줄이고 한글 요점을 읽는다.
4. 적용 한계 세 항목을 한 문장으로 묶는다.
5. Payment Terms의 FAIL → RED → 한 줄 수정 → 전체 GREEN → PASS는 생략하지 않는다.

---

## 리허설 또는 발표 후 RED 상태로 되돌리기

발표를 다시 해야 한다면 먼저 현재 상태를 확인한다.

~~~bash
git diff -- app/main.py plan.md
~~~

두 파일이 GREEN 상태이고 diff가 비어 있으면, 발표 전에 저장한 패치를 적용한다.

~~~bash
git apply .harness/live-demo-red.patch
~~~

focused test가 다시 `Expected 422 / Actual 200`으로 실패하는지 확인한다.

~~~bash
uv run pytest tests/test_contract_payment_terms.py::test_rejects_negative_payment_percentage_even_when_sum_is_100 -vv
~~~

패치를 만들지 않았다면 IDE에서 다음 두 부분만 되돌린다.

1. `app/main.py`: `advance_payment_percentage: int = Field(..., ge=0)`을
   `advance_payment_percentage: int`로 바꾼다.
2. `plan.md`: Live Demo Current Item을 `[ ]` 미완료와 `Expected 422 / Actual 200` 현재 RED 설명으로
   바꾼다.

테스트 파일은 수정하지 않는다. 이 RED 상태는 발표 시작점이므로 커밋하지 않는다.

---

## 예상 질문과 답변

### 우리 회사 구조는 모노레포인가요?

하나의 상위 폴더에 여러 프로젝트가 있어도 각 프로젝트가 독립된 `.git`을 가지면 멀티레포 또는
Polyrepo다. 모노레포는 하나의 Git 저장소 안에 여러 애플리케이션이나 패키지가 함께 있는 구조다.
저장소 구성만으로 마이크로서비스 여부를 판단하지는 않는다.

### 기존 회사 테스트가 부족하다는 발표인가요?

아니다. 이미 Frontend와 Backend의 unit, integration, e2e와 harness가 서로 다른 위험을 보호한다.
이 발표는 기존 테스트를 평가하는 것이 아니라, AI가 변경할 때 업무 기대값과 실행할 테스트를
연결하고 결과를 반복 확인하는 작은 작업 방식을 제안한다.

### Frontend와 Backend가 같은 테스트를 관리해야 하나요?

아니다. Frontend는 화면 상태와 사용자 흐름을, Backend는 업무 규칙과 API·DB 경계를 각자
소유한다. 공유하는 것은 같은 테스트 파일이 아니라 API 계약, 중요한 실패 시나리오와 실행 결과다.

### 이것이 Kent Beck이 말한 AI 하네스인가요?

아니다. Kent Beck의 Canon TDD에서 테스트 목록을 만들고 그중 하나를 실행 가능한 테스트로 만든
뒤 통과시키고 필요하면 리팩터링하는 순서를 참고했다. `AGENTS.md`, `plan.md`, `harness.toml`과
Python 실행기는 이 발표 저장소에서 그 순서를 AI 작업에 적용해 본 최소 구현이다.

### OpenAI가 이 `harness.toml` 구조를 권장했나요?

아니다. OpenAI의 Harness Engineering 글에서 사람은 의도를 제시하고, AI가 저장소 지식과 표준
개발 도구, 테스트와 피드백을 직접 사용할 수 있게 환경을 구성한다는 아이디어를 참고했다. 현재
TOML 구조와 실행 순서는 발표를 위해 직접 만든 예시다.

### 테스트도 AI가 쓰면 AI가 자기 답을 채점하는 것 아닌가요?

AI가 테스트 초안을 만들 수는 있지만 업무 정답과 expected value는 사람이 승인한다. 테스트가
제품 코드보다 먼저 유효한 동작 이유로 실패하는지 확인하고, GREEN에서 테스트를 삭제하거나
기대값을 낮추지 못하게 하며, 사람은 최종 diff와 실행 결과를 함께 검토한다.

### 왜 이미 있는 테스트를 일부러 실패하게 만들었나요?

40분 발표에서 새 기능의 테스트 작성부터 모든 코드를 만들기보다, bug-fix TDD의 핵심인 오류 재현,
유효한 RED, 테스트 유지, 최소 수정과 전체 회귀를 안정적으로 보여주기 위해서다. 운영 원본에는 이미
음수 방지 조건이 있고, 데모 복제본에서만 그 한 줄을 뺐다는 점을 먼저 밝힌다.

### 세 API가 실제 운영 endpoint인가요?

아니다. 실제 command validator의 지급조건, 예산 형태와 제출자료 규칙을 가져왔지만 DB, 인증,
저장과 알림을 제외하고 검증만 분리한 발표용 FastAPI endpoint다.

### 왜 브라우저 버튼과 pytest가 둘 다 필요한가요?

pytest는 자동화된 회귀 증거를 만들고, 브라우저 버튼은 같은 규칙이 실행 중인 서버의 HTTP 요청과
응답에서 어떻게 보이는지 청중이 확인하게 한다. pytest의 `TestClient`와 브라우저의 Uvicorn 요청은
서로 다른 실행 경로지만 같은 업무 기대값을 확인한다.

### 왜 Python Backend만 실습하나요?

발표자가 직접 설명할 수 있는 계약 규칙을 짧은 시간에 재현하기 위해서다. Frontend는 Jest,
Vitest와 Playwright의 역할을 설명하고, 같은 API 계약과 실패 시나리오를 자기 저장소의 테스트로
검증한다는 공통 기준에 집중한다.

### 모든 PR에서 전체 TDD와 전체 테스트를 강제해야 하나요?

그럴 필요는 없다. 데이터 제약, 핵심 업무 규칙, 재현 가능한 오류와 리팩토링처럼 실패 비용이 큰
변경부터 적용하고, 먼저 가까운 focused test로 피드백을 얻은 뒤 저장소의 기존 full gate를
실행하는 정도로 시작할 수 있다. 실제 도움이 확인된 범위부터 팀 기준으로 발전시키는 것이 좋다.

### 테스트가 통과하면 운영 장애가 없어지나요?

아니다. 코드로 재현 가능한 동작과 회귀를 줄이는 데 도움을 줄 뿐이다. 운영 DB 데이터, 네트워크,
외부 서비스, 배포와 권한 문제는 integration, E2E, 계약 관리, 모니터링과 운영 로그가 함께 필요하다.

---

## 발표에서 사용하는 출처와 주장 범위

- [Kent Beck, Canon TDD](https://newsletter.kentbeck.com/p/canon-tdd): 테스트 시나리오 목록을 만들고
  정확히 하나를 실행 가능한 테스트로 바꾼 뒤 통과시키고 선택적으로 리팩터링하는 흐름의 근거다.
- [Kent Beck, Sustainable Augmented Development · YOW! 2025](https://www.youtube.com/watch?v=sMujMp4h_EY&t=24s):
  AI로 달라지는 개발 방식과 TDD 결합에 대한 문제 제기 구간으로 사용한다.
- [The Pragmatic Engineer, TDD, AI agents and coding with Kent Beck](https://www.youtube.com/watch?v=aSXaxOdVtAQ&t=3024s):
  AI가 실패를 해결하는 과정에서 테스트를 바꾸려 한 위험 사례 구간으로 사용한다.
- [GitHub 공식 영상, Test-driven development with GitHub Copilot](https://www.youtube.com/watch?v=arn6hqERKn4&t=366s):
  요구조건, 테스트 생성, RED, 구현과 GREEN 순서를 보여주는 공식 사례다.
- [GitHub Blog, TDD with GitHub Copilot](https://github.blog/ai-and-ml/github-copilot/github-for-beginners-test-driven-development-tdd-with-github-copilot/):
  2025년 GitHub 공식 글의 Red, Green, Refactor와 Copilot 프롬프트 설명을 참고한다.
- [OpenAI, Harness Engineering](https://openai.com/index/harness-engineering/): 사람이 의도를 제시하고
  AI가 저장소 지식, 개발 도구와 피드백을 직접 사용할 수 있게 환경을 구성한다는 아이디어를
  참고한다. 현재 저장소의 하네스 구현과 동일한 제품이라고 말하지 않는다.
- [FastAPI 공식 Testing 문서](https://fastapi.tiangolo.com/tutorial/testing/): `TestClient`를 사용한
  in-process API 테스트 설명의 근거다.
- [pytest 공식 문서](https://docs.pytest.org/en/stable/): focused node ID와 전체 테스트 실행기의 근거다.

발표 본문에서는 출처를 길게 설명하지 않는다. 질문이 나오면 위 주장 범위를 기준으로 답한다.

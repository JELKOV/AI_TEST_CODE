# AI-assisted TDD 발표 스크립트

## 발표 전 실행

Git Bash 창 하나에서:

~~~bash
cd /c/Users/tvcf_project/AI_TDD_FastAPI_Demo
uv sync
uv run pytest
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
~~~

브라우저에서 <http://127.0.0.1:8000>을 연다.

검증용 Git Bash 창을 하나 더 열어 둔다.

~~~bash
cd /c/Users/tvcf_project/AI_TDD_FastAPI_Demo
~~~

---

## 0:00–0:50 — 기: 왜 이 주제를 골랐는가

> 오늘 발표할 내용은 AI가 FastAPI 안에서 동작하는 기능이 아닙니다.
> AI 코딩 에이전트에게 실제 업무 코드를 맡길 때, 어떻게 범위를 통제하고
> 결과를 신뢰할 것인가에 대한 개발 방식입니다.
>
> 처음에는 일반적인 예약 충돌 예제로 만들었습니다. 이해는 쉬웠지만 제가 해 온
> AdMarket 업무와 연결되지 않아 경험을 말하기 어려웠습니다. 그래서 실제
> AdMarket 테스트에서 계약 지급조건 규칙을 가져와 작은 실습으로 다시 만들었습니다.
>
> 핵심 문장은 하나입니다. AI가 구현 속도를 높이고, 사람이 승인한 테스트가
> AI의 행동 범위를 통제합니다.

`AI-assisted TDD`는 Kent Beck이 별도로 명명한 공식 방법론이 아니다.
[Canon TDD](https://newsletter.kentbeck.com/p/canon-tdd)의 흐름을 AI 코딩 작업에
적용한 이 프로젝트의 설명이다.

## 0:50–1:40 — 실제 AdMarket 경험과 연결

화면 오른쪽의 `AdMarket Contract Payment Terms`를 가리킨다.

> 광고 계약에는 선금, 중도금, 잔금이 있습니다. 여기에는 단순 CRUD보다 중요한
> 업무 규칙이 있습니다.
>
> 첫째, 세 비율의 합계는 정확히 100이어야 합니다.
> 둘째, 세 지급 시점은 중복될 수 없습니다.
> 셋째, 계약 체결보다 기획 확정이 먼저 오는 식으로 지급 순서가 뒤집힐 수 없습니다.

실제 근거는 다음 두 곳이다.

~~~text
admarket_fastapi_BE/tests/unittests/contract/service_test.py
  └─ TestPaymentTermsCommandValidation

admarket_fastapi_BE/app/contract/application/command.py
  └─ PaymentTermsCommand.validate_payment_split()
~~~

> 운영 코드를 통째로 복사하지는 않았습니다. DB, 인증, 계약 저장, 알림은 발표
> 핵심이 아니어서 제외하고, 제가 설명할 수 있는 업무 불변조건과 테스트 사례만
> 현재 데모로 옮겼습니다.

## 1:40–2:30 — 세 역할

화면 상단의 세 카드를 왼쪽부터 설명한다.

> AI Agent는 사람이 승인한 `plan.md`의 다음 테스트 하나에 필요한 코드를 제안합니다.
>
> Human은 합계가 100이어야 한다는 것처럼 업무 정답과 기대 결과를 결정하고,
> 테스트와 diff를 검토합니다.
>
> pytest는 같은 입력으로 코드를 반복 실행해 통과 여부를 판정합니다.
> AI가 “완료했습니다”라고 말하는 것은 증거가 아닙니다.

~~~text
실제 업무 규칙
      ↓
사람이 승인한 테스트 하나
      ↓
의도한 행동 차이로 실패하는 RED
      ↓
AI의 최소 구현
      ↓
focused pytest → full pytest
      ↓
사람의 diff·설계 검토
~~~

## 2:30–3:35 — 승: RED → GREEN → REFACTOR

화면 왼쪽의 세 카드를 가리킨다.

> 합계 오류 사이클을 예로 들겠습니다.
>
> RED에서 20%, 30%, 40%, 즉 합계 90인 요청은 422여야 한다는 테스트를 먼저
> 작성했습니다. 당시 API는 입력을 그대로 승인했기 때문에 실제 200이 나왔습니다.
> 기대 422, 실제 200이라는 업무 행동 차이가 유효한 RED입니다.
>
> 서버가 안 켜지거나 import가 실패한 것은 RED가 아닙니다. 제품 행동까지 도달하지
> 못한 환경 오류이기 때문입니다.
>
> GREEN에서는 실패한 테스트를 바꾸지 않고 세 비율의 합계가 100인지 확인하는
> 조건만 추가했습니다. 다음 규칙인 중복과 순서는 각각 별도의 테스트 사이클로
> 진행했습니다.
>
> 모든 테스트가 통과한 뒤에만 이름과 구조를 정리합니다. 이때 새 동작을 섞지
> 않는 단계가 REFACTOR입니다.

실제 기록은 [docs/TDD_CYCLES.md](docs/TDD_CYCLES.md)에 있다.

~~~bash
uv run pytest tests/test_contract_payment_terms.py::test_rejects_payment_percentage_sum_not_100 -vv
uv run pytest
~~~

## 3:35–5:05 — 전: 실제 API 세 가지 실행

### 1. Valid Terms (정상 지급조건)

`Valid Terms` 버튼을 누른다.

> 선금 30, 중도금 30, 잔금 40이고 지급 시점도 정상 순서입니다.
> 화면의 JavaScript가 지금 실행 중인 FastAPI의
> `POST /contracts/payment-terms/validate`를 호출했습니다.
> 기대값과 실제값이 모두 200이므로 PASS입니다.

Request와 Response 패널의 JSON을 가리킨다.

### 2. Invalid Total (합계 오류)

`Invalid Total` 버튼을 누른다.

> 이번에는 20, 30, 40으로 합계가 90입니다. HTTP 형식은 맞지만 계약 업무
> 규칙에는 맞지 않으므로 422입니다. 응답의 Pydantic validation detail에서
> `payment percentages must sum to 100`을 확인할 수 있습니다.

### 3. Invalid Order (순서 오류)

`Invalid Order` 버튼을 누른다.

> 선금 지급 시점을 기획 확정으로 두고 중도금 지급 시점을 계약 체결로 두었습니다.
> 금액 합계는 100이지만 시간 순서가 뒤집혔기 때문에 422입니다.
>
> 합계 테스트만 있었다면 이 결함은 놓칩니다. 서로 다른 업무 이유는 서로 다른
> 테스트로 고정해야 실패 원인을 바로 알 수 있습니다.

지급 시점 중복 사례도 터미널 테스트로 고정되어 있다.

~~~bash
uv run pytest tests/test_contract_payment_terms.py::test_rejects_duplicate_payment_timings -vv
~~~

## 5:05–5:55 — 코드가 실제로 돌아가는 위치

`app/main.py`를 열어 다음 순서로 설명한다.

> `ContractPaymentTiming`은 API가 받을 수 있는 네 개의 지급 시점을 제한합니다.
>
> `ContractPaymentTerms`는 여섯 개 필드를 받고 하나의 정책 validator에서 합계,
> 중복, 시간 순서를 차례로 판정합니다.
>
> FastAPI는 route 함수에 들어가기 전에 Pydantic 모델을 검증합니다. 검증에
> 실패하면 route 본문은 실행되지 않고 422가 반환됩니다. 모두 통과한 경우에만
> route가 검증된 입력을 200으로 반환합니다.

핵심 코드는 다음 의미다.

~~~python
total = advance + interim + final
if total != 100:
    raise ValueError(...)

if len(set(timings)) != len(timings):
    raise ValueError(...)

if positions != sorted(positions):
    raise ValueError(...)
~~~

> 파일을 여러 레이어로 나누지 않은 이유는 운영 아키텍처를 재현하는 것이 아니라
> AI-TDD의 짧은 피드백 루프를 보여주는 프로젝트이기 때문입니다.

## 5:55–6:35 — 결: 실행 증거

두 번째 Git Bash 창에서 실행한다.

~~~bash
uv run pytest tests/test_contract_payment_terms.py -vv
uv run pytest
uv run ruff check .
uvx pyright
~~~

> focused suite는 계약 규칙만 빠르게 확인합니다. 이어서 full suite로 발표 화면과
> OpenAPI 계약까지 회귀가 없는지 확인합니다. Ruff와 Pyright는 스타일과 타입
> 문제를 별도로 확인합니다.
>
> 이 출력이 완료 증거입니다. AI의 자연어 설명은 보조 자료이고, 같은 명령을
> 누구나 다시 실행할 수 있어야 합니다.

## 6:35–7:10 — 한계와 팀 적용

> 이 데모가 TDD의 생산성 향상을 정량적으로 증명하는 것은 아닙니다.
> AI가 만든 테스트가 자동으로 정답이 되는 것도 아닙니다.
>
> 대신 기존 서비스의 작은 업무 규칙 하나를 골라 재현 테스트를 먼저 만들고,
> focused test와 full suite를 CI 필수 체크로 만드는 시작 방법을 보여줍니다.
>
> 결론적으로 AI는 판단 기준이 아니라 구현 가속기입니다. 무엇이 맞는지는 사람이
> 정하고, 테스트와 리뷰가 그 기준을 반복 가능하게 만듭니다.

## 질문을 받았을 때

### AI와 정확히 무슨 관계인가요?

AI가 API 요청을 처리하는 것이 아니라 개발자처럼 테스트와 제품 코드를 작성한다.
`AGENTS.md`가 작업 순서를 제한하고, 사람과 `pytest`가 결과를 승인한다.

### 왜 실제 AdMarket API를 그대로 복사하지 않았나요?

실제 계약 생성은 DB, 권한, 제안 선택, 알림 등 여러 관심사가 연결된다. 발표에서는
지급조건 규칙의 TDD 흐름을 선명하게 보여주기 위해 순수 정책만 추출했다.

### 이것도 결국 Pydantic validation 아닌가요?

맞다. 중요한 것은 라이브러리가 아니라 “합계 100, 중복 금지, 시간 순서”라는
업무 규칙을 테스트로 먼저 고정했다는 점이다. Pydantic은 그 규칙을 HTTP 경계에서
실행하는 구현 수단이다.

### 테스트도 AI가 만들면 의미가 없지 않나요?

AI가 초안을 낼 수는 있지만 업무 규칙과 기대 status는 사람이 검토하고 승인한다.
테스트 실행 결과와 diff를 함께 확인해야 한다.

### MCP나 별도 AI 프레임워크가 필요한가요?

필수는 아니다. 저장소 작업 규칙, 테스트 명령, CI 게이트만으로 시작할 수 있다.
이 프로젝트도 별도 MCP나 런타임 AI SDK를 사용하지 않는다.

### 더 현업다운 다음 단계는 무엇인가요?

AdMarket의 “최종 파트너는 한 회사만 선정” 같은 상태·권한·동시성 정책을 다음
슬라이스로 선택할 수 있다. 다만 현재 발표에서는 범위를 키우지 않기 위해 제외했다.

## 선택 부록 — mutation testing 20초

> 테스트가 존재한다고 해서 결함을 잘 찾는지는 별개의 질문입니다. mutation
> testing이 `total != 100`을 `total == 100`으로 바꿨을 때 정상·실패 테스트가
> 깨지는지 확인할 수 있습니다. mutmut는 AI 기능이 아니라 TDD 뒤에 붙이는 선택적
> 테스트 품질 감사 도구입니다. native Windows 제약 때문에 라이브에서는 제외했습니다.

자세한 내용은 [docs/OPTIONAL_MUTATION.md](docs/OPTIONAL_MUTATION.md)에 있다.

## 참고 자료

- [Kent Beck, Canon TDD](https://newsletter.kentbeck.com/p/canon-tdd)
- [Kent Beck, Augmented Coding: Beyond the Vibes](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes)
- [Kent Beck BPlusTree3 CLAUDE.md](https://github.com/KentBeck/BPlusTree3/blob/ca80e4d85a99cd0af2effe717f709d43e80403bc/rust/docs/CLAUDE.md)
- [딩코딩코 해설·재현 영상, 2:17부터](https://www.youtube.com/watch?v=AAd8taPTyTM&t=137s)
- [FastAPI 공식 Testing 문서](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pydantic validators 공식 문서](https://docs.pydantic.dev/latest/concepts/validators/)
- [pytest 공식 문서](https://docs.pytest.org/en/stable/)
- [uv 공식 프로젝트 가이드](https://docs.astral.sh/uv/guides/projects/)

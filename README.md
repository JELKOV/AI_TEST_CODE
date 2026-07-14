# TVCF AI-TDD Harness

Frontend와 Backend에 이미 있는 테스트 자산을 배경으로, AI 코딩 에이전트에게
업무 의도와 실행할 테스트를 알려주고 결과를 반복 가능하게 검증하는 FastAPI 발표
프로젝트다.

핵심 문장은 다음과 같다.

> AI가 코드를 빨리 만들수록, 무엇이 맞는지 판단하는 기준이 더 중요해진다.

발표의 구체적인 목표는 다음과 같다.

> AI가 변경한 코드가 기대한 업무 규칙을 지키는지 재현 가능한 테스트 명령과 실제
> HTTP 응답으로 증명한다.

AI는 이 서버의 제품 기능이 아니다. 개발 과정에서 테스트와 구현을 제안하는 작업자이고,
사람이 업무 정답을 승인하며 `pytest`가 결과를 판정한다.

Kent Beck의 Canon TDD에서 테스트 목록 중 하나를 실행 가능한 테스트로 만들고 통과시키는
순서를 가져오고, OpenAI의 Harness Engineering에서 AI가 저장소의 문서·도구·테스트를 직접
사용할 수 있게 한다는 아이디어를 참고했다. 현재 저장소의 Markdown 문서는 역할이 다르다.

- `plan.md` — **무엇을 할지:** 사람이 승인한 테스트 목록에서 이번에 진행할 하나를 선택한다.
- `AGENTS.md` — **어떻게 작업할지:** AI가 지킬 10개 규칙으로 유효한 RED, 최소 구현과
  검증 순서를 고정한다.

두 문서만으로 명령이 자동 실행되지는 않는다. 현재 프로젝트는 `harness.toml`에 문서 경로와
검증 명령을 선언하고 `scripts/tdd_harness.py`를 하나의 실행 진입점으로 사용한다.

## 최소 Repository Harness

| 구성 | 역할 |
| --- | --- |
| `harness.toml` | `AGENTS.md`, `plan.md`와 focused·full·lint·type 명령을 연결한다. |
| `scripts/tdd_harness.py check` | 문서가 존재하고 네 명령과 증거 경로가 유효한지 확인한다. |
| `scripts/tdd_harness.py verify` | focused부터 실행하고 첫 실패에서 중단하며, 통과하면 나머지 게이트를 순서대로 실행한다. |
| `.harness/runs/*.json` | 각 실행의 명령, 종료 코드, 소요 시간과 최종 상태를 자동 기록한다. |

하네스가 자동으로 판단하는 범위는 명령 순서, 종료 코드와 실행 기록이다. 업무 기대값이
맞는지, 실패가 유효한 RED인지, 테스트를 약하게 바꿨는지는 사람이 diff와 결과를 검토한다.

## Frontend와 Backend 테스트 구성

프로젝트별 테스트 수나 품질을 비교하지 않고, 코드 영역이 보호해야 하는 위험을 기준으로
정리한다.

- Frontend: Jest·Vitest로 상태 계산과 데이터 변환을 빠르게 검증하고, Playwright로
  렌더링·오류 UI·핵심 사용자 흐름을 브라우저에서 확인한다.
- Backend: pytest로 업무 규칙을 단위 테스트하고, integration·e2e와 harness로 API,
  DB 연동, 저장소 규칙을 확인한다.
- 공통 기준: 테스트 소유권은 각 영역에 두고 API 계약, 핵심 시나리오와 재현 가능한
  실행 결과를 공유한다.

라이브 실습은 Backend 계약 규칙 세 가지를 축약한 FastAPI 데모로 진행한다.

현재 데모의 실제 작업 순서는 다음과 같다.

~~~text
사람 승인 → plan.md에서 하나 선택 → AGENTS.md 규칙으로 RED·GREEN
→ tdd_harness.py가 검증 명령 실행 → JSON 결과와 diff 확인
~~~

## 장점과 고려사항

현재 업무 코드에서 사용하는 테스트 계층을 평가나 점수 비교가 아닌 운영 관점으로
정리한다.

| 구분 | 의미 |
| --- | --- |
| 빠른 피드백 | Pydantic과 pytest가 잘못된 입력을 DB 작업 전에 발견한다. |
| 계층별 안전망 | unit·integration·e2e·harness가 서로 다른 위험을 보호한다. |
| 실행 가능한 명세 | 지급 합계나 예산 조합 같은 규칙을 반복 실행할 수 있다. |
| 실행 비용 | DB·인증·외부 연동이 필요한 테스트는 준비와 실행 시간이 더 든다. |
| 영향 테스트 탐색 | 테스트가 많아질수록 변경 경로와 가까운 테스트를 먼저 찾을 필요가 있다. |
| Mock과 실제 경계 | 빠른 단위 테스트가 놓칠 수 있는 연동 차이를 integration·e2e로 보완한다. |

## 실습 업무 규칙

| 테스트 | 업무 규칙 | 데모 API |
| --- | --- | --- |
| Payment Terms | 지급 비율은 0 이상이고 합계·시점 조건을 만족해야 한다. | `POST /contracts/payment-terms/validate` |
| Budget Shape | 확정 금액 방식은 제작비와 총예산을 함께 보내며 구간 예산과 섞지 않는다. | `POST /contracts/budget/validate` |
| Submission Material | 첨부 양식에는 실제 파일을 가리키는 `file_id`가 필요하다. | `POST /contracts/submission-material/validate` |

규칙은 실제 AdMarket의 `PaymentTermsCommand`, `BiddingContextCommand`,
`ContractSubmissionMaterialItemCommand`에서 가져왔다. DB, 인증, 저장과 알림은 복사하지
않았으며 위 세 경로는 validator를 설명하기 위한 데모 API다.

## Git Bash 실행

처음 한 번:

~~~bash
cd /c/Users/gram/tvcf/AI_TEST_CODE
uv sync
~~~

하네스 연결 확인:

~~~bash
uv run python scripts/tdd_harness.py check
~~~

선택 테스트부터 전체 검증:

~~~bash
uv run python scripts/tdd_harness.py verify --focused tests/test_contract_budget.py::test_accepts_confirmed_budget_with_production_and_total_amounts
~~~

RED에서는 focused 실패 직후 중단된다. 최소 구현 뒤 같은 명령을 다시 실행하면 focused,
full suite, Ruff, Pyright까지 이어서 확인하고 `.harness/latest-run.json`을 갱신한다.

발표 서버:

~~~bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
~~~

- 발표 및 API 실습: <http://127.0.0.1:8000>
- OpenAPI 문서: <http://127.0.0.1:8000/docs>
- 종료: `Ctrl+C`

발표 페이지는 별도 Node 설치 없이 FastAPI에서 제공한다.

## 실습 테스트

~~~bash
uv run pytest tests/test_contract_payment_terms.py::test_rejects_negative_payment_percentage_even_when_sum_is_100 -vv
uv run pytest tests/test_contract_budget.py::test_accepts_confirmed_budget_with_production_and_total_amounts -vv
uv run pytest tests/test_contract_submission_material.py::test_rejects_attached_material_without_file_id -vv
uv run pytest -vv
~~~

pytest의 `TestClient`는 별도 서버 없이 FastAPI app을 같은 프로세스에서 호출한다.
발표 화면의 세 버튼은 실행 중인 Uvicorn으로 실제 HTTP 요청을 보낸다.

| 시나리오 | 요청 요약 | 기대 |
| --- | --- | --- |
| 지급조건 | 합계는 100이지만 선금 비율이 `-10` | `422` |
| 확정 예산 | 제작비와 총예산을 함께 전달 | `200` |
| 첨부 자료 | `ATTACHED_FORMAT`이지만 `file_id` 누락 | `422` |

## 파일 구성

~~~text
AI_TEST_CODE/
├── app/
│   ├── main.py
│   ├── presentation.html
│   └── tvcfLogo.png
├── docs/
│   └── REPOSITORY_HARNESS.md
├── scripts/
│   └── tdd_harness.py
├── tests/
│   ├── test_contract_budget.py
│   ├── test_contract_payment_terms.py
│   ├── test_contract_submission_material.py
│   ├── test_documentation.py
│   └── test_presentation.py
├── AGENTS.md
├── harness.toml
├── PRESENTATION.md
├── plan.md
├── pyproject.toml
├── uv.lock
└── README.md
~~~

- `AGENTS.md`: AI가 지킬 작업 계약
- `plan.md`: 사람이 승인한 테스트 목록과 발표 범위 원칙
- `harness.toml`: 문서 경로, 검증 명령과 증거 경로를 연결하는 설정
- `scripts/tdd_harness.py`: focused부터 품질 게이트까지 실행하는 단일 진입점
- `app/main.py`: 세 계약 규칙 모델, FastAPI 검증 경로, 발표 자산 경로
- `app/presentation.html`: 목표·장단점·영상·AI와 TDD 작업 흐름·명령과 3 API 실습
- `docs/REPOSITORY_HARNESS.md`: 하네스 구성과 실행 방법
- `PRESENTATION.md`: 40분 화면 순서와 발표 문장

## 참고 자료

- [OpenAI, Harness Engineering](https://openai.com/index/harness-engineering/)
- [GitHub Spec Kit](https://github.github.com/spec-kit/) - 별도 Spec-Driven Development 도구, 현재 데모에는 미사용
- [TDAD: Test-Driven Agentic Development](https://arxiv.org/abs/2603.17973) - 테스트 영향 분석 연구, 현재 데모에는 미사용
- [Playwright Test Agents](https://playwright.dev/docs/test-agents)
- [Kent Beck, Canon TDD](https://newsletter.kentbeck.com/p/canon-tdd)
- [Kent Beck, Sustainable Augmented Development · YOW! 2025](https://www.youtube.com/watch?v=sMujMp4h_EY&t=24s)
- [The Pragmatic Engineer, TDD, AI agents and coding with Kent Beck](https://www.youtube.com/watch?v=aSXaxOdVtAQ&t=3024s)
- [GitHub 공식 영상, Test-driven development with GitHub Copilot](https://www.youtube.com/watch?v=arn6hqERKn4&t=366s)
- [GitHub Blog, TDD with GitHub Copilot](https://github.blog/ai-and-ml/github-copilot/github-for-beginners-test-driven-development-tdd-with-github-copilot/)
- [FastAPI 공식 Testing 문서](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest 공식 문서](https://docs.pytest.org/en/stable/)

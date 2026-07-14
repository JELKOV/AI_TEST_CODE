# AI-TDD FastAPI Demo

실제 AdMarket의 계약 지급조건 테스트를 작게 추출해, AI 코딩 에이전트를
RED → GREEN → REFACTOR 순서로 통제하는 FastAPI 발표 프로젝트다.

AI는 이 서버 안에서 실행되는 기능이 아니다. 개발 과정에서 코드를 제안하는
구현자이고, 사람은 업무 규칙을 승인하며, `pytest`가 결과를 판정한다.

## 발표에서 보여주는 업무 규칙

AdMarket 계약에는 선금(advance), 중도금(interim), 잔금(final)이 있다.

- 세 지급 비율의 합계는 정확히 100이어야 한다.
- 세 단계의 지급 시점은 중복될 수 없다.
- 지급 시점은 계약 체결 → 기획 확정 → 촬영 완료 → 최종 납품 순서를 거스를 수 없다.
- 규칙에 맞는 요청은 `200`, 맞지 않는 요청은 FastAPI/Pydantic의 `422`로 응답한다.

데모 API는 하나다.

~~~text
POST /contracts/payment-terms/validate
~~~

이 경로는 발표용으로 축약한 검증 경로다. 실제 AdMarket의 전체 계약 생성 API를
복사한 것이 아니며 DB, 인증, 저장, 알림을 의도적으로 제외했다.

## 실제 AdMarket와의 연결

원본 저장소 `C:/Users/tvcf_project/admarket_fastapi_BE`에서 다음 부분을 읽기 전용으로
분석했다.

- 원본 테스트:
  `tests/unittests/contract/service_test.py::TestPaymentTermsCommandValidation`
- 원본 규칙:
  `app/contract/application/command.py::PaymentTermsCommand.validate_payment_split`
- 현재 데모 테스트: `tests/test_contract_payment_terms.py`
- 현재 데모 규칙: `app/main.py::ContractPaymentTerms`

원본에서 가져온 것은 코드 전체가 아니라 업무 불변조건과 테스트 사례다.

## Git Bash 실행

처음 한 번:

~~~bash
cd /c/Users/tvcf_project/AI_TDD_FastAPI_Demo
uv sync
~~~

전체 검증:

~~~bash
uv run pytest
uv run ruff check .
uvx pyright
~~~

발표 서버:

~~~bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
~~~

브라우저:

- 발표 및 실제 API 실습: <http://127.0.0.1:8000>
- OpenAPI 문서: <http://127.0.0.1:8000/docs>

종료:

~~~text
Ctrl+C
~~~

이 프로젝트는 Python 전용이므로 `npm`, `npm test`, `frontend` 디렉터리를 사용하지 않는다.

## 테스트를 하나씩 실행

~~~bash
uv run pytest tests/test_contract_payment_terms.py::test_accepts_valid_contract_payment_terms -vv
uv run pytest tests/test_contract_payment_terms.py::test_rejects_payment_percentage_sum_not_100 -vv
uv run pytest tests/test_contract_payment_terms.py::test_rejects_duplicate_payment_timings -vv
uv run pytest tests/test_contract_payment_terms.py::test_rejects_reversed_payment_timing_order -vv
uv run pytest tests/test_presentation.py -vv
uv run pytest
~~~

## 파일 구성

~~~text
AI_TDD_FastAPI_Demo/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── presentation.html
├── docs/
│   ├── AI_PROMPTS.md
│   ├── OPTIONAL_MUTATION.md
│   ├── TDD_CYCLES.md
│   └── VIDEO_ALIGNMENT.md
├── tests/
│   ├── test_contract_payment_terms.py
│   └── test_presentation.py
├── AGENTS.md
├── PRESENTATION.md
├── plan.md
├── pyproject.toml
├── uv.lock
└── README.md
~~~

- `AGENTS.md`: AI가 지킬 작업 계약
- `plan.md`: 사람이 승인한 테스트 목록
- `app/main.py`: 지급조건 모델, 업무 규칙, FastAPI 경로
- `app/presentation.html`: 설명과 실제 API 실행 화면
- `tests/test_contract_payment_terms.py`: 정상·실패·경계 계약
- `docs/TDD_CYCLES.md`: 실제 RED와 GREEN 증거
- `PRESENTATION.md`: 화면 순서에 맞춘 발표 대본

## 발표 흐름

1. AI, Human, pytest의 역할을 구분한다.
2. 실제 AdMarket 테스트에서 어떤 규칙을 추출했는지 보여준다.
3. 합계 오류 테스트가 `200 → 422`를 만들었던 RED/GREEN을 설명한다.
4. 화면에서 정상 지급조건 `200`을 실행한다.
5. 합계 오류와 순서 오류가 각각 `422`인지 실행한다.
6. Git Bash에서 focused test와 full suite를 실행한다.
7. AI의 설명이 아니라 테스트 결과와 사람의 검토가 완료 기준이라고 결론 낸다.

## 참고 자료

- [Kent Beck, Canon TDD](https://newsletter.kentbeck.com/p/canon-tdd)
- [Kent Beck, Augmented Coding: Beyond the Vibes](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes)
- [Kent Beck BPlusTree3 CLAUDE.md](https://github.com/KentBeck/BPlusTree3/blob/ca80e4d85a99cd0af2effe717f709d43e80403bc/rust/docs/CLAUDE.md)
- [딩코딩코 해설·재현 영상, 2:17부터](https://www.youtube.com/watch?v=AAd8taPTyTM&t=137s)
- [FastAPI 공식 Testing 문서](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest 공식 문서](https://docs.pytest.org/en/stable/)
- [uv 공식 프로젝트 가이드](https://docs.astral.sh/uv/guides/projects/)

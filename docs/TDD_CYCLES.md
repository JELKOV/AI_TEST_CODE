# AI-TDD 실제 사이클 기록

실제 AdMarket의 계약 지급조건 테스트를 발표용 FastAPI에 옮기며 확인한 RED와
GREEN 증거다. 명령은 프로젝트 루트의 Git Bash에서 실행한다.

환경·문법·import 실패는 RED로 인정하지 않았다. 아래 RED는 모두 구현되지 않은
HTTP 행동 때문에 기대 status와 실제 status가 달랐던 실패다.

## Cycle 1 — 정상 계약 지급조건

- Test first: `test_accepts_valid_contract_payment_terms`
- 계약: 30/30/40 비율과 정상 순서의 지급 시점은 `200`과 입력 계약을 반환한다.
- RED: 기대 `200`, 실제 `404`
- GREEN: 지급 시점 enum, 입력 모델, 검증 API 경로만 추가
- 결과: focused `1 passed`, full suite `11 passed`

~~~bash
uv run pytest tests/test_contract_payment_terms.py::test_accepts_valid_contract_payment_terms -vv
uv run pytest
~~~

## Cycle 2 — 지급 비율 합계

- Test first: `test_rejects_payment_percentage_sum_not_100`
- 계약: 선금·중도금·잔금 비율의 합계가 100이 아니면 `422`
- RED: 기대 `422`, 실제 `200`
- GREEN: 세 비율을 더해 100인지 확인하는 validator만 추가
- 결과: focused `1 passed`, full suite `12 passed`

~~~bash
uv run pytest tests/test_contract_payment_terms.py::test_rejects_payment_percentage_sum_not_100 -vv
uv run pytest
~~~

## Cycle 3 — 지급 시점 중복

- Test first: `test_rejects_duplicate_payment_timings`
- 계약: 같은 지급 시점을 두 단계에 중복 지정하면 `422`
- RED: 기대 `422`, 실제 `200`
- GREEN: 세 지급 시점의 유일성 검사만 추가
- 결과: focused `1 passed`, full suite `13 passed`

~~~bash
uv run pytest tests/test_contract_payment_terms.py::test_rejects_duplicate_payment_timings -vv
uv run pytest
~~~

## Cycle 4 — 지급 시점 순서

- Test first: `test_rejects_reversed_payment_timing_order`
- 계약: 선금 지급 시점이 중도금보다 늦으면 `422`
- RED: 기대 `422`, 실제 `200`
- GREEN: 계약 체결부터 최종 납품까지의 순서 비교만 추가
- 결과: focused `1 passed`, full suite `14 passed`

~~~bash
uv run pytest tests/test_contract_payment_terms.py::test_rejects_reversed_payment_timing_order -vv
uv run pytest
~~~

## Cycle 5 — 실제 API 발표 화면

- Test first: `test_presentation_runs_admarket_contract_payment_scenarios`
- 계약: 화면에서 정상·합계 오류·순서 오류와 실제 API 경로를 확인
- RED: 기존 화면에 AdMarket 계약 문구와 API 경로가 없음
- GREEN: 예약 시나리오를 단일 요청 기반 지급조건 시나리오 3개로 교체
- 결과: focused `1 passed`, full suite `15 passed`

~~~bash
uv run pytest tests/test_presentation.py::test_presentation_runs_admarket_contract_payment_scenarios -vv
uv run pytest
~~~

## Cycle 6 — 제품 표면 교체

- Test first: `test_openapi_exposes_only_contract_demo_product_route`
- 계약: OpenAPI에는 지급조건 경로만 있고 이전 예약 경로는 없음
- RED: `/reservations`가 OpenAPI paths에 남음
- GREEN: 예약 모델·라우트·테스트를 제거하고 API 제목을 계약 데모로 변경
- 결과: focused `1 passed`, 교체 후 full suite `9 passed`

~~~bash
uv run pytest tests/test_contract_payment_terms.py::test_openapi_exposes_only_contract_demo_product_route -vv
uv run pytest
~~~

## 현재 재현 명령

~~~bash
uv run pytest tests/test_contract_payment_terms.py -vv
uv run pytest
uv run ruff check .
uvx pyright
~~~

과거 사이클의 full suite 개수가 현재보다 큰 이유는 제거 대상이던 예약 테스트가
당시 함께 실행되었기 때문이다. 최종 제품 표면 교체 후 현재 suite는 9개다.

## REFACTOR 증거

모든 테스트가 GREEN인 상태에서 세 validator를 원본 `PaymentTermsCommand`와 같은
하나의 정책 검증 흐름으로 합쳤다. 새 동작이나 테스트 변경은 없었고 중복된
`timings` 계산과 decorator만 제거했다.

~~~bash
uv run pytest tests/test_contract_payment_terms.py -vv
uv run pytest
uv run ruff check .
uvx pyright
~~~

결과는 focused `5 passed`, full suite `9 passed`, Ruff `All checks passed`,
Pyright `0 errors, 0 warnings`다.

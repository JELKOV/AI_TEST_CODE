# 최소 Repository Harness

이 하네스는 AI가 정답을 판단하는 시스템이 아니다. 사람이 승인한 테스트 하나를 기준으로
검증 명령을 같은 순서로 실행하고, 결과를 다시 확인할 수 있는 JSON으로 남기는 저장소
작업 장치다.

## 전체 흐름

~~~text
사람이 기대 결과 승인
  → plan.md에서 테스트 하나 선택
  → AGENTS.md 규칙에 따라 테스트 작성
  → tdd_harness.py verify 실행
  → focused 실패 시 중단하고 RED 원인을 사람이 확인
  → 최소 구현 후 같은 명령 재실행
  → focused → full → lint → type 통과
  → .harness/latest-run.json 확인
  → docs/TDD_CYCLES.md에 판단과 변경 내용을 요약
~~~

## 파일별 역할

| 파일 | 역할 | 자동 실행 여부 |
| --- | --- | --- |
| `AGENTS.md` | AI가 따라야 할 TDD 작업 순서와 금지사항을 정의한다. | Codex 작업 지침이지만 품질 명령을 직접 실행하지는 않는다. |
| `plan.md` | 사람이 승인한 테스트 목록과 현재 진행할 항목을 관리한다. | 사람이 기대 결과를 승인하고 AI가 완료 상태를 갱신한다. |
| `harness.toml` | 세 문서 경로, 네 품질 게이트와 증거 저장 위치를 선언한다. | `tdd_harness.py`가 읽는다. |
| `scripts/tdd_harness.py` | 구성을 검사하고 품질 게이트를 순서대로 실행한다. | 직접 실행하는 하네스 진입점이다. |
| `pyproject.toml` | pytest 수집 경로, Ruff와 Pyright의 프로젝트 설정을 제공한다. | 각 도구가 실행될 때 읽는다. |
| `tests/` | 제품 동작과 발표 화면의 기대 결과를 실행 가능한 테스트로 표현한다. | pytest가 수집하고 실행한다. |
| `.harness/runs/*.json` | 각 실행의 명령, 종료 코드, 소요 시간과 최종 상태를 저장한다. | `verify` 실행마다 자동 생성하며 Git에는 커밋하지 않는다. |
| `.harness/latest-run.json` | 가장 최근 실행 결과를 고정된 경로로 제공한다. | `verify`가 매번 갱신한다. |
| `docs/TDD_CYCLES.md` | RED 원인, 최소 GREEN 변경과 REFACTOR 여부를 사람이 읽을 수 있게 요약한다. | JSON과 diff를 검토한 뒤 AI가 작성하고 사람이 확인한다. |

## 설정 파일

`harness.toml`은 다음 연결만 담당한다.

~~~toml
[documents]
agreement = "AGENTS.md"
plan = "plan.md"
cycle_log = "docs/TDD_CYCLES.md"

[commands]
focused = ["uv", "run", "pytest", "{focused}", "-vv"]
full = ["uv", "run", "pytest", "-vv"]
lint = ["uv", "run", "ruff", "check", "."]
type = ["uvx", "pyright"]
~~~

Markdown 내용을 파싱해 업무 규칙을 추측하지 않는다. 문서가 존재하는지 확인하고, 실행할
명령과 순서만 기계적으로 연결한다.

## 실행 명령

처음 한 번 의존성을 설치한다.

~~~bash
uv sync
~~~

문서, 명령과 증거 경로가 올바르게 연결됐는지 확인한다.

~~~bash
uv run python scripts/tdd_harness.py check
~~~

현재 변경과 가장 가까운 pytest node ID를 지정해 검증한다.

~~~bash
uv run python scripts/tdd_harness.py verify --focused tests/test_contract_budget.py::test_accepts_confirmed_budget_with_production_and_total_amounts
~~~

## 중단 조건

`verify`는 다음 순서를 고정한다.

1. `focused`: 선택한 테스트 하나
2. `full`: 전체 pytest
3. `lint`: Ruff
4. `type`: Pyright

어느 단계든 종료 코드가 0이 아니면 즉시 중단한다. 실패 이후 단계는 실행하지 않으며,
실패한 단계까지의 결과도 JSON으로 남긴다. focused가 RED인 상황에서는 JSON만 보고 기능
실패라고 단정하지 않고, 사람이 import·문법·환경 문제가 아닌 기대한 동작 실패인지 확인한다.

## 증거 구분

- 기계 증거: 실행한 명령, 종료 코드, 소요 시간, 통과 여부
- 사람의 판단: 업무 기대값, RED가 유효한 이유, 테스트를 약화하지 않았는지, diff의 적절성
- 사이클 기록: 기계 증거와 사람의 판단을 합친 `docs/TDD_CYCLES.md` 요약

이 경계 때문에 하네스는 테스트 통과를 반복 가능하게 만들지만, 업무 정답 승인이나 코드
리뷰를 대신하지 않는다.

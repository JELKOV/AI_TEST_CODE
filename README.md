# AI-TDD FastAPI Demo

AI 코딩 에이전트가 구현을 제안하되, 사람이 승인한 테스트와 `pytest` 결과가 작업 범위를 통제하는 가벼운 FastAPI 발표 프로젝트입니다.

이 프로젝트는 별도의 AI API를 호출하지 않습니다. AI는 런타임 기능이 아니라 개발 과정의 구현자 역할이며, [AGENTS.md](AGENTS.md)가 AI의 작업 규칙, 테스트가 실행 가능한 요구사항, `pytest`가 통과 여부를 판정하는 자동화된 게이트입니다.

## 발표 주제

> AI가 구현 속도를 높이고, 테스트가 행동을 통제한다.

예약 API를 한 번에 완성하지 않고 다음 흐름을 반복합니다.

1. 사람이 다음 요구사항을 테스트 하나로 승인합니다.
2. 테스트를 실행해 의도한 동작 때문에 실패하는지 확인합니다. 이것이 RED입니다.
3. AI는 테스트를 수정하지 않고 통과에 필요한 최소 코드만 작성합니다. 이것이 GREEN입니다.
4. 전체 테스트가 통과한 상태에서만 구조를 정리합니다. 이것이 REFACTOR입니다.

## Git Bash 실행

처음 한 번만 의존성을 설치합니다.

```bash
cd /c/Users/tvcf_project/AI_TDD_FastAPI_Demo
uv sync
```

테스트와 정적 검사를 실행합니다.

```bash
uv run pytest
uv run ruff check .
```

발표 서버를 실행합니다.

```bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

브라우저에서 다음 주소를 엽니다.

- 발표 및 API 실습 화면: <http://127.0.0.1:8000>
- FastAPI 자동 API 문서: <http://127.0.0.1:8000/docs>

서버 종료는 서버를 실행한 Git Bash 창에서 `Ctrl+C`입니다.

## 기능

- `POST /reservations`: 예약 생성
- 같은 방의 시간이 겹치면 `409 Conflict`
- 종료가 시작보다 늦지 않거나 방 ID가 비어 있으면 `422 Unprocessable Content`
- 종료 시각과 다음 시작 시각이 정확히 같으면 예약 허용
- 시간이 같아도 방이 다르면 예약 허용
- `GET /reservations`: 현재 프로세스에 저장된 예약 조회

데이터는 발표를 단순하게 유지하기 위해 메모리에 저장됩니다. 서버를 재시작하면 초기화되며 DB, 로그인, 외부 API는 사용하지 않습니다.

## 파일 구성

```text
AI_TDD_FastAPI_Demo/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── presentation.html
├── docs/
│   ├── AI_PROMPTS.md
│   └── TDD_CYCLES.md
├── tests/
│   ├── test_presentation.py
│   └── test_reservations.py
├── AGENTS.md
├── PRESENTATION.md
├── pyproject.toml
├── uv.lock
└── README.md
```

- `app/main.py`: 입력 모델, 예약 충돌 정책, FastAPI 라우트를 한 파일에 둔 실습 코드
- `app/presentation.html`: 같은 FastAPI 서버에서 제공하는 발표 및 실제 API 호출 화면
- `tests/`: 사람이 승인한 동작 계약
- `AGENTS.md`: AI가 지켜야 할 RED-GREEN-REFACTOR 작업 규칙
- `PRESENTATION.md`: 화면과 Git Bash를 따라 진행하는 7분 발표 대본
- `docs/TDD_CYCLES.md`: 실제로 확인한 실패와 최소 구현 기록
- `docs/AI_PROMPTS.md`: 발표에서 복사해 사용할 단계별 AI 프롬프트

## 7분 발표 순서

1. 화면 상단에서 AI, 사람, `pytest`의 역할을 구분합니다.
2. RED-GREEN-REFACTOR 카드로 테스트 우선 개발 흐름을 설명합니다.
3. 정상 예약을 실행해 `201`을 확인합니다.
4. 겹치는 예약을 실행해 첫 요청 `201`, 두 번째 요청 `409`를 확인합니다.
5. 경계 인접 예약을 실행해 두 요청 모두 `201`임을 확인합니다.
6. Git Bash에서 `uv run pytest`를 실행해 전체 계약이 통과함을 보여줍니다.
7. 마지막에 AI의 답변이 아니라 재현 가능한 테스트가 품질 판단 기준이라는 결론을 말합니다.

## 참고 자료

- [Kent Beck, Canon TDD](https://newsletter.kentbeck.com/p/canon-tdd)
- [FastAPI 공식 Testing 문서](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest 공식 문서](https://docs.pytest.org/en/stable/)
- [uv 공식 프로젝트 가이드](https://docs.astral.sh/uv/guides/projects/)

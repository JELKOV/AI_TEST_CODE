# AI-assisted TDD 발표 스크립트

## 발표 전 실행

Git Bash에서 다음 명령을 실행한다.

```bash
cd /c/Users/tvcf_project/AI_TDD_FastAPI_Demo
uv sync
uv run pytest
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

브라우저에서 <http://127.0.0.1:8000>을 연다.

## 0:00–0:50 — 문제 제기

> 오늘 발표할 주제는 AI가 코드를 대신 작성하는 방법이 아니라, AI가 작성하는 코드의 범위를 어떻게 통제할 것인가입니다.
>
> AI는 구현 후보를 매우 빠르게 만들지만, 요구사항을 스스로 결정하게 두면 필요 이상의 기능을 넣거나 기존 동작을 바꿀 수 있습니다. 그래서 사람의 의도를 실행 가능한 테스트로 먼저 고정한 뒤 AI에게 최소 구현만 맡겼습니다.
>
> 한 문장으로 정리하면, AI가 구현 속도를 높이고 테스트가 행동을 통제합니다.

여기서 `AI-assisted TDD`는 Kent Beck이 별도로 정의한 공식 방법론 이름이 아니다. 이 프로젝트가 [Canon TDD](https://newsletter.kentbeck.com/p/canon-tdd)의 흐름을 AI 코딩 에이전트 작업 규칙에 적용한 방식이다.

딩코딩코의 [해설·재현 영상 2:17 구간](https://www.youtube.com/watch?v=AAd8taPTyTM&t=137s)은 Claude 명령으로 `plan.md`의 다음 테스트를 RED, GREEN, REFACTOR, 검증 순서로 처리한다. 영상은 Kent Beck 본인의 발표가 아니며, 이 프로젝트는 영상의 Claude 명령을 복제한 것이 아니라 같은 핵심 규칙을 도구 중립적인 `AGENTS.md`, `plan.md`, Python `pytest`로 옮긴 예제다.

## 0:50–1:40 — 세 역할

화면의 세 역할을 왼쪽부터 설명한다.

> 첫 번째는 AI Agent입니다. 사람이 승인한 plan.md에서 지금 선택된 행동 하나에 필요한 구현을 제안합니다.
>
> 두 번째는 Human입니다. 어떤 예약 정책이 맞는지 결정하고 테스트를 승인합니다. 영상보다 한 단계 더 명시적인 이 승인 절차는 이 프로젝트가 추가한 거버넌스입니다.
>
> 세 번째는 pytest입니다. AI가 “완료했다”고 말하는지는 중요하지 않습니다. 실제 프로세스가 기대한 응답을 내는지를 pytest가 같은 조건으로 반복 판정합니다.

통제 구조는 다음과 같다.

```text
사람이 승인한 요구사항
        ↓
plan.md의 다음 테스트 하나
        ↓
실패하는 테스트 한 개
        ↓
AI의 최소 구현
        ↓
focused pytest → full pytest
        ↓
사람의 변경 검토
```

- `AGENTS.md`: AI가 따라야 할 작업 규칙
- `plan.md`: 승인된 테스트 목록과 현재 진행 상태
- `tests/`: 요구사항을 실행 가능한 계약으로 고정
- `pytest` 종료 코드: 자동화된 완료 판정

## 1:40–3:10 — RED, GREEN, REFACTOR

화면 왼쪽의 세 카드를 가리킨다.

`VIDEO 2:17` 카드를 누르면 영상에서 전체 사이클, 개별 RED/GREEN/REFACTOR, 구조 변경 전용 tidy, 테스트 검증과 커밋 규칙을 설명하는 지점이 열린다.

> RED에서는 테스트를 먼저 작성합니다. 예를 들어 같은 방의 예약 시간이 겹치면 두 번째 요청은 409여야 한다고 정했습니다. 정책이 없던 시점에는 실제 201이 반환되어 테스트가 실패했습니다.
>
> 여기서 서버가 안 켜지거나 import가 깨진 것은 유효한 RED가 아닙니다. 반드시 구현되지 않은 행동 때문에 assertion이 실패해야 합니다.
>
> GREEN에서는 테스트를 지우거나 기대값을 바꾸지 않습니다. 두 시간 구간이 실제로 교차할 때만 409를 반환하는 최소 조건을 넣었습니다.
>
> 전체 테스트가 통과한 뒤에만 REFACTOR를 합니다. 이 단계에서는 이름과 중복을 정리할 수 있지만 새 동작은 추가하지 않습니다.

이 프로젝트에서는 영상과 Kent Beck의 Tidy First 원칙에 맞춰 행동 변경과 구조 변경을 같은 단계나 커밋에 섞지 않는다.

실제 사이클을 Git Bash에서 확인하려면 다음 명령을 사용한다.

```bash
uv run pytest tests/test_reservations.py::test_rejects_overlapping_reservation_for_same_room -vv
uv run pytest
```

발표에서 강조할 점은 테스트를 많이 만드는 것이 아니라, 테스트 목록에서 정확히 하나를 실행 가능한 테스트로 바꾸고 짧은 피드백 루프를 반복한다는 것이다.

## 3:10–5:10 — 라이브 API 실습

### Create (정상 예약)

`Create` 버튼을 누른다.

> 먼저 정상 예약입니다. 화면이 실제 `POST /reservations`를 호출하고 `201 Created`를 받았습니다. 미리 적어 둔 정적 결과가 아니라 지금 실행 중인 FastAPI 응답입니다.

### Conflict (겹침 거절)

`Conflict` 버튼을 누른다.

> 첫 요청은 기준 예약이라 201입니다. 두 번째 요청은 같은 방에서 시간이 겹치므로 409입니다. 아래 Request와 Response에서 입력 시간과 `reservation_conflict` 결과를 함께 볼 수 있습니다.

### Boundary (경계 인접 허용)

`Boundary` 버튼을 누른다.

> 단순히 시간이 같다는 이유로 모두 막으면 정상 사용까지 거절합니다. 첫 예약이 11시에 끝나고 다음 예약이 정확히 11시에 시작하면 두 요청 모두 201입니다. 이 경계 사례도 별도 테스트로 고정했습니다.

시간이 겹쳐도 방이 다르면 허용한다는 계약도 테스트에 포함되어 있다. 각 화면 실행은 고유한 `room_id`를 사용하므로 이전 클릭의 인메모리 데이터와 충돌하지 않는다.

## 5:10–6:00 — 코드 구조

> 프로젝트는 의도적으로 작게 만들었습니다. `app/main.py` 한 파일에 입력 모델, 충돌 정책, API 라우트가 있고 `presentation.html`이 같은 FastAPI 프로세스에서 제공됩니다.
>
> 데이터베이스, 로그인, 메시지 큐, React, npm, 런타임 LLM 호출은 없습니다. 발표의 대상은 예약 시스템 아키텍처가 아니라 AI와 짧은 TDD 피드백 루프의 관계이기 때문입니다.

API 동작은 다음과 같다.

- `POST /reservations`: 예약 생성
- `GET /reservations`: 현재 프로세스의 예약 조회
- 같은 방의 시간 교차: `409 Conflict`
- 잘못된 시간 또는 빈 방 ID: `422`
- 서버 재시작: 인메모리 데이터 초기화

FastAPI 자동 문서는 화면의 `OpenAPI Docs` 버튼으로 연다.

## 6:00–6:40 — 최종 증거

별도의 Git Bash 창에서 실행한다.

```bash
uv run pytest
uv run ruff check .
```

> 현재 전체 테스트 10개가 통과하고 정적 검사도 통과합니다. 이 출력이 현재 작업의 완료 증거입니다. AI의 설명은 보조 자료이고, 재현 가능한 명령 결과가 품질 게이트입니다.

## 6:40–7:20 — 결론과 확장

> AI를 붙였다고 자동으로 TDD가 되는 것은 아닙니다. 사람은 다음 행동을 테스트로 선택하고, AI는 그 테스트를 통과시키는 작은 변경을 만들며, 도구가 전체 회귀를 판정해야 합니다.
>
> 이 구조는 지금은 로컬 작업 규칙이지만 팀에서는 같은 `uv run pytest`와 `uv run ruff check .`를 CI의 필수 체크로 올릴 수 있습니다. 그러면 AI가 만든 변경도 테스트를 통과하지 않으면 병합되지 않습니다.
>
> 결론적으로 AI는 판단 기준이 아니라 구현 가속기이고, 테스트와 리뷰가 통제 장치입니다.

영상의 전체 사이클 자동화는 AI가 요구사항을 정한다는 뜻이 아니다. 사람이 승인한 계획의 다음 항목을 순서대로 실행한다는 뜻이며, 올바른 설계인지 판단하는 책임은 계속 사람에게 있다.

이 프로젝트가 증명하지 않는 것도 분명히 말한다.

- TDD가 항상 생산성을 높인다는 정량 실험은 아니다.
- AI가 테스트 자체의 정답을 보장하지 않는다.
- 테스트에 없는 요구사항까지 자동으로 검증하지 않는다.
- 실제 운영용 동시성, 영속성, 인증 설계를 포함하지 않는다.

## 질문을 받았을 때

### AI와 정확히 무슨 관계인가요?

AI가 FastAPI 안에서 실행되는 것이 아니라 개발자 역할로 코드를 변경한다. `AGENTS.md`가 작업 절차를 제한하고, 사람이 승인한 테스트와 pytest가 결과를 검증한다.

### 테스트도 AI가 만들면 의미가 없지 않나요?

AI가 초안을 제안할 수는 있지만 정책과 기대 결과는 사람이 검토하고 승인해야 한다. 같은 에이전트의 말만 믿지 않고 실행 결과와 diff를 함께 확인하는 이유다.

### 기존 코드에 어떻게 적용하나요?

작은 버그나 정책 하나를 선택해 재현 테스트를 먼저 만들고, focused 테스트와 전체 suite를 필수 명령으로 둔다. 처음부터 모든 코드를 다시 작성할 필요는 없다.

### MCP나 별도 AI 프레임워크가 필요한가요?

필수는 아니다. 저장소 규칙, 테스트 명령, CI 게이트만으로 시작할 수 있다. 이 프로젝트도 별도 MCP나 런타임 AI SDK 없이 그 최소 구조를 보여준다.

## 선택 부록 — mutation testing 30초

> 테스트가 있다고 해서 그 테스트가 반드시 결함을 잘 찾는 것은 아닙니다. mutation testing은 `<`를 `<=`처럼 조금 바꾸고 테스트가 실패하는지 확인합니다. 현재 프로젝트에서는 이 변경이 인접 예약을 잘못 막으며 경계 테스트가 이를 발견합니다. mutmut는 AI 기능이 아니라 TDD 뒤에서 테스트 품질을 감사하는 선택 도구입니다. 다만 native Windows를 지원하지 않아 이번 라이브 실행에서는 제외했습니다.

자세한 설명은 `docs/OPTIONAL_MUTATION.md`를 사용한다.

## 참고 자료

- [Kent Beck, Canon TDD](https://newsletter.kentbeck.com/p/canon-tdd)
- [Kent Beck, Augmented Coding: Beyond the Vibes](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes)
- [Kent Beck BPlusTree3 CLAUDE.md](https://github.com/KentBeck/BPlusTree3/blob/ca80e4d85a99cd0af2effe717f709d43e80403bc/rust/docs/CLAUDE.md)
- [딩코딩코 해설·재현 영상, 2:17부터](https://www.youtube.com/watch?v=AAd8taPTyTM&t=137s)
- [FastAPI 공식 Testing 문서](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest 공식 문서](https://docs.pytest.org/en/stable/)
- [uv 공식 프로젝트 가이드](https://docs.astral.sh/uv/guides/projects/)

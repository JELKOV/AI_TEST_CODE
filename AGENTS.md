# AI-TDD Working Agreement

1. Keep the test list in `plan.md`, then select and implement exactly one concrete test.
2. Confirm that the new test fails for the expected behavioral reason. Import, syntax, and environment failures are not valid RED evidence.
3. Change production code only while a relevant test is failing.
4. During GREEN, never delete, skip, weaken, or rewrite the failing test.
5. Write only enough production code to make the current test pass.
6. Run the focused test first and the full suite immediately afterward.
7. Refactor only while every test is green, add no new behavior, and run the full suite afterward.
8. Keep behavioral changes separate from structural changes and never mix them in one step or commit.
9. Mark a `plan.md` item complete only after the focused test and full suite pass.
10. Commit only when tests, lint, and type checks are green and the change is one logical unit.

## 한글 설명

### 1번 규칙 — 테스트 목록에서 한 가지만 선택한다

먼저 `plan.md`에 구현할 테스트 목록을 적는다. 그중 지금 구현할 구체적인 테스트는
반드시 하나만 선택한다. 여러 기능을 한 번에 만들지 않고, 선택한 테스트 하나만
완료하는 데 집중한다.

### 2번 규칙 — 기능이 없어서 실패한 RED인지 확인한다

새 테스트를 먼저 실행해 기대한 동작이 아직 구현되지 않아 실패하는지 확인한다.
`ImportError`, 문법 오류, 의존성 미설치처럼 테스트 내용과 관계없는 실패는 RED가
아니다. 그런 문제는 먼저 원인을 분리해 해결한다.

### 3번 규칙 — 관련 테스트가 실패할 때만 제품 코드를 바꾼다

현재 구현하려는 동작과 연결된 테스트가 RED일 때만 서버·앱 같은 제품 코드를 수정한다.
테스트가 이미 통과하는데 기능 코드를 먼저 바꾸지 않는다.

### 4번 규칙 — GREEN 중에는 실패했던 테스트를 약하게 만들지 않는다

테스트를 통과시키려고 실패한 테스트를 삭제하거나, `skip`으로 건너뛰거나, 기대값을
낮추거나, 내용을 다시 쓰면 안 된다. 같은 테스트를 유지한 채 제품 코드로 통과시킨다.

### 5번 규칙 — 현재 테스트를 통과시키는 최소 코드만 작성한다

다음 기능까지 미리 만들거나 필요 이상으로 복잡한 구조를 추가하지 않는다. 지금
실패한 테스트를 통과시키는 데 필요한 만큼만 제품 코드를 작성한다.

### 6번 규칙 — 가까운 테스트 후 전체 테스트를 바로 실행한다

먼저 방금 작업한 테스트 하나를 실행해 빠르게 확인한다. 통과하면 곧바로 전체 테스트
모음을 실행해 다른 기능이 깨지지 않았는지 확인한다.

### 7번 규칙 — 리팩터링은 모든 테스트가 GREEN일 때만 한다

리팩터링은 중복 제거·이름 개선처럼 구조만 정리하는 작업이다. 모든 테스트가 통과한
상태에서만 하며, 새 동작을 넣지 않는다. 정리한 뒤에는 전체 테스트를 다시 실행한다.

### 8번 규칙 — 기능 변경과 구조 변경을 섞지 않는다

새 동작을 만드는 변경과 코드 구조를 정리하는 변경은 같은 작업 단계나 커밋에 섞지
않는다. 그래야 어떤 변경이 동작에 영향을 줬는지 쉽게 검토하고 되돌릴 수 있다.

### 9번 규칙 — focused와 전체 테스트가 통과한 뒤에만 계획을 완료한다

`plan.md`의 항목을 완료 표시하기 전에, 관련 테스트 하나와 전체 테스트 모음이 모두
통과해야 한다. 둘 중 하나라도 실패하면 항목은 아직 완료가 아니다.

### 10번 규칙 — 모든 검증이 통과한 하나의 논리 단위만 커밋한다

테스트, lint(코드 형식·기본 오류 검사), type check(타입 검사)가 모두 통과한 뒤에만
커밋한다. 하나의 커밋에는 하나의 목적이 분명한 변경만 담는다.

## 최소 Repository Harness

- `harness.toml`은 이 작업 규칙, 테스트 계획의 경로와 focused·full·lint·type
  명령을 선언한다.
- `uv run python scripts/tdd_harness.py check`로 문서와 명령 연결을 확인한다.
- 테스트 하나를 선택한 뒤 `uv run python scripts/tdd_harness.py verify --focused <pytest-node-id>`를
  실행한다. focused가 실패하면 즉시 중단하고, 통과하면 full·lint·type을 순서대로 실행한다.
- 모든 실행은 `.harness/runs/`에 JSON으로 남고 마지막 실행은
  `.harness/latest-run.json`에서도 확인한다.
- JSON은 명령·종료 코드·소요 시간의 기계 증거다. 사람이 업무 기대값, RED 실패 이유와
  실제 diff를 함께 확인한다.

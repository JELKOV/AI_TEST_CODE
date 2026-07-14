# AI-TDD 실제 사이클 기록

이 문서는 발표용 예약 API를 테스트 하나씩 확장하며 확인한 RED와 GREEN만 기록한다.
명령은 프로젝트 루트의 Git Bash에서 실행하며 모두 `uv run`을 사용한다.

`ModuleNotFoundError`처럼 애플리케이션 동작에 도달하지 못한 환경·임포트 실패는 RED가 아니다.
환경을 복구한 뒤, 새 테스트가 기대한 동작 차이로 실패한 실행만 유효한 RED로 사용했다.

## Cycle 1 — 예약 생성

- Test first: `test_create_reservation`
- 계약: `POST /reservations`가 생성된 예약과 `201`을 반환한다.
- 유효한 RED: 기대 `201`, 실제 `404`
- Minimal GREEN: `POST /reservations`와 응답 모델만 추가해 `id`와 예약을 반환했다.

```bash
uv run pytest tests/test_reservations.py::test_create_reservation
uv run pytest
```

Focused GREEN은 `1 passed`로 확인했다.

## Cycle 2 — 종료 시간 검증

- Test first: `test_rejects_end_time_not_after_start_time`
- 계약: `ends_at <= starts_at`이면 `422`와 `end_must_be_after_start`를 반환한다.
- 유효한 RED: 기대 `422`, 실제 `201`
- Minimal GREEN: 시간 비교 한 번과 `HTTPException`만 추가했다.
- GREEN 후 refactor: 동작을 바꾸지 않고 deprecated
  `status.HTTP_422_UNPROCESSABLE_ENTITY`를
  `status.HTTP_422_UNPROCESSABLE_CONTENT`로 교체했다.

```bash
uv run pytest tests/test_reservations.py::test_rejects_end_time_not_after_start_time
uv run pytest
```

Focused GREEN과 refactor 후 재실행은 각각 `1 passed`로 확인했다.

## Cycle 3 — 같은 방의 시간 충돌

- Test first: `test_rejects_overlapping_reservation_for_same_room`
- 계약: 같은 `room_id`의 시간이 겹치면 `409`와 `reservation_conflict`를 반환한다.
- 유효한 RED: 기대 `409`, 실제 `201`
- Minimal GREEN: 기존 예약을 순회하며 같은 방이고 두 구간이 겹치는 경우만 거절했다.

```bash
uv run pytest tests/test_reservations.py::test_rejects_overlapping_reservation_for_same_room
uv run pytest
```

Focused GREEN은 `1 passed`로 확인했다.

## Cycle 4 — 빈 room_id 거절

- Test first: `test_rejects_empty_room_id`
- 계약: 빈 `room_id`는 `422`로 거절한다.
- 유효한 RED: 기대 `422`, 실제 `201`
- Minimal GREEN: 입력 모델의 `room_id`에 `Field(min_length=1)`만 추가했다.

```bash
uv run pytest tests/test_reservations.py::test_rejects_empty_room_id
uv run pytest
```

Focused GREEN은 `1 passed`로 확인했다.

## Cycle 5 — 예약 목록 조회

- Test first: `test_lists_created_reservations`
- 계약: `GET /reservations`가 생성된 예약 목록과 `200`을 반환한다.
- 유효한 RED: 기대 `200`, 실제 `405`
- Minimal GREEN: 기존 인메모리 목록을 그대로 반환하는 GET 경로만 추가했다.

```bash
uv run pytest tests/test_reservations.py::test_lists_created_reservations
uv run pytest
```

Focused GREEN은 `1 passed`로 확인했다.

## 일반화된 충돌 로직의 계약 고정

다음 두 테스트는 새 구현을 끌어낸 RED-GREEN 사이클이 아니다. Cycle 3의 일반화된
구간 비교가 이미 통과시킨 동작을 이후 변경으로부터 보호하는 계약 고정 테스트다.

- 같은 방의 인접 예약은 허용한다.
- 다른 방이라면 시간이 겹쳐도 허용한다.

```bash
uv run pytest tests/test_reservations.py::test_allows_adjacent_reservation_for_same_room tests/test_reservations.py::test_allows_overlapping_time_for_different_room
uv run pytest tests/test_reservations.py
```

실제 결과는 각각 `2 passed`, `7 passed`였다.

## Cycle 6 — 발표 화면 제공

- Test first: `test_serves_presentation_lab`
- 계약: `GET /`가 `200`과 발표 핵심 문구를 포함한 HTML을 반환한다.
- 유효한 RED: 기대 `200`, 실제 `404`
- Minimal GREEN: 발표 HTML 경로와 `FileResponse`를 사용하는 root 경로만 추가했다.

```bash
uv run pytest tests/test_presentation.py::test_serves_presentation_lab
uv run pytest
```

구현 완료 후 실제 결과는 focused `1 passed`, 당시 전체 `8 passed`였다.

## Cycle 7 — 발표 근거 링크

- Test first: `test_presentation_links_to_primary_sources`
- 계약: 발표 화면에 Canon TDD, FastAPI Testing, `/docs` 링크가 모두 존재한다.
- 유효한 RED: Canon TDD 링크가 HTML에 없어 assertion이 실패했다.
- Minimal GREEN: 기존 `/docs` 링크는 유지하고 Canon TDD와 FastAPI Testing 링크만 추가했다.
- GREEN 후 refactor: 중복된 근거 링크를 제거하고 TDD 흐름 옆 한 곳에만 남겼다.

```bash
uv run pytest tests/test_presentation.py::test_presentation_links_to_primary_sources
uv run pytest
```

구현 완료 후 실제 결과는 focused `1 passed`, 전체 `9 passed`였다.

## 최종 검증

```bash
uv run pytest tests/test_reservations.py
uv run pytest
```

- 예약 API suite: `7 passed`
- 최종 전체 suite: `9 passed`

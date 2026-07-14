# 선택 부록 — mutmut를 넣지 않고 30초만 설명하기

## 결론

이 프로젝트의 메인 흐름에는 `mutmut`를 설치하지 않는다.

- AI-assisted TDD 발표의 핵심은 사람, AI 코딩 에이전트, pytest의 역할 분리다.
- `mutmut`는 AI 기능이 아니라 테스트 품질을 추가로 감사하는 mutation testing 도구다.
- mutmut 3.6.0은 Python 3.13을 지원하지만 native Windows에서는 실행되지 않는다.
- Git Bash는 WSL이 아니므로 Git Bash에서 실행해도 Windows 제약은 그대로다.

실제로 native Windows에서 실행하면 다음 메시지로 종료된다.

```text
To run mutmut on Windows, please use the WSL.
```

## 발표에서 보여줄 한 사례

현재 예약 충돌 조건에는 다음 비교가 있다.

```python
reservation.starts_at < current.ends_at
```

mutation testing 도구가 `<`를 `<=`로 바꾼다고 가정한다.

```python
reservation.starts_at <= current.ends_at
```

이 변경은 첫 예약이 11시에 끝나고 다음 예약이 11시에 시작해도 충돌로 판단하게 만든다. 현재의 `test_allows_adjacent_reservation_for_same_room` 테스트는 이 잘못된 변경을 발견한다.

관련 코드와 테스트는 Git Bash에서 다음 명령으로 찾을 수 있다.

```bash
rg -n "reservation.starts_at|test_allows_adjacent" app/main.py tests/test_reservations.py
uv run pytest tests/test_reservations.py::test_allows_adjacent_reservation_for_same_room -vv
```

## 발표 문장

> TDD는 요구사항을 테스트로 먼저 고정합니다. 하지만 테스트가 존재한다고 해서 반드시 좋은 테스트인 것은 아닙니다. mutation testing은 `<`를 `<=`처럼 살짝 바꾼 뒤 테스트를 다시 실행해 테스트가 실제 결함을 발견하는지 확인합니다. 이 프로젝트에서는 인접 예약 테스트가 그 변경을 잡아냅니다. mutmut는 AI가 아니라 TDD 뒤에 선택적으로 붙일 수 있는 테스트 품질 감사 도구입니다.

## 나중에 실제로 도입하려면

안정적인 Linux 또는 WSL 환경, WSL 내부 Python과 uv, 커밋된 작업 트리가 먼저 필요하다. 현재 구조에서 본격적인 mutation score를 사용하려면 FastAPI 라우팅과 충돌 정책을 분리해 중요한 정책 함수만 mutation 대상으로 좁히는 편이 낫다.

`mutmut apply <mutant>`는 원본 코드를 실제로 변경하며 결과는 `mutants/`에 저장된다. 따라서 실제 도입 시에는 `mutants/`를 `.gitignore`에 추가하고 apply 전에 반드시 커밋해야 한다.

## 공식 자료

- [mutmut 공식 문서](https://mutmut.readthedocs.io/en/latest/)
- [mutmut 3.6.0 PyPI](https://pypi.org/project/mutmut/)
- [native Windows 지원 이슈](https://github.com/boxed/mutmut/issues/397)

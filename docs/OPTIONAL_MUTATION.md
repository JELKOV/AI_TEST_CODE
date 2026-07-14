# 선택 부록 — mutmut를 넣지 않고 20초만 설명하기

## 결론

이 프로젝트의 메인 흐름에는 `mutmut`를 설치하지 않는다.

- 발표 핵심은 사람, AI 코딩 에이전트, `pytest`의 역할 분리다.
- `mutmut`는 AI 기능이 아니라 테스트 품질을 추가로 감사하는 mutation testing 도구다.
- native Windows에서는 실행할 수 없고 WSL이 필요하다.
- Git Bash는 WSL이 아니므로 현재 발표 환경의 라이브 실행에서 제외한다.

## 현재 코드로 설명할 mutation

지급 비율 합계 규칙은 다음과 같다.

~~~python
if total != 100:
    raise ValueError(...)
~~~

mutation testing 도구가 비교를 다음처럼 바꾼다고 가정한다.

~~~python
if total == 100:
    raise ValueError(...)
~~~

이 mutant는 정상 30/30/40을 거절하고 합계 90을 통과시킨다. 다음 두 테스트가
각 방향의 잘못을 발견한다.

~~~bash
uv run pytest tests/test_contract_payment_terms.py::test_accepts_valid_contract_payment_terms -vv
uv run pytest tests/test_contract_payment_terms.py::test_rejects_payment_percentage_sum_not_100 -vv
~~~

코드와 테스트 위치:

~~~bash
rg -n "total != 100|test_accepts_valid|test_rejects_payment_percentage" app/main.py tests
~~~

## 발표 문장

> TDD는 업무 규칙을 테스트로 먼저 고정합니다. 하지만 테스트가 있다는 사실과
> 그 테스트가 결함을 잘 발견한다는 것은 다릅니다. mutation testing은 비교 연산자를
> 일부러 바꾼 뒤 테스트가 실패하는지 확인합니다. 여기서는 `!=`를 `==`로 바꾸면
> 정상과 합계 오류 테스트가 모두 그 잘못을 잡습니다. mutmut는 AI가 아니라 TDD
> 뒤에 선택적으로 붙이는 테스트 품질 감사 도구입니다.

## 실제 도입 전 조건

Linux 또는 WSL 환경, 그 환경 안의 Python과 `uv`, 깨끗하게 커밋된 작업 트리가
먼저 필요하다. `mutmut apply`는 원본 코드를 변경하므로 현재 Git Bash 발표
흐름에서 즉석 실행하지 않는다.

## 공식 자료

- [mutmut 공식 문서](https://mutmut.readthedocs.io/en/latest/)
- [mutmut PyPI](https://pypi.org/project/mutmut/)
- [native Windows 지원 이슈](https://github.com/boxed/mutmut/issues/397)

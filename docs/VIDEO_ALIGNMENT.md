# 영상과 프로젝트 정합성

## 자료의 성격

- 영상: 딩코딩코 채널의 「AI 코딩 그렇게 하는 거 아닌데 - 켄트 백 (40년차)」, 2025-11-09, 5:04
- 사용자 지정 구간: [2:17부터 보기](https://www.youtube.com/watch?v=AAd8taPTyTM&t=137s)
- 주의: Kent Beck 본인의 발표 영상이 아니라 Kent Beck의 공개 자료와 CLAUDE.md를 Spring 예제로 해설·재현한 2차 자료다.
- 1차 자료: Kent Beck의 [Augmented Coding: Beyond the Vibes](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes)와 [BPlusTree3 CLAUDE.md](https://github.com/KentBeck/BPlusTree3/blob/ca80e4d85a99cd0af2effe717f709d43e80403bc/rust/docs/CLAUDE.md)

## 대응 관계

| 영상의 흐름 | 이 프로젝트 | 의미 |
|---|---|---|
| `plan.md`의 다음 미완료 테스트 | `plan.md` | 사람이 승인한 동작을 한 항목씩 선택 |
| Claude용 `CLAUDE.md` | `AGENTS.md` | AI 코딩 에이전트가 지킬 저장소 규칙 |
| `go`, `red`, `green`, `refactor` | `docs/AI_PROMPTS.md` | 도구에 종속되지 않은 단계별 작업 프롬프트 |
| 가장 작은 실패 테스트 | focused `pytest` | 구현되지 않은 행동 때문에 실패하는 유효한 RED 확인 |
| 통과에 필요한 최소 코드 | GREEN 규칙 | 테스트 삭제·완화와 요청하지 않은 기능 금지 |
| `tidy` 구조 변경 | AGENTS 8번 | 행동 변경과 구조 변경을 분리 |
| `check-tests` | focused test 후 full suite | AI의 설명이 아니라 실행 결과로 판정 |
| `commit-tdd` | AGENTS 10번 | 테스트·lint·type check가 모두 green일 때만 논리 단위 커밋 |
| 개발자의 중간 확인 | Human review | 정책, diff, 설계의 최종 책임은 사람에게 유지 |

## 정확하게 말해야 할 차이

- 영상은 Claude와 Spring/Kotlin/Gradle 예제이며, 현재 프로젝트는 특정 AI 제품에 종속되지 않는 Python/FastAPI 예제다.
- `pytest`는 Kent Beck이 지정한 도구가 아니라 Python에서 같은 검증 역할을 수행하도록 선택한 테스트 러너다.
- 테스트마다 사람의 명시적 승인을 요구하는 규칙은 영상의 직접 인용이 아니라 이 프로젝트가 추가한 더 강한 거버넌스다.
- 영상의 품질 향상과 구현 시간 단축은 데모의 주장이지 정량 실험 결과가 아니다.
- 영상에는 mutation testing이 없으므로 mutmut는 메인 흐름과 분리된 선택 부록으로 유지한다.

## 발표용 연결 문장

> 영상은 Claude custom command로 TDD 순서를 자동화합니다. 이 데모는 같은 핵심 규칙을 AGENTS.md, plan.md, pytest로 가볍게 옮겼습니다. 자동화되는 것은 사람이 승인한 다음 테스트의 실행 순서이고, 무엇이 정답인지와 설계가 올바른지는 여전히 사람이 판단합니다.

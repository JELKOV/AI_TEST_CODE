# AI-TDD Test Plan

사람이 동작과 기대 결과를 승인하면 AI 코딩 에이전트가 미완료 항목 하나만 선택한다.
완료 표시는 유효한 RED, focused GREEN, full suite GREEN을 모두 확인한 뒤에만 바꾼다.

## Live Demo Current Item

발표 실습에서는 지급조건 규칙 하나를 RED에서 GREEN까지 검증한 흐름을 보여준다.

- [x] **선택한 테스트:** 합계가 100이어도 선금 지급 비율이 음수이면
  `POST /contracts/payment-terms/validate`가 `422`로 거절한다. 실습 화면은 현재
  `Expected 422 / Actual 200`이었던 RED와 테스트를 유지한 최소 구현 요청문을 함께 보여준다.

## Completed History — AdMarket 계약 지급조건

- [x] 선금 30%, 중도금 30%, 잔금 40%와 순서가 맞는 지급 시점은 `200`으로 승인한다.
- [x] 세 지급 비율의 합계가 100이 아니면 `422`로 거절한다.
- [x] 선금·중도금·잔금의 지급 시점이 중복되면 `422`로 거절한다.
- [x] 선금보다 중도금이 빠른 역순 지급 시점은 `422`로 거절한다.
- [x] 발표 화면에서 정상·합계 오류·순서 오류를 실제 API로 구분해 실행한다.
- [x] OpenAPI 제품 표면에서 이전 예약 예제를 제거하고 계약 지급조건만 남긴다.

## Completed History — 회사 테스트 자산을 연결한 발표 확장

- [x] 합계가 100이어도 개별 지급 비율이 음수이면 `422`로 거절한다.
- [x] 발표 화면은 TVCF Main, AdMarket Frontend, AdMarket Backend의 현재 테스트 방식을
  우열이나 점수 없이 설명한다.
- [x] 발표 화면에서 정상·합계 오류·순서 오류·음수 비율을 직접 실행하고 API 응답을 확인한다.
- [x] 발표 화면은 Spec → Test Map → Focused Test → Full Gate의 AI 작업 흐름을 보여준다.
- [x] 발표용 TVCF 로고 자산을 별도 제품 API로 노출하지 않고 제공한다.
- [x] 화면 공유용 내비게이션, TVCF 로고와 40분 발표 흐름을 제공한다.

## Completed History — 발표 범위 교정

- [x] **선택한 다음 테스트:** TVCF 브랜딩은 유지하되, TVCF Main과 AdMarket
  Frontend는 회사의 테스트 형태를 이해하기 위한 배경으로만 소개하고 발표자가 직접
  설명·실습하는 코드 범위는 AdMarket Backend임을 화면에 명시한다.

- [x] **선택한 다음 테스트:** 발표 화면에서 TVCF Main과 AdMarket Frontend의 구체
  실행 명령은 제거하고, 발표자가 직접 실행할 AdMarket Backend 데모 명령만 제공한다.

## Completed History — 공유용 발표 페이지

- [x] **선택한 다음 테스트:** 1번 챕터는 프로젝트명이 아니라 Frontend와 Backend의
  테스트 형태로 구분하고, 도구·검증 대상·AI 완료 기준과 두 영역의 공통 품질 기준을
  청중이 이해할 수 있게 보여준다.

- [x] **선택한 다음 테스트:** 공유 페이지의 발표 운영 메모를 제거하고 방문자가
  이해할 수 있는 데모 검증 명령, 40분 구성, 참고 자료와 제품형 푸터 문구로 교체한다.
  Cycle 33에서 청중용 정보가 아닌 `40분 구성`은 다시 발표자 대본으로 분리했다.

## Completed History — AdMarket 계약 규칙 API 3종 실습

- [x] **선택한 다음 테스트:** `CONFIRMED_AMOUNT` 예산에 `production_cost`와
  `total_budget`을 함께 보내면 `POST /contracts/budget/validate`가 `200`으로 승인한다.

- [x] **선택한 다음 테스트:** `CONFIRMED_AMOUNT`에 확정 금액과 구간 예산을 함께
  보내면 `POST /contracts/budget/validate`가 `422`로 거절한다.

- [x] **선택한 다음 테스트:** `ATTACHED_FORMAT` 계약 제출자료에 `file_id`가 없으면
  `POST /contracts/submission-material/validate`가 `422`로 거절한다.

## Completed History — 설명·영상·명령·3 API 화면 확장

- [x] AI-TDD 참고 영상을 개인정보 보호 강화 embed로 페이지 안에서 직접 재생한다.
  Cycle 26에서 켄트 벡 본인 채널 원본의 발표용 구간으로 교체했다.

- [x] 서두에서 발표 목표와 현재 테스트 구조의 Strengths(장점),
  Trade-offs(고려사항)를 한글 설명과 함께 균형 있게 보여준다. Cycle 25에서
  특정 프로젝트명 없이 Frontend와 Backend의 공통 과제로 일반화했다.

- [x] **선택한 다음 테스트:** 라이브 실습 화면에서 지급조건·예산 형태·제출자료의
  pytest 코드와 focused 명령을 보여주고 서로 다른 실제 FastAPI 경로 3개를 호출한다.

- [x] **선택한 다음 테스트:** `uv sync`부터 focused pytest, full suite, lint·type까지
  실제 명령과 pytest가 API를 호출하고 PASS/FAIL을 판정하는 과정을 단계별로 보여준다.

- [x] **선택한 다음 테스트:** 일반 한글 설명은 단어 중간에서 줄바꿈하지 않고,
  긴 코드와 API 경로는 별도 규칙으로 컨테이너 안에서 안전하게 표시한다.

## Completed History — 서론 표현 교정과 켄트 벡 원본 영상

- [x] 영상 전 서론에서는 특정 프로젝트명을 사용하지 않고,
  Frontend와 Backend가 이미 사용하는 테스트 자산의 공통 과제로 발표 목표와
  장점·고려사항을 설명한다.

- [x] 켄트 벡 본인 채널의
  `Genie Sessions: Can You Force a Genie to Do TDD?`를
  발표 페이지에서 핵심 구간부터 직접 재생하고 원본 링크와 한글 시청 포인트를 제공한다.
  Cycle 31에서 GitHub 공식 사례와 현재 저장소 실습으로 교체해 발표 본문에서는 제외했다.

## Completed History — 한 줄 요점형 발표 문구

- [x] 긴 설명 문단을 짧은 요점으로 나누고, 데스크톱에서는
  각 요점을 한 줄로 표시하되 모바일에서는 가로 넘침 없이 자연스럽게 줄바꿈한다.

## Completed History — 3개 원본 영상 순서형 브리핑

- [x] **선택한 다음 테스트:** 무대 강연의 문제 제기, 인터뷰의 위험 사례, 라이브
  코딩의 실천 장면을 하나의 플레이어에서 순서대로 선택하고 영상별 한글 요점과
  다음 발표 문장을 확인할 수 있게 한다. Cycle 40에서 연결 문장은 공유 화면에서 제거하고
  `PRESENTATION.md`의 발표자 대본으로만 관리하도록 범위를 교정했다.

## Completed History — 영상 탭 한글 요점 전환

- [x] **선택한 다음 테스트:** 다른 영상 탭을 선택해도 해당 영상의 한글 요점 세 줄을
  번호가 붙은 `data-*` 속성에서 빠짐없이 읽어 화면에 표시한다.

## Completed History — 외부 영상 2개에서 로컬 실습으로 전환

- [x] **선택한 다음 테스트:** Kent Beck의 문제 제기와 GitHub 공식 Copilot TDD 사례만
  외부 영상으로 보고, 세 번째 실전 관찰은 현재 저장소의 `plan.md`, focused test와
  Live API를 직접 확인하는 단계로 연결한다.

## Completed History — 공유 페이지에서 발표 시간표 제거

- [x] **선택한 다음 테스트:** 청중에게 공유하는 웹페이지에서는 `40분 구성`과 구간별
  발표 시간을 노출하지 않고, 발표자 진행 정보는 `PRESENTATION.md`에서만 관리한다.

## Completed History — 2번 인터뷰 복원과 실전 영상 범위 교정

- [x] **선택한 다음 테스트:** 2번 The Pragmatic Engineer 인터뷰는 유지하고, 기존
  3번 Kent Beck 라이브 코딩 영상만 제외한다. 세 번째에는 GitHub 공식 사례를 두고,
  별도의 `실전 관찰` 단계와 전환 블록은 표시하지 않는다.

## Completed History — 회사 맥락을 마지막 적용 정리로 이동

- [x] **선택한 다음 테스트:** 기존 대제목과 도입부를 유지하고 별도 회사 맥락 챕터는
  제거한다. 서비스가 나뉜 현재 구조를 평가하지 않으며, AI가 한 저장소의 문맥으로
  작업할 때 생길 수 있는 범위 확장 위험과 focused test 하나의 필요성만 마지막 적용
  구간에서 짧게 정리한다.

## Completed History — 테스트 구성의 도구 표기 정리

- [x] **선택한 다음 테스트:** `Frontend와 Backend의 테스트 구성`에서 Backend 테스트
  도구는 `pytest`로만 표시하고, 각 검증 설명 아래에 중복된 배지형 도구 표시는 모두
  제거한다. FastAPI 설명은 실제 API 실행 흐름에만 유지한다.

## Completed History — AI와 TDD 작업 흐름의 출처와 실제 범위 명확화

- [x] **선택한 다음 테스트:** 두 번째 챕터는 Kent Beck의 TDD 흐름, OpenAI의 Harness
  Engineering 개념과 현재 데모의 조합을 구분해 설명한다. 실제 구현이 없는 `Test Map`,
  `Full Gate`, Spec Kit·TDAD 연결과 pytest 내부 동작 목록은 제거하고, 기대 결과 → RED
  → GREEN → 전체 확인 및 실제 Git Bash 명령만 보여준다.

## Completed History — 불필요한 보조 문서 정리

- [x] **선택한 다음 테스트:** README는 제거된 `AI_PROMPTS.md`,
  `OPTIONAL_MUTATION.md`, `VIDEO_ALIGNMENT.md`를 프로젝트 파일로 나열하지 않는다.

## Completed History — 작업 규칙 한글 안내

- [x] **선택한 다음 테스트:** `AGENTS.md`는 AI-TDD 작업 규칙마다
  초보자가 이해할 수 있는 한글 설명을 제공한다.

## Completed History — Markdown 문서 역할과 작업 흐름 연결

- [x] **선택한 다음 테스트:** 발표 화면은 작업 문서와 실행 증거의 역할을 구분하고,
  사람이 기대 결과를 승인한 뒤 RED·GREEN·전체 검증으로 이어지는 실제 흐름을 보여준다.

## Completed History — 최소 Repository Harness 실행 연결

- [x] **선택한 다음 테스트:** `harness.toml`은 작업 문서와 검증 명령을 선언하고,
  `scripts/tdd_harness.py`는 구성을 확인하거나 focused → full suite → lint → type 순서로
  실행해 첫 실패에서 중단하고 `.harness/latest-run.json`에 실행 증거를 남긴다. 발표
  화면은 이 실제 진입점과 사람이 판단해야 하는 범위를 구분해 보여준다.

## Completed History — 공유 영상에서 발표자 연결 문장 분리

- [x] **선택한 다음 테스트:** 공유 발표 페이지의 영상 영역은 영상별 한글 요점 세 줄과
  원본 링크만 보여주고, `다음 발표 문장`과 `data-video-takeaway` 전환 로직은 제거한다.
  영상 사이의 연결 문장은 `PRESENTATION.md`에서만 관리한다.

## Completed History — Hero 핵심 메시지 강화

- [x] **선택한 다음 테스트:** 첫 화면은 기능 목록 대신 AI 시대의 병목이 코드 생성보다
  정답 판정 기준에 있다는 문제를 제시하고, 테스트의 역할·Frontend와 Backend의 공유
  기준·계약 API와 Repository Harness 실습으로 이어지는 네 문장을 보여준다.

## Completed History — TVCF AI 변경의 검토와 인수인계 기준

- [x] **선택한 다음 테스트:** 팀 적용 화면은 Vibe·Agentic Coding으로 빨라진 코드 생성과
  TVCF에 오래 축적된 데이터·계약 문맥 사이의 간격을 설명하고, AI를 사용한 변경마다
  업무 의도·영향 범위·검증 증거·제외 범위를 남긴 뒤 report-only → 핵심 계약 → 안정된
  CI gate 순서로 적용하는 구체적인 기준을 보여준다.

## Completed History — 회사 상황과 적용 고려사항 중심으로 단순화

- [x] **선택한 다음 테스트:** 팀 적용 화면은 세부 PR 규칙이나 CI 도입 단계 대신 현재
  회사 상황 네 가지와 우리가 적용을 고려해볼 부분 세 가지를 번호 순서로 보여주고,
  작은 변경에서 확인한 기준부터 회사 방식으로 발전시키자는 가이드로 마무리한다.

## Completed History — 멀티레포의 AI Context Gap으로 적용 주제 구체화

- [x] **선택한 다음 테스트:** 마지막 적용 화면은 현재 회사 구조를 모노레포가 아닌
  멀티레포로 정확히 설명하고, 연결된 업무 문맥과 저장소 단위로 제한되기 쉬운 AI 문맥의
  차이를 `AI Context Gap`으로 제시한다. 해결 방향은 작업 전·중·후가 아니라 Repository
  Map·Contract Source·Verification Route 세 가지 연결로 보여준다.

## Completed History — 작업 문서의 현재 안내와 완료 이력 분리

- [x] **선택한 다음 테스트:** `plan.md`는 현재 진행 항목과 완료된 작업 이력을 구분한다.

## Completed History — 멀티레포 Context Gap의 결론을 TDD로 연결

- [x] **선택한 다음 테스트:** 멀티레포와 AI Context Gap은 회사 배경으로 유지하되, 적용
  결론은 문서 탐색 방법이 아니라 Frontend와 Backend가 같은 업무 시나리오를 정하고 각
  저장소의 테스트로 RED를 확인한 뒤 API 계약과 전체 테스트로 GREEN을 확인하는 TDD
  기준을 보여준다.

## Completed History — 우리 회사 TDD 도입 이유와 적용 범위로 전면 교체

- [x] **선택한 다음 테스트:** 마지막 장은 멀티레포 구조, 숨은 DB·내부 검증 제약,
  리팩토링 시 오류 재현과 디버깅이라는 TDD 도입 이유 세 가지와, TDD만으로 해결되지
  않거나 과하게 적용하면 안 되는 범위를 구분한다. 결론은 테스트로 재현 가능한 서버
  오류 원인을 코드 단계에서 먼저 잡아야 한다는 메시지로 마무리한다.

## Completed History — 발표 화면의 문장 흐름 정리

- [x] **선택한 다음 테스트:** 마지막 장의 카드 세부 문장과 결론은 긴 문단으로 줄바꿈되지
  않고, 각각 완결된 짧은 문장 또는 두 개의 독립된 결론으로 읽힌다.

## Completed History — TDD 도입 범위 결론 제거

- [x] **선택한 다음 테스트:** 마지막 장의 결론 블록은 제거하고, `왜 TDD가 도움이 되는가`와
  `TDD를 과하게 기대하면 안 되는 부분` 두 묶음 뒤에는 기존 Closing으로 바로 이동한다.

## Completed History — 수동 사이클 기록의 하네스 필수 구성 제거

- [x] **선택한 다음 테스트:** Repository Harness는 `AGENTS.md`와 `plan.md`만 필수 작업
  문서로 확인하고 수동 사이클 로그를 요구하거나 출력하지 않는다.

## Completed History — 발표 화면에서 수동 사이클 기록 제거

- [x] **선택한 다음 테스트:** AI와 TDD 작업 화면은 `plan.md`와 `AGENTS.md`만 소개하고,
  수동 사이클 문서 대신 하네스가 자동 생성한 JSON 실행 결과를 확인하는 흐름을 보여준다.

## Completed History — 수동 사이클 문서와 규칙 제거

- [x] **선택한 다음 테스트:** AI-TDD 작업 규칙은 10개만 제공하고, 저장소의 현재 안내와
  파일 구성은 별도의 수동 사이클 문서를 필수 산출물로 포함하지 않는다.

## Company Context Principle

이 발표는 기존 테스트 작성자나 프로젝트를 평가하지 않는다. TVCF Main과 AdMarket
Frontend는 로컬 구성에서 확인한 테스트 도구와 검증 목적만 회사 배경으로 언급한다.
발표자가 직접 작업 내용을 설명하고 시연하는 범위는 AdMarket Backend다.

- `tvcf_main_next_FE`: Jest 기반의 빠른 프론트엔드 로직 테스트 형태가 있다.
- `admarket_next_FE`: Vitest 기반의 빠른 검증과 Playwright 기반의 브라우저 흐름
  검증 형태가 있다.
- `admarket_fastapi_BE`: pytest의 unit·integration·e2e 계층과 architecture·API 계약
  같은 harness 검사를 함께 사용한다.

타 프로젝트의 구체 테스트 파일, 구현 세부사항, 실행 명령은 발표에서 시연하지 않는다.

운영 `PaymentTermsCommand`에는 이미 음수 방지 조건인 `Field(..., ge=0)`이 있다.
현재 데모는 그 규칙을 의도적으로 빠뜨린 학습용 복제본에서 RED를 만들며, 운영 코드의
결함을 주장하지 않는다.

## Source Mapping

원본 AdMarket 저장소는 읽기만 하고, 다음 업무 규칙을 현재 데모에 축약 이식했다.

- 원본 테스트: `tests/unittests/contract/service_test.py`의
  `TestPaymentTermsCommandValidation`
- 원본 제품 코드: `app/contract/application/command.py`의
  `PaymentTermsCommand.validate_payment_split()`
- 데모 테스트: `tests/test_contract_payment_terms.py`
- 데모 제품 코드: `app/main.py`의 `ContractPaymentTerms`

DB, 인증, 계약 저장, 알림은 복사하지 않았다. 발표에서 직접 설명할 수 있는
지급 비율과 지급 시점 규칙만 유지했다.

## Next Item Protocol

1. 사람이 다음 동작과 기대 결과를 승인한다.
2. AI가 미완료 항목 하나를 진행 중으로 표시한다.
3. 가장 작은 실행 가능한 테스트 하나를 작성한다.
4. `tdd_harness.py verify --focused <pytest-node-id>`를 실행해 focused 실패에서 멈추고,
   요구 동작 부재로 실패하는 유효한 RED인지 사람이 확인한다.
5. 테스트를 수정하지 않고 최소 제품 코드로 GREEN을 만든다.
6. 같은 verify 명령을 다시 실행해 focused·full suite·lint·type을 순서대로 통과시킨다.
7. GREEN 상태에서만 구조 변경을 별도로 수행하고 같은 verify 명령을 다시 실행한다.
8. `.harness/latest-run.json`과 diff를 검토한 뒤 항목을 완료한다.

# AI-TDD Test Plan

사람이 동작과 기대 결과를 승인하면 AI 코딩 에이전트가 미완료 항목 하나만 선택한다.
완료 표시는 유효한 RED, focused GREEN, full suite GREEN을 모두 확인한 뒤에만 바꾼다.

## Completed — AdMarket 계약 지급조건

- [x] 선금 30%, 중도금 30%, 잔금 40%와 순서가 맞는 지급 시점은 `200`으로 승인한다.
- [x] 세 지급 비율의 합계가 100이 아니면 `422`로 거절한다.
- [x] 선금·중도금·잔금의 지급 시점이 중복되면 `422`로 거절한다.
- [x] 선금보다 중도금이 빠른 역순 지급 시점은 `422`로 거절한다.
- [x] 발표 화면에서 정상·합계 오류·순서 오류를 실제 API로 구분해 실행한다.
- [x] OpenAPI 제품 표면에서 이전 예약 예제를 제거하고 계약 지급조건만 남긴다.

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
4. 요구 동작 부재로 실패하는 유효한 RED를 확인한다.
5. 테스트를 수정하지 않고 최소 제품 코드로 GREEN을 만든다.
6. focused 테스트와 full suite를 순서대로 실행한다.
7. GREEN 상태에서만 구조 변경을 별도로 수행하고 full suite를 다시 실행한다.
8. 실행 증거와 diff를 검토한 뒤 항목을 완료한다.

# AI-TDD Test Plan

## Live Demo Current Item

- [ ] 합계가 100이어도 선금 지급 비율이 음수이면 `POST /contracts/payment-terms/validate`가 `422`로 거절한다.

Focused test:
`tests/test_contract_payment_terms.py::test_rejects_negative_payment_percentage_even_when_sum_is_100`

Current RED:
`Expected 422 / Actual 200`

Completion:
`verify`가 focused · full · lint · type을 모두 통과한 뒤 `[x]`로 변경한다.

from fastapi.testclient import TestClient

from app.main import create_app


def test_serves_presentation_lab() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "AI에게 TDD를 시키는 것만으로 충분할까?" in response.text


def test_presentation_links_to_primary_sources() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    assert "https://newsletter.kentbeck.com/p/canon-tdd" in response.text
    assert "https://fastapi.tiangolo.com/tutorial/testing/" in response.text
    assert 'href="/docs"' in response.text


def test_presentation_explains_goal_and_test_tradeoffs_without_project_name_in_intro() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    intro = response.text.split('<section class="video-band"', maxsplit=1)[0]

    assert "오늘의 목표" in response.text
    assert "재현 가능한 테스트와 실제 HTTP 응답으로 증명한다" in response.text
    assert "Strengths (장점)" in response.text
    assert "Trade-offs (고려사항)" in response.text
    assert "unit · integration · e2e · harness" in response.text
    assert "DB·인증·외부 연동" in response.text
    assert "Mock과 실제 경계" in response.text
    assert "변경 경로와 가까운 테스트를 먼저 찾는다." in response.text
    assert "Frontend와 Backend는 테스트 파일이 아니라" in intro
    assert "Kent Beck · AI가 잘못된 방향으로 가는 3가지 신호" in intro
    assert "같은 행동을 반복한다" in intro
    assert "요청하지 않은 범위를 구현한다" in intro
    assert "테스트를 삭제하거나 우회한다" in intro
    assert "삭제·비활성화·기대값 변경" in intro
    assert "AdMarket" not in intro


def test_shared_video_briefing_keeps_audience_points_without_presenter_transitions() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    assert "세 관점으로 비교하는 AI 시대 TDD" in response.text
    assert 'role="tablist"' in response.text
    assert response.text.count('role="tab"') == 3
    assert 'data-video-key="problem"' in response.text
    assert 'data-video-key="risk"' in response.text
    assert 'data-video-key="github"' in response.text
    assert (
        "https://www.youtube-nocookie.com/embed/sMujMp4h_EY?start=24&amp;end=76"
        in response.text
    )
    assert (
        "https://www.youtube-nocookie.com/embed/aSXaxOdVtAQ?start=3024&amp;end=3118"
        in response.text
    )
    assert (
        "https://www.youtube-nocookie.com/embed/arn6hqERKn4?start=366&amp;end=444"
        in response.text
    )
    assert "TDD, AI agents and coding with Kent Beck" in response.text
    assert "02 · 위험 확인" in response.text
    assert "AI가 테스트를 바꾸려 하면 누가 멈추는가?" in response.text
    assert (
        "Test-driven development with GitHub Copilot: A beginner's practical guide"
        in response.text
    )
    assert "GitHub 공식 채널 · 2025" in response.text
    assert "개발자가 기능 요구조건을 먼저 정의한다." in response.text
    assert "Copilot이 아직 없는 기능의 테스트를 먼저 만든다." in response.text
    assert "실패 확인 뒤 구현을 만들고 다시 실행한다." in response.text
    assert "03 · GitHub 공식 사례" in response.text
    assert "다음 발표 문장" not in response.text
    assert "정답이 없다는 사실을 출발점으로 삼는다." not in response.text
    assert "data-video-takeaway" not in response.text
    assert "video-takeaway" not in response.text
    assert "실전 관찰" not in response.text
    assert 'id="local-practice"' not in response.text
    assert "allowfullscreen" in response.text
    assert "ouGJSC5SdRQ" not in response.text
    assert "AAd8taPTyTM" not in response.text


def test_presentation_runs_three_admarket_contract_rule_apis() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    assert "3 Contract Rule APIs (계약 규칙 API 3개)" in response.text
    assert "Payment Terms (지급조건 검증)" in response.text
    assert "Budget Shape (예산 입력 형태 검증)" in response.text
    assert "Submission Material (계약 제출자료 검증)" in response.text
    assert "POST /contracts/payment-terms/validate" in response.text
    assert "POST /contracts/budget/validate" in response.text
    assert "POST /contracts/submission-material/validate" in response.text
    assert 'data-scenario="payment-range"' in response.text
    assert 'data-scenario="budget-shape"' in response.text
    assert 'data-scenario="material-file"' in response.text


def test_presentation_removes_frontend_backend_test_layers_chapter() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    assert 'id="company"' not in response.text
    assert 'href="#company"' not in response.text
    assert "Frontend / Backend Test Layers" not in response.text
    assert "Frontend와 Backend의" not in response.text
    assert "테스트 구성" not in response.text
    assert "Frontend 테스트" not in response.text
    assert "Backend 테스트" not in response.text
    assert "01 · 작업 흐름" in response.text
    assert "02 · 실습" in response.text
    assert "03 · 적용" in response.text
    assert 'src="/assets/tvcf-logo.png"' in response.text


def test_ai_tdd_workflow_explains_sources_and_actual_demo_steps() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    chapter = response.text.split('id="harness"', maxsplit=1)[1].split('id="lab"', maxsplit=1)[0]

    assert "AI와 TDD를 연결하는 실제 작업 순서" in chapter
    assert "Kent Beck · TDD" in chapter
    assert "OpenAI · Harness Engineering" in chapter
    assert "현재 저장소의 Markdown 문서" in chapter
    assert "무엇을 할지" in chapter
    assert "사람이 승인한 테스트 목록에서 이번에 진행할 하나를 선택한다." in chapter
    assert "어떻게 작업할지" in chapter
    assert "AI가 지킬 10개 규칙으로 유효한 RED, 최소 구현과 검증 순서를 고정한다." in chapter
    assert "TDD_CYCLES.md" not in chapter
    assert "수동 사이클 기록" not in chapter
    assert "사람 승인 → plan.md에서 하나 선택 → AGENTS.md 규칙으로 RED·GREEN → 전체 검증 → JSON 실행 결과 확인" in chapter
    assert ".harness/latest-run.json에서 실행 결과를 확인한다." in chapter
    assert "별도 제품이 아니다." not in chapter
    assert "AGENTS.md, plan.md와 pytest 명령을 조합한 예시다." not in chapter
    assert "01 / EXPECTED" in chapter
    assert "02 / RED" in chapter
    assert "03 / GREEN" in chapter
    assert "04 / VERIFY" in chapter
    assert "기대 결과 → RED → GREEN → 전체 확인" in chapter
    assert "Repository Harness → Test Map → Full Gate" not in chapter
    assert "Test Map" not in chapter
    assert "Full Gate" not in chapter
    assert "GitHub · Spec Kit" not in chapter
    assert "TDAD · Test Impact Analysis" not in chapter
    assert "Collect (수집)" not in chapter
    assert "TestClient가 FastAPI app에 in-process POST" not in chapter
    assert "데모 검증 명령" in response.text
    assert "실제로 실행하는 Git Bash 명령" in chapter
    assert "40분 구성" not in response.text
    assert "2 Videos + Live Handoff" not in response.text
    assert "37–40분" not in response.text
    assert ">참고 자료</h2>" in response.text
    assert "TVCF AI-TDD Working Demo" in response.text
    assert "타 프로젝트의 실행 명령" not in response.text
    assert "발표 실습에서 직접 실행할 명령" not in response.text
    assert "현재 테스트 자산을 평가하지 않고 연결하는 발표" not in response.text
    assert "yarn test" not in response.text
    assert "pnpm --filter" not in response.text


def test_minimal_repository_harness_connects_docs_gates_and_evidence() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    chapter = response.text.split('id="harness"', maxsplit=1)[1].split('id="lab"', maxsplit=1)[0]

    assert "실행 가능한 최소 Repository Harness" in chapter
    assert "harness.toml" in chapter
    assert "scripts/tdd_harness.py" in chapter
    assert ".harness/latest-run.json" in chapter
    assert (
        "uv run python scripts/tdd_harness.py verify --focused "
        "tests/test_contract_budget.py::test_accepts_confirmed_budget_with_production_and_total_amounts"
        in chapter
    )
    assert "업무 기대값과 RED 실패 이유는 사람이 판단한다." in chapter
    assert "uv run pytest tests/test_contract_payment_terms.py" in response.text
    assert "https://newsletter.kentbeck.com/p/canon-tdd" in chapter
    assert "https://openai.com/index/harness-engineering/" in response.text


def test_presentation_explains_real_test_commands_and_results() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    assert "실제로 실행하는 Git Bash 명령" in response.text
    assert "uv sync" in response.text
    assert "uv run pytest tests/test_contract_budget.py" in response.text
    assert "uv run pytest -vv" in response.text
    assert "uv run ruff check ." in response.text
    assert "uvx pyright" in response.text
    assert "실패 이유 확인" in response.text
    assert "선택 테스트 통과" in response.text
    assert "전체 확인" in response.text


def test_presentation_maps_three_api_cases_to_test_payloads() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    lab = response.text.split('id="lab"', maxsplit=1)[1].split(
        'id="adoption"', maxsplit=1
    )[0]

    assert "LIVE TDD · INITIAL STATE" in lab
    assert "현재 실패를 AI에게 어떻게 요청할까?" in lab
    assert "Expected 422" in lab
    assert "Actual 200" in lab
    assert "advance_payment_percentage: int" in lab
    assert "테스트를 수정하거나 삭제하지 않는다." in lab
    assert "선금 지급 비율이 음수이면 422로 거절하는 최소 제품 코드만 작성한다." in lab
    assert "같은 verify 명령을 다시 실행한다." in lab
    assert "판단 기준" in lab
    assert "테스트 유지" in lab
    assert "제품 코드 한 줄" in lab
    assert "focused · full · lint · type" in lab
    assert "test_rejects_negative_payment_percentage_even_when_sum_is_100" in response.text
    assert "test_accepts_confirmed_budget_with_production_and_total_amounts" in response.text
    assert "test_rejects_attached_material_without_file_id" in response.text
    assert "advance_payment_percentage: -10" in response.text
    assert 'budget_type: "CONFIRMED_AMOUNT"' in response.text
    assert 'format_type: "ATTACHED_FORMAT"' in response.text
    assert 'path: "/contracts/payment-terms/validate"' in response.text
    assert 'path: "/contracts/budget/validate"' in response.text
    assert 'path: "/contracts/submission-material/validate"' in response.text


def test_serves_tvcf_logo_without_exposing_an_openapi_product_route() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/assets/tvcf-logo.png")
        schema = client.get("/openapi.json").json()

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert response.content.startswith(b"\x89PNG")
    assert "/assets/tvcf-logo.png" not in schema["paths"]


def test_presentation_has_navigation_brand_and_references() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    assert 'src="/assets/tvcf-logo.png"' in response.text
    assert 'href="#company"' not in response.text
    assert 'href="#harness"' in response.text
    assert 'href="#lab"' in response.text
    assert 'href="#adoption"' in response.text
    assert "https://playwright.dev/docs/test-agents" in response.text
    assert "https://arxiv.org/abs/2603.17973" in response.text


def test_presentation_keeps_korean_words_together_without_breaking_code() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    assert "word-break: keep-all;" in response.text
    assert "pre,\n    code" in response.text
    assert "word-break: normal;" in response.text


def test_presentation_frames_ai_speed_as_a_verification_problem() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    intro = response.text.split('<section class="video-band"', maxsplit=1)[0]

    assert "AI에게 TDD를 시키는 것만으로 충분할까?" in intro
    assert "AI가 코드를 빨리 만들수록, 무엇이 맞는지 판단하는 기준이 더 중요해진다." in intro
    assert "테스트는 오류 검사를 넘어 업무 의도와 완료 조건을 AI에게 전달한다." in intro
    assert (
        "Frontend와 Backend는 테스트 파일이 아니라 API 계약과 핵심 시나리오를 공유한다."
        in intro
    )
    assert "작은 계약 API와 Repository Harness로 이 기준이 실제로 작동하는지 확인한다." in intro
    assert "새 테스트 도구를 강요하지 않는다." not in intro
    assert 'class="company-need"' not in response.text
    assert "AI 활용이나 기존 테스트를 제한하고 평가하는 발표가 아니다." not in response.text
    assert "하나의 회사, 여러 업무 역할" not in response.text
    assert response.text.count('class="summary-lines single-line-points"') >= 6
    assert "@media (min-width: 981px)" in response.text
    assert ".single-line-points > li" in response.text
    assert "white-space: nowrap;" in response.text
    assert "이 발표는 새 테스트 도구를 강요하는 이야기가 아니라," not in response.text


def test_team_adoption_explains_company_tdd_need_limits_and_conclusion() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    adoption = response.text.split('id="adoption"', maxsplit=1)[1].split(
        'aria-labelledby="references-title"', maxsplit=1
    )[0]

    assert "우리 회사에 TDD가 필요한 이유와 적용 범위" in adoption
    assert "03 · Why TDD Here" in adoption
    assert "운영 장애를 모두 테스트로 없앨 수는 없다." in adoption
    assert "코드로 재현 가능한 오류는 배포 전에 반복 검증할 수 있다." in adoption
    assert "현재 구조에서 테스트가 효과적인 세 지점" in adoption
    assert adoption.count('class="situation-item"') == 3
    assert "01 · 멀티레포 구조" in adoption
    assert "02 · 숨은 데이터 제약" in adoption
    assert "03 · 리팩토링·디버깅" in adoption
    assert "기대 동작과 연결 계약을 테스트로 고정한다." in adoption
    assert "기존 DB 데이터·내부 validator·상태 조합" in adoption
    assert "실패 테스트로 오류를 재현" in adoption
    assert "TDD를 과하게 기대하면 안 되는 세 가지" in adoption
    assert adoption.count('class="adoption-item"') == 3
    assert "01 · 멀티레포 전체 해결" in adoption
    assert "02 · 운영 환경 완전 복제" in adoption
    assert "03 · 모든 코드 Test-first" in adoption
    assert "저장소 연결 자체를 해결하지는 않는다" in adoption
    assert "실제 DB와 외부 환경을 모두 재현하지 못한다" in adoption
    assert "위험이 낮은 코드까지 강제하지 않는다" in adoption
    assert "integration·E2E·모니터링" in adoption
    assert 'class="goal-statement adoption-conclusion"' not in adoption
    assert "테스트 입력으로 재현한다." in adoption
    assert "원인과 재발을 함께 확인한다." in adoption
    assert "AI Context Gap" not in adoption
    assert "SHARED SCENARIO" not in adoption
    assert "REPO-LOCAL RED" not in adoption
    assert "CONTRACT GREEN" not in adoption


def test_video_tabs_read_all_three_korean_points_when_selection_changes() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    assert 'tab.getAttribute("data-video-point-1")' in response.text
    assert 'tab.getAttribute("data-video-point-2")' in response.text
    assert 'tab.getAttribute("data-video-point-3")' in response.text
    assert "videoPoints.replaceChildren" in response.text

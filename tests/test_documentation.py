from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REMOVED_OPTIONAL_DOCS = (
    "AI_PROMPTS.md",
    "OPTIONAL_MUTATION.md",
    "VIDEO_ALIGNMENT.md",
)


def test_readme_does_not_list_removed_optional_docs() -> None:
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

    for document_name in REMOVED_OPTIONAL_DOCS:
        assert document_name not in readme
        assert not (PROJECT_ROOT / "docs" / document_name).exists()


def test_working_agreement_and_docs_do_not_require_manual_cycle_log() -> None:
    agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")

    for rule_number in range(1, 11):
        assert f"### {rule_number}번 규칙" in agents
    assert "### 11번 규칙" not in agents

    cycle_log = PROJECT_ROOT / "docs" / "TDD_CYCLES.md"
    assert not cycle_log.exists()

    current_guides = (
        "AGENTS.md",
        "README.md",
        "PRESENTATION.md",
        "plan.md",
        "harness.toml",
        "docs/REPOSITORY_HARNESS.md",
    )
    for relative_path in current_guides:
        content = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
        assert "TDD_CYCLES.md" not in content

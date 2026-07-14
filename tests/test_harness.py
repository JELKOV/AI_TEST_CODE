import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_harness_check_connects_required_documents_commands_and_evidence() -> None:
    completed = subprocess.run(
        [sys.executable, "scripts/tdd_harness.py", "check"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "Repository Harness: ready" in completed.stdout
    assert "agreement: AGENTS.md" in completed.stdout
    assert "plan: plan.md" in completed.stdout
    assert "cycle_log" not in completed.stdout
    assert "TDD_CYCLES.md" not in completed.stdout
    assert "focused: uv run pytest {focused} -vv" in completed.stdout
    assert "full: uv run pytest -vv" in completed.stdout
    assert "lint: uv run ruff check ." in completed.stdout
    assert "type: uvx pyright" in completed.stdout
    assert "evidence: .harness/latest-run.json" in completed.stdout

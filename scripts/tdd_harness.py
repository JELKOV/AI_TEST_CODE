from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DOCUMENT_KEYS = ("agreement", "plan", "cycle_log")
STAGE_KEYS = ("focused", "full", "lint", "type")


class HarnessConfigError(ValueError):
    pass


@dataclass(frozen=True)
class HarnessConfig:
    root: Path
    documents: dict[str, Path]
    commands: dict[str, list[str]]
    evidence_directory: Path
    evidence_latest: Path


def _required_table(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise HarnessConfigError(f"[{key}] table is required")
    return value


def _repository_path(root: Path, raw_path: str, label: str) -> Path:
    path = (root / raw_path).resolve()
    try:
        path.relative_to(root)
    except ValueError as error:
        raise HarnessConfigError(f"{label} must stay inside the repository") from error
    return path


def load_config(config_path: Path) -> HarnessConfig:
    resolved_config = config_path.resolve()
    with resolved_config.open("rb") as config_file:
        data = tomllib.load(config_file)

    if data.get("version") != 1:
        raise HarnessConfigError("version must be 1")

    root = resolved_config.parent
    document_table = _required_table(data, "documents")
    documents: dict[str, Path] = {}
    for key in DOCUMENT_KEYS:
        raw_path = document_table.get(key)
        if not isinstance(raw_path, str) or not raw_path:
            raise HarnessConfigError(f"documents.{key} must be a path")
        document_path = _repository_path(root, raw_path, f"documents.{key}")
        if not document_path.is_file():
            raise HarnessConfigError(f"documents.{key} does not exist: {raw_path}")
        documents[key] = document_path

    command_table = _required_table(data, "commands")
    commands: dict[str, list[str]] = {}
    for key in STAGE_KEYS:
        raw_command = command_table.get(key)
        if (
            not isinstance(raw_command, list)
            or not raw_command
            or not all(isinstance(part, str) and part for part in raw_command)
        ):
            raise HarnessConfigError(f"commands.{key} must be a non-empty string array")
        commands[key] = list(raw_command)

    if not any("{focused}" in part for part in commands["focused"]):
        raise HarnessConfigError("commands.focused must contain {focused}")

    evidence_table = _required_table(data, "evidence")
    raw_directory = evidence_table.get("directory")
    raw_latest = evidence_table.get("latest")
    if not isinstance(raw_directory, str) or not raw_directory:
        raise HarnessConfigError("evidence.directory must be a path")
    if not isinstance(raw_latest, str) or not raw_latest:
        raise HarnessConfigError("evidence.latest must be a path")

    return HarnessConfig(
        root=root,
        documents=documents,
        commands=commands,
        evidence_directory=_repository_path(root, raw_directory, "evidence.directory"),
        evidence_latest=_repository_path(root, raw_latest, "evidence.latest"),
    )


def _relative(config: HarnessConfig, path: Path) -> str:
    return path.relative_to(config.root).as_posix()


def print_check(config: HarnessConfig) -> None:
    print("Repository Harness: ready")
    print("Documents")
    for key in DOCUMENT_KEYS:
        print(f"  {key}: {_relative(config, config.documents[key])}")
    print("Gates")
    for key in STAGE_KEYS:
        print(f"  {key}: {' '.join(config.commands[key])}")
    print(f"  evidence: {_relative(config, config.evidence_latest)}")


def _write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    temporary_path.write_text(content, encoding="utf-8")
    temporary_path.replace(path)


def write_evidence(config: HarnessConfig, report: dict[str, Any], run_id: str) -> Path:
    content = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    run_path = config.evidence_directory / f"{run_id}.json"
    _write_atomic(run_path, content)
    _write_atomic(config.evidence_latest, content)
    return run_path


def run_verify(config: HarnessConfig, focused_test: str) -> int:
    print_check(config)
    print()

    started_at = datetime.now(timezone.utc)
    run_id = started_at.strftime("%Y%m%dT%H%M%S.%fZ")
    stages: list[dict[str, Any]] = []
    failed_exit_code = 0

    for index, stage_name in enumerate(STAGE_KEYS, start=1):
        command = [part.replace("{focused}", focused_test) for part in config.commands[stage_name]]
        print(f"[{index}/4] {stage_name}: {' '.join(command)}", flush=True)
        stage_started = time.monotonic()
        error_message: str | None = None
        try:
            completed = subprocess.run(command, cwd=config.root, check=False)
            exit_code = completed.returncode
        except OSError as error:
            exit_code = 127
            error_message = str(error)
            print(f"ERROR: {error_message}", file=sys.stderr)

        stages.append(
            {
                "name": stage_name,
                "command": command,
                "status": "passed" if exit_code == 0 else "failed",
                "exit_code": exit_code,
                "duration_ms": round((time.monotonic() - stage_started) * 1000),
                **({"error": error_message} if error_message else {}),
            }
        )

        if exit_code != 0:
            failed_exit_code = exit_code
            print(f"STOP: {stage_name} failed with exit code {exit_code}")
            break

    finished_at = datetime.now(timezone.utc)
    report = {
        "version": 1,
        "run_id": run_id,
        "status": "failed" if failed_exit_code else "passed",
        "focused_test": focused_test,
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "documents": {
            key: _relative(config, config.documents[key]) for key in DOCUMENT_KEYS
        },
        "stages": stages,
    }
    run_path = write_evidence(config, report, run_id)
    print(f"Evidence: {_relative(config, run_path)}")
    print(f"Latest: {_relative(config, config.evidence_latest)}")
    return failed_exit_code


def build_parser() -> argparse.ArgumentParser:
    default_config = Path(__file__).resolve().parents[1] / "harness.toml"
    parser = argparse.ArgumentParser(description="Run the repository's AI-TDD quality gates.")
    parser.add_argument("--config", type=Path, default=default_config)
    subparsers = parser.add_subparsers(dest="action", required=True)
    subparsers.add_parser("check", help="Validate and print the harness wiring.")
    verify_parser = subparsers.add_parser("verify", help="Run focused and repository gates.")
    verify_parser.add_argument("--focused", required=True, help="Pytest node ID for this change.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        config = load_config(args.config)
    except (HarnessConfigError, OSError, tomllib.TOMLDecodeError) as error:
        print(f"Harness configuration error: {error}", file=sys.stderr)
        return 2

    if args.action == "check":
        print_check(config)
        return 0
    return run_verify(config, args.focused)


if __name__ == "__main__":
    raise SystemExit(main())

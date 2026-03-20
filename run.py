# Planned migration path:
# 1. Use CLAUDE.md as the operating workflow inside Claude Code.
# 2. Migrate orchestration into this file using Anthropic API calls.
# 3. Run the API-based workflow on a schedule, such as cron.
"""Stub CLI entrypoint for future API-based automation of the GEO pipeline."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Future CLI entrypoint for the Radisson GEO Optimizer."
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Reserved for future live pipeline execution.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Reserved for future validation-only execution.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    parser.parse_args()
    print(
        "run.py is a stub for future API automation. To run the pipeline now, open this repo in Claude Code and type /geo-run"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

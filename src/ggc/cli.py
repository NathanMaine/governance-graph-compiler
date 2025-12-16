from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .compiler import parse_policy, write_graph


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ggc", description="Governance Graph Compiler")
    subparsers = parser.add_subparsers(dest="command", required=True)

    compile_parser = subparsers.add_parser("compile", help="Compile policy markdown into a graph")
    compile_parser.add_argument("--policy", required=True, type=Path, help="Path to policies.md")
    compile_parser.add_argument("--out", default=Path("out"), type=Path, help="Output directory (default: out)")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "compile":
        graph = parse_policy(args.policy)
        graph_json, graph_dot = write_graph(graph, args.out)
        print(f"Graph JSON written to {graph_json}")
        print(f"DOT written to {graph_dot}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


@dataclass
class Graph:
    nodes: List[dict]
    edges: List[dict]


def parse_policy(path: Path) -> Graph:
    text = path.read_text().splitlines()
    nodes: List[dict] = []
    edges: List[dict] = []

    section_counter = 0
    rule_counter = 0
    current_section_id: str | None = None

    for line in text:
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            title = stripped[level:].strip()
            section_counter += 1
            section_id = f"section-{section_counter}"
            nodes.append({
                "id": section_id,
                "label": title,
                "type": "section",
                "level": level,
            })
            current_section_id = section_id
            continue

        if stripped.startswith(('-', '*')):
            rule_counter += 1
            label = stripped.lstrip('-* ').strip()
            rule_id = f"rule-{rule_counter}"
            nodes.append({
                "id": rule_id,
                "label": label,
                "type": "rule",
            })
            if current_section_id:
                edges.append({"from": current_section_id, "to": rule_id, "label": "contains"})
            continue

        # Fallback: treat plain text as a rule under the current section
        rule_counter += 1
        rule_id = f"rule-{rule_counter}"
        nodes.append({
            "id": rule_id,
            "label": stripped,
            "type": "rule",
        })
        if current_section_id:
            edges.append({"from": current_section_id, "to": rule_id, "label": "contains"})

    return Graph(nodes=nodes, edges=edges)


def to_dot(graph: Graph) -> str:
    lines = ["digraph G {"]
    for node in graph.nodes:
        label = node.get("label", "")
        node_id = node["id"]
        lines.append(f'  "{node_id}" [label="{label}"];')
    for edge in graph.edges:
        edge_label = edge.get("label", "")
        lines.append(f'  "{edge["from"]}" -> "{edge["to"]}" [label="{edge_label}"];')
    lines.append("}")
    return "\n".join(lines)


def write_graph(graph: Graph, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    graph_json = out_dir / "graph.json"
    graph_dot = out_dir / "graph.dot"

    graph_json.write_text(json.dumps(asdict(graph), indent=2))
    graph_dot.write_text(to_dot(graph))
    return graph_json, graph_dot

# Governance Graph Compiler

Compiles natural-language policy statements into executable governance graphs
for agent routing, enforcement, and auditing.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python -m ggc.cli compile --policy policies/example.md --out out
```

Outputs: `out/graph.json` and `out/graph.dot` with headings/bullets turned into nodes and edges.

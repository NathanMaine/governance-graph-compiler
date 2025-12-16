import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.append(str(SRC_ROOT))

from ggc.cli import main  # noqa: E402


def test_compile_creates_graph(tmp_path):
    policy = Path(__file__).parent / "fixtures" / "policy.md"
    out_dir = tmp_path / "out"

    code = main(["compile", "--policy", str(policy), "--out", str(out_dir)])

    assert code == 0
    assert (out_dir / "graph.json").exists()
    dot = out_dir / "graph.dot"
    assert dot.exists()
    assert "digraph" in dot.read_text()

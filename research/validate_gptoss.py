"""Validacion end-to-end: corre el pipeline oficial de scoring (eval_attack) con
nuestro attack.py contra gpt-oss:20b local + guardian optimal_public. Config minima
(pocas llamadas al LLM, que es lento) para PROBAR score > 0 contra el modelo real.
"""

import importlib.util
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "research"))

from ollama_gptoss_agent import OllamaGptOssAgent  # noqa: E402
from aicomp_sdk.evaluation.ops import eval_attack, resolve_fixtures_dir  # noqa: E402
from aicomp_sdk.scoring import score_attack, score_attack_raw  # noqa: E402


def load_attack(msgs_per_finding: int, max_findings: int):
    spec = importlib.util.spec_from_file_location("attack_mod", str(ROOT / "attack.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    class Small(mod.AttackAlgorithm):
        def __init__(self, config=None):
            super().__init__({"msgs_per_finding": msgs_per_finding, "max_findings": max_findings})

    return Small


def main():
    mpf = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    mf = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    budget = float(sys.argv[3]) if len(sys.argv) > 3 else 900.0
    print(f"[cfg] msgs/finding={mpf} findings={mf} budget={budget}s  (LLM calls ~= {mpf*mf})")

    AttackCls = load_attack(mpf, mf)
    fixtures = resolve_fixtures_dir(None)

    t0 = time.monotonic()
    validated = eval_attack(
        AttackCls,
        budget_s=budget,
        agent_factory=lambda: OllamaGptOssAgent(),
        env_selection="gym",
        fixtures_dir=fixtures,
    )
    dt = time.monotonic() - t0

    raw = score_attack_raw(validated)
    norm = score_attack(validated)
    n_pred = sum(len(f.get("predicates", [])) for f in validated)
    cells = len({f.get("score_cell_signature", {}).get("hash") for f in validated})
    print(f"[result] {dt:.1f}s | findings_validos={len(validated)} | predicados={n_pred} | unique_cells={cells}")
    print(f"[score] raw={raw:.1f}  normalized={norm:.3f}")
    for i, f in enumerate(validated[:3]):
        preds = [p.get("predicate") for p in f.get("predicates", [])]
        print(f"  finding[{i}] predicados={preds}")


if __name__ == "__main__":
    main()

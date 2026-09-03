"""Genera el notebook de ENVIO denso (jed-attack-dual) embebiendo attack_v2.py.

Estructura identica a la del jed-attack-dense que ya scoreo (41.265): 5 celdas,
internet OFF, T4; el rerun del gateway provee los modelos y sobrescribe submission.csv.
Kernel NUEVO para no pisar el failsafe banqueado.
"""
import base64
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
ATTACK = sys.argv[1] if len(sys.argv) > 1 else "attack_v2.py"
KID = sys.argv[2] if len(sys.argv) > 2 else "jed-attack-dual"
attack = (ROOT / ATTACK).read_text()

# NO se antepone preambulo: attack.py puede empezar por `from __future__ import annotations`
# (debe ir lo primero) y la celda 1 del notebook ya deja sys.path listo antes de importarlo.
blob = base64.b64encode(attack.encode()).decode()

setup = (
    "import sys, glob\n"
    "from pathlib import Path\n"
    "sys.argv=[sys.argv[0]]\n"
    "for c in glob.glob('/kaggle/input/**/kaggle_evaluation', recursive=True):\n"
    "    dr=str(Path(c).parent)\n"
    "    if dr not in sys.path: sys.path.insert(0,dr)\n"
    "    print('root',dr); break\n"
    "print('ok')\n"
)
write_attack = (
    "import base64\n"
    f'B64="{blob}"\n'
    "open('/kaggle/working/attack.py','w').write(base64.b64decode(B64).decode())\n"
    "print('attack_v2 escrito')\n"
)
placeholder = (
    "open('/kaggle/working/submission.csv','w').write("
    "'Id,Score\\n'+''.join(f'{r},0\\n' for r in "
    "('gpt_oss_public','gpt_oss_private','gemma_public','gemma_private')))\n"
    "print('ph ok')\n"
)
serve = (
    "import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as isv\n"
    "isv.JEDAttackInferenceServer().serve()\n"
)


def code(src):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": src.splitlines(keepends=True)}


nb = {
    "cells": [
        {"cell_type": "markdown", "metadata": {}, "source": [
            "# JED Attack DUAL — single-post N=2000, mensaje que casca gpt_oss + gemma-4\n"]},
        code(setup), code(write_attack), code(placeholder), code(serve),
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4, "nbformat_minor": 5,
}

outdir = HERE / KID
outdir.mkdir(exist_ok=True)
(outdir / f"{KID}.ipynb").write_text(json.dumps(nb, indent=1))
(outdir / "kernel-metadata.json").write_text(json.dumps({
    "id": f"marcmaldonado/{KID}",
    "title": KID.replace("-", " ").title(),
    "code_file": f"{KID}.ipynb",
    "language": "python",
    "kernel_type": "notebook",
    "is_private": True,
    "enable_gpu": True,
    "enable_tpu": False,
    "enable_internet": False,
    "dataset_sources": [],
    "competition_sources": ["ai-agent-security-multi-step-tool-attacks"],
    "kernel_sources": [],
    "model_sources": [],
    "machine_shape": "NvidiaTeslaT4",
}, indent=2))
print("escrito", outdir, "con TEMPLATE_KEY del attack_v2 actual")

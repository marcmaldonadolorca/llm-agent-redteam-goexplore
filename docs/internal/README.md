# Internal working notes

The day-by-day working log of the competition (late August to 1 September 2026), kept as it was
written, in Spanish. The [root README](../../README.md) and [`../finding.md`](../finding.md)
(English) are the summary; these files are the evidence and the full derivation behind them.

- [`HALLAZGO-2026-08-27.md`](HALLAZGO-2026-08-27.md) is the central document: the mechanics of
  the evaluation read directly from the downloaded gateway and `aicomp_sdk` 3.1.2, with every
  submission's public score logged against the change that produced it, up to the final reveal
  on 2 September where every private score was 0.
- [`PLAN-ATAQUE.md`](PLAN-ATAQUE.md) is the full derivation of the scoring model and the plan,
  with each claim marked as verified against the SDK code or against the local sandbox.
- [`PLAN-ESCALADO-2026-08-29.md`](PLAN-ESCALADO-2026-08-29.md) is the scaling plan written while
  still chasing a medal, before the private reveal; its levers are listed ranked and, in
  hindsight, aimed at the public guardrail that did not decide the medal.
- [`HALLAZGO-GEMMA.md`](HALLAZGO-GEMMA.md) is an earlier hypothesis (25 August) that the next
  jump lay in the second target model; `HALLAZGO-2026-08-27.md` refutes it with measurements
  and supersedes it.

[`SUBMIT.md`](SUBMIT.md) is the submission-process checklist (Kaggle CLI, the gated submission
flow and what each submission scored).

The work was done with an AI coding assistant (Claude); the notes are first-person planning and
measurement logs. They repeatedly flagged, from the first day, the one risk that materialised:
if the hidden private guardrail inspected the payload, every submission's private score would
collapse to zero regardless of public standing. It did.

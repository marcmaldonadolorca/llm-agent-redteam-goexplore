# What the evaluation really measured, and why the public score was a mirage

English summary of [`internal/HALLAZGO-2026-08-27.md`](internal/HALLAZGO-2026-08-27.md), the
running log (in Spanish) kept from 27 August to the result on 2 September 2026. It is the
document behind the thesis of this repository. Every number below is a **public leaderboard**
score; every private score was 0.

## 1. Scoring reconstructed from source, not guessed

The competition's evaluation gateway and `aicomp_sdk` 3.1.2 were downloaded and read in full.
The score of a submission is a deterministic function of the evaluation code: it rewards the
count of successful tool calls that satisfy the scored predicate, plus a bonus per distinct
scored cell, normalised and capped. Reading this from `scoring.py` and `predicates.py` (rather
than from the write-up) corrected several earlier assumptions, including the identity of the
second target model and whether the public score was a sum or a mean of the per-model rows.
The practical consequence was that progress came from throughput of valid tool calls under a
time budget, not from more elaborate prompts; several more elaborate ideas were measured and
regressed.

## 2. The public board rewarded the wrong thing

The public and private leaderboards differ by **guardrail**, not by data: the same submission
is scored against a documented, auditable public guardrail and, separately, against a hidden
private one. The technique that everyone converged on scored high on the public board and
**zero against the private guardrail**, which blocked that route. The public board was not a
representative sample of the private one.

## 3. The honest result

The submission climbed the public board over a few days (from the low tens to **91.0**, around
top 10% public), but **the private score was 0 on every submission; final rank 3,985 of 4,186**.
The teams that medalled had an attack robust to the hidden guardrail — something not present in
any public notebook — so a strategy of reproducing and tuning the public-board technique had a
structural ceiling of zero on private, impossible to know before the reveal.

## 4. The lesson carried forward

In a security competition with a hidden private guardrail, the public leaderboard does not
predict the medal; it is itself part of the game. The budget should have been spent probing
robustness off the path everyone else was reproducing, rather than hardening a technique that
the public board already rewarded. This is why the finding is documented even though it won no
medal: the methodology (scoring reconstructed from the SDK's own code) is sound and
reproducible, and the failure is a reusable lesson rather than a result to showcase.

The scaling plan written before the private reveal is in
[`internal/PLAN-ESCALADO-2026-08-29.md`](internal/PLAN-ESCALADO-2026-08-29.md); the full
derivation and the per-day log are in [`internal/`](internal/).

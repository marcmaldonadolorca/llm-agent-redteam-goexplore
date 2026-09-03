# Plan de escalado — de 90.035 hacia plata/oro

Estado: **90.035** (borde del bronce). Técnica: live-fill + harmony-frame + multipost(8) en
gpt_oss + fill agresivo (config evgendvorkin). Fuente: research de 9 notebooks + workflow
`jed-scaling-plan` (mina de optimizaciones) + verificación en el SDK.

## Escalera de medallas (leaderboard 4158 equipos)
| Medalla | Puesto | Score | Gap desde 90.035 |
|---|---|---|---|
| **Bronce** | top 415 | 90.305 | +0,27 (¡ya casi!) |
| **Plata** | top 207 | 93.255 | +3,2 |
| **Oro** | top 18 | 120.595 | +30,6 (muro) |

## Árbol de decisión según el bracket (moderado 55854221 aún en cola)
- **conservador (cushion 1.35) = 81.28 · agresivo (1.005) = 90.035**, sin void → el cushion mínimo
  es terreno seguro. El moderado (1.10) caerá en medio (~86-88), confirmando la curva.
- **Cruzar 90.3 y apuntar a 93.3:** el fill ya está al ~100% (no hay más ahí). Los levers reales
  quedan abajo.

## Levers de escalado, RANKEADOS (verificados)
1. **[EL LEVER] Multipost en la fila de GEMMA — subir la fila baja de la media.** La LB pública =
   MEAN(gpt_oss_row, gemma_row). gpt_oss ya hace **8× http.post/candidato** (128 raw/fila) vía el
   plan harmony forjado (`_forge_plan_msg`); gemma va **single-post** (16 raw/fila) porque no parsea
   tokens harmony. La media la arrastra la fila más baja. **Si gemma encadena N posts/candidato, su
   fila ×N y la media salta ~90→100+ (plata/oro).** UNTESTED — es el experimento clave (diagnóstico
   `jed-attack-diagnose` v5, en marcha). Mi diag previo mostró gemma haciendo 1 post con mensaje
   plano; hay que probar formato nativo gemma-4 (`<|tool_call>call:http.post{...}<tool_call|>`
   encadenado) o un plan pre-forjado en su plantilla.
2. **REPLAY_SAFE_SIZING=False + FILL_BUDGET_FRAC=0.99999** (evgendvorkin real; nuestro 90.035 usó
   REPLAY_SAFE_SIZING=True). Gasta el 100% del budget de generación sin reservar para replay →
   +candidatos. **Void ALTO** si el tiempo de replay cuenta hacia el deadline 8930s. Probar con red
   (el 90.035 queda de failsafe). +varios puntos si no voidea.
3. **Tuning de `SLOW_MULTIPOST_N`** (probar 6 vs 8): con 8 hops el modelo puede saturar y completar
   <8 posts; 6 podría dar mayor tasa de completado → más K efectivo. Marginal.
4. **Reutilizar el candidato de warmup** (+1 fila, +0.09). Trivial.

## Levers DESCARTADOS (verificados muertos)
- **DESTRUCTIVE_WRITE** (multi-predicado exfil+fs.delete de dimong4): solo dispara sobre `secret.txt`
  (bloqueado). No suma. MUERTO.
- **CONFUSED_DEPUTY** (email.send): alcanzable pero peso 4 vs 16 de http.post; con 8 hops, http.post
  puro domina. No escala.
- **Multi-mensaje** (attack_v3): refutado (28.5/ERROR).
- **Cerrar gemma para "sumar"**: refutado (ya cumple; la LB es media, no suma).

## Secuencia de ejecución (envíos ~24 h de cola, 5/día, deadline 1-sep)
1. **Diagnóstico gemma-multipost** (sin gastar envío): ¿encadena gemma? Formatos a probar: nativo
   gemma-4 secuencial, plan pre-forjado en su chat-template, instrucción numerada explícita.
2. Si gemma encadena → attack con multipost en AMBAS filas → esperado ~100+ (plata, quizá oro).
3. Si NO → estamos cerca del techo de la técnica pública (~90-93); afinar fill/sizing (lever 2-3)
   para asegurar plata, y el oro queda como stretch (probablemente exige un edge no publicado).
4. Cada envío: una variante; bracketeo y me quedo con la mejor. Failsafes: 41.28 · 81.28 · 90.035.

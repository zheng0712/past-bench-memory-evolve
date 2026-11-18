# 逐 episode 结果 t2

共 32 行（with/without 两个变体分别计数，含 reflection 等无评分阶段）。

| run | variant | task_id | bucket | score | passed | hard | judge | content | turns | wall_s | tokens |
|---|---|---|---|---:|---|---|---:|---:|---:|---:|---:|
| 20261118_sm01_hermes_smoke | with_persistence | SM01_COLD_001 | baseline | 0.600 | 否 | 否 | 1.000 | 0.000 | 1 | 28.1 | 18212 |
| 20261118_sm01_hermes_smoke | with_persistence | SM01_LEARN_A_001 | learn | 0.760 | 否 | 否 | 1.000 | 0.000 | 1 | 36.4 | 31094 |
| 20261118_sm01_hermes_smoke | with_persistence | SM01_LEARN_B_001 | learn | 0.760 | 否 | 否 | 0.900 | 0.000 | 1 | 18.7 | 17721 |
| 20261118_sm01_hermes_smoke | with_persistence | SM01_LEARN_B_001_REFLECT | reflection | 0.000 | 否 | - | - | - | 1 | 15.1 | 4407 |
| 20261118_sm01_hermes_smoke | with_persistence | SM01_EVAL_NEAR_001 | evaluation | 1.000 | 是 | 是 | 1.000 | 1.000 | 1 | 21.2 | 17937 |
| 20261118_sm01_hermes_smoke | with_persistence | SM01_EVAL_FAR_001 | evaluation | 1.000 | 是 | 是 | 1.000 | 1.000 | 1 | 22.6 | 18277 |
| 20261118_sm01_hermes_smoke | with_persistence | SM01_CONTROL_002 | control | 0.600 | 否 | 否 | 1.000 | 0.000 | 1 | 29.9 | 24135 |
| 20261118_sm01_hermes_smoke | with_persistence | SM01_CONTROL_001 | control | 0.600 | 否 | 否 | 0.300 | 0.000 | 1 | 20.2 | 17527 |
| 20261118_sm01_hermes_smoke | with_persistence | SM01_CONTROL_003 | control | 0.600 | 否 | 否 | 0.950 | 0.000 | 1 | 22.9 | 14162 |
| 20261118_sm01_hermes_smoke | without_persistence | SM01_COLD_001 | baseline | 0.600 | 否 | 否 | 1.000 | 0.000 | 1 | 28.1 | 18212 |
| 20261118_sm01_hermes_smoke | without_persistence | SM01_LEARN_A_001 | learn | 0.560 | 否 | 否 | 1.000 | 0.000 | 1 | 28.1 | 19796 |
| 20261118_sm01_hermes_smoke | without_persistence | SM01_LEARN_B_001 | learn | 0.600 | 否 | 否 | 0.500 | 0.000 | 1 | 19.3 | 13903 |
| 20261118_sm01_hermes_smoke | without_persistence | SM01_LEARN_B_001_REFLECT | reflection | 0.000 | 否 | - | - | - | 1 | 24.7 | 8074 |
| 20261118_sm01_hermes_smoke | without_persistence | SM01_EVAL_NEAR_001 | evaluation | 0.400 | 否 | 否 | 0.300 | 0.000 | 1 | 18.3 | 13810 |
| 20261118_sm01_hermes_smoke | without_persistence | SM01_EVAL_FAR_001 | evaluation | 0.400 | 否 | 否 | 1.000 | 0.000 | 1 | 24.7 | 14146 |
| 20261118_sm01_hermes_smoke | without_persistence | SM01_CONTROL_002 | control | 0.600 | 否 | 否 | 1.000 | 0.000 | 1 | 29.0 | 15508 |
| 20261118_sm01_hermes_smoke | without_persistence | SM01_CONTROL_001 | control | 1.000 | 是 | 是 | 1.000 | 1.000 | 1 | 23.7 | 14570 |
| 20261118_sm01_hermes_smoke | without_persistence | SM01_CONTROL_003 | control | 0.600 | 否 | 否 | 1.000 | 0.000 | 1 | 18.7 | 13884 |
| 20261118_sm03_hermes_smoke | with_persistence | SM03_COLD_001 | baseline | 0.600 | 否 | 否 | 0.000 | 0.000 | 1 | 19.1 | 18635 |
| 20261118_sm03_hermes_smoke | with_persistence | SM03_UPDATE_001 | learn | 1.000 | 是 | 是 | 1.000 | 1.000 | 1 | 40.3 | 33343 |
| 20261118_sm03_hermes_smoke | with_persistence | SM03_EVAL_NEAR_001 | evaluation | 1.000 | 是 | 是 | 1.000 | 1.000 | 1 | 17.6 | 18487 |
| 20261118_sm03_hermes_smoke | with_persistence | SM03_EVAL_FAR_001 | evaluation | 1.000 | 是 | 是 | 0.700 | 1.000 | 1 | 21.2 | 19086 |
| 20261118_sm03_hermes_smoke | with_persistence | SM03_CONTROL_003 | control | 0.600 | 否 | 否 | 0.800 | 0.000 | 1 | 59.0 | 72765 |
| 20261118_sm03_hermes_smoke | with_persistence | SM03_CONTROL_002 | control | 1.000 | 是 | 是 | 1.000 | 1.000 | 1 | 19.5 | 17601 |
| 20261118_sm03_hermes_smoke | with_persistence | SM03_CONTROL_001 | control | 1.000 | 是 | 是 | 1.000 | 1.000 | 1 | 18.0 | 17287 |
| 20261118_sm03_hermes_smoke | without_persistence | SM03_COLD_001 | baseline | 0.600 | 否 | 否 | 0.300 | 0.000 | 1 | 210.2 | 538160 |
| 20261118_sm03_hermes_smoke | without_persistence | SM03_UPDATE_001 | learn | 0.560 | 否 | 否 | 1.000 | 1.000 | 1 | 21.9 | 14737 |
| 20261118_sm03_hermes_smoke | without_persistence | SM03_EVAL_NEAR_001 | evaluation | 0.704 | 否 | 否 | 0.500 | 0.000 | 1 | 54.8 | 45960 |
| 20261118_sm03_hermes_smoke | without_persistence | SM03_EVAL_FAR_001 | evaluation | 0.704 | 否 | 否 | 0.350 | 0.000 | 1 | 240.5 | 557953 |
| 20261118_sm03_hermes_smoke | without_persistence | SM03_CONTROL_003 | control | 0.600 | 否 | 否 | 0.900 | 0.000 | 1 | 82.2 | 55493 |
| 20261118_sm03_hermes_smoke | without_persistence | SM03_CONTROL_002 | control | 1.000 | 是 | 是 | 1.000 | 1.000 | 1 | 24.7 | 18689 |
| 20261118_sm03_hermes_smoke | without_persistence | SM03_CONTROL_001 | control | 1.000 | 是 | 是 | 1.000 | 1.000 | 1 | 23.4 | 18456 |

# PAST-Bench 基线实验报告（SM01 / SM03）

生成时间：2026-11-19 13:06（Asia/Shanghai）

## 0. 实验配置

- 数据集：`PAST-Bench/self-evolve-tasks-v2`，commit `f822351`
- family：`memory_ability/SM01_preference_adoption`、`update_ability/SM03_fact_correction`
- agent：`hermes`；profile：`qwen`；model：`qwen3.5-plus`
- judge：`qwen3.5-plus`（与 agent 同模型；judge_score 只写入 communication，不进入 task_score）
- runtime：`local`；`--sandbox --sandbox-tools`；`--compare-no-persistence`
- 有效 run：SM01 3 个（smoke / run2 / run3），SM03 3 个（smoke / run4 / run5）

有效 run 的判定：with/without 两个变体都无空响应、无 infra_blocked、无 403；两个变体都完整产出 7 或 8 个任务（SM01 另含 1 个 reflection 记录）。

## 1. 有效实验表

### 1.1 有效 run 判定

| run | family | W 空响应 | WO 空响应 | W 任务数 | WO 任务数 | 403 | 结论 |
|---|---|---:|---:|---:|---:|---|---|
| 20261118_sm01_hermes_smoke | SM01_preference_adoption | 0 | 0 | 9 | 9 | 否 | 有效 |
| 20261119_sm01_run2 | SM01_preference_adoption | 0 | 0 | 9 | 9 | 否 | 有效 |
| 20261119_sm01_run3 | SM01_preference_adoption | 0 | 0 | 9 | 9 | 否 | 有效 |
| 20261118_sm03_hermes_smoke | SM03_fact_correction | 0 | 0 | 7 | 7 | 否 | 有效 |
| 20261119_sm03_run2 | SM03_fact_correction | 0 | 5 | 7 | 7 | 否 | 无效 |
| 20261119_sm03_run3 | SM03_fact_correction | 7 | 7 | 7 | 7 | 是 | 无效 |
| 20261119_sm03_run4 | SM03_fact_correction | 0 | 0 | 7 | 7 | 否 | 有效 |
| 20261119_sm03_run5 | SM03_fact_correction | 0 | 0 | 7 | 7 | 否 | 有效 |

### 1.2 family 级实验表（仅有效 run）

| run | var | n | baseline | eval | eval_pass | delta(eval-base) | write | recall | update | retention | pollution | mechanism | evolve | paired_delta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20261118_sm01_hermes_smoke | W | 9 | 0.600 | 1.000 | 1.000 | 0.400 | 1.000 | 1.000 | 0.833 | 1.000 | 0.000 | 0.967 | 0.387 | 0.600 |
| 20261118_sm01_hermes_smoke | WO | 9 | 0.600 | 0.400 | 0.000 | -0.200 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.400 | 0.000 | - |
| 20261119_sm01_run2 | W | 9 | 0.600 | 0.852 | 0.500 | 0.252 | 1.000 | 0.500 | 0.833 | 1.000 | 0.000 | 0.867 | 0.218 | 0.452 |
| 20261119_sm01_run2 | WO | 9 | 0.600 | 0.400 | 0.000 | -0.200 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.400 | 0.000 | - |
| 20261119_sm01_run3 | W | 9 | 0.600 | 0.704 | 0.000 | 0.104 | 1.000 | 0.000 | 0.500 | 1.000 | 0.000 | 0.700 | 0.073 | 0.304 |
| 20261119_sm01_run3 | WO | 9 | 0.600 | 0.400 | 0.000 | -0.200 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.400 | 0.000 | - |
| 20261118_sm03_hermes_smoke | W | 7 | 0.600 | 1.000 | 1.000 | 0.400 | 0.833 | 1.000 | 1.000 | 1.000 | 0.500 | 0.867 | 0.347 | 0.296 |
| 20261118_sm03_hermes_smoke | WO | 7 | 0.600 | 0.704 | 0.000 | 0.104 | 0.333 | 0.000 | 0.500 | 1.000 | 0.000 | 0.567 | 0.059 | - |
| 20261119_sm03_run4 | W | 7 | 0.600 | 1.000 | 1.000 | 0.400 | 0.833 | 1.000 | 1.000 | 1.000 | 0.000 | 0.967 | 0.387 | 0.296 |
| 20261119_sm03_run4 | WO | 7 | 0.600 | 0.704 | 0.000 | 0.104 | 0.333 | 0.000 | 0.500 | 1.000 | 0.000 | 0.567 | 0.059 | - |
| 20261119_sm03_run5 | W | 7 | 0.600 | 1.000 | 1.000 | 0.400 | 0.833 | 1.000 | 1.000 | 1.000 | 0.000 | 0.967 | 0.387 | 0.296 |
| 20261119_sm03_run5 | WO | 7 | 0.600 | 0.704 | 0.000 | 0.104 | 0.333 | 0.000 | 0.500 | 1.000 | 0.000 | 0.567 | 0.059 | - |

### 1.3 SM01 有效 run 逐 episode

| run | var | task | bucket | stage | score | g | c | s | slot | pass | judge | mw | inj | used | aq | rule_q | wall_s | out_tok | chars | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20261118_sm01_hermes_smoke | W | SM01_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 28.1 | 1014 | 519 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_LEARN_A_001 | learn | learn_a | 0.760 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 1 | 0 | False | 1.000 | 1.000 | 36.4 | 2082 | 711 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_LEARN_B_001 | learn | learn_b | 0.760 | 1.000 | 0.000 | 1.000 | - | False | 0.900 | 0 | 1 | True | 1.000 | 1.000 | 18.7 | 774 | 476 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_LEARN_B_001_REFLECT | reflection | reflection | 0.000 | - | - | - | - | - | - | 0 | - | - | - | - | 15.1 | 742 | 335 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_EVAL_NEAR_001 | evaluation | eval_near | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 21.2 | 945 | 380 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_EVAL_FAR_001 | evaluation | eval_far | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 22.6 | 1132 | 400 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_CONTROL_002 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 29.9 | 1588 | 607 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_CONTROL_001 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 0.300 | 0 | 0 | False | 0.000 | 0.000 | 20.2 | 902 | 571 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 0.950 | 0 | 0 | False | 0.000 | 0.000 | 22.9 | 890 | 478 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 28.1 | 1014 | 519 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_LEARN_A_001 | learn | learn_a | 0.560 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 28.1 | 1460 | 587 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_LEARN_B_001 | learn | learn_b | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 0.500 | 0 | 0 | False | 0.000 | 0.000 | 19.3 | 855 | 572 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_LEARN_B_001_REFLECT | reflection | reflection | 0.000 | - | - | - | - | - | - | 0 | - | - | - | - | 24.7 | 1440 | 749 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_EVAL_NEAR_001 | evaluation | eval_near | 0.400 | 1.000 | 0.000 | 1.000 | - | False | 0.300 | 0 | 0 | False | 0.000 | 0.000 | 18.3 | 768 | 403 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_EVAL_FAR_001 | evaluation | eval_far | 0.400 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 24.7 | 940 | 559 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_CONTROL_002 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 29.0 | 1558 | 595 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 23.7 | 1191 | 399 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 18.7 | 789 | 494 | ok |
| 20261119_sm01_run2 | W | SM01_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 26.2 | 1262 | 606 | ok |
| 20261119_sm01_run2 | W | SM01_LEARN_A_001 | learn | learn_a | 0.760 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 1 | 0 | False | 1.000 | 1.000 | 32.6 | 1774 | 838 | ok |
| 20261119_sm01_run2 | W | SM01_LEARN_B_001 | learn | learn_b | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 20.5 | 882 | 378 | ok |
| 20261119_sm01_run2 | W | SM01_LEARN_B_001_REFLECT | reflection | reflection | 0.000 | - | - | - | - | - | - | 0 | - | - | - | - | 12.6 | 553 | 311 | ok |
| 20261119_sm01_run2 | W | SM01_EVAL_NEAR_001 | evaluation | eval_near | 0.704 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 20.8 | 919 | 541 | ok |
| 20261119_sm01_run2 | W | SM01_EVAL_FAR_001 | evaluation | eval_far | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 22.4 | 1097 | 412 | ok |
| 20261119_sm01_run2 | W | SM01_CONTROL_002 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 29.0 | 1562 | 615 | ok |
| 20261119_sm01_run2 | W | SM01_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 22.5 | 1105 | 399 | ok |
| 20261119_sm01_run2 | W | SM01_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 20.6 | 882 | 468 | ok |
| 20261119_sm01_run2 | WO | SM01_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 26.2 | 1262 | 606 | ok |
| 20261119_sm01_run2 | WO | SM01_LEARN_A_001 | learn | learn_a | 0.560 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 31.8 | 1667 | 803 | ok |
| 20261119_sm01_run2 | WO | SM01_LEARN_B_001 | learn | learn_b | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 0.700 | 0 | 0 | False | 0.000 | 0.000 | 19.9 | 899 | 574 | ok |
| 20261119_sm01_run2 | WO | SM01_LEARN_B_001_REFLECT | reflection | reflection | 0.000 | - | - | - | - | - | - | 0 | - | - | - | - | 31.0 | 1485 | 704 | ok |
| 20261119_sm01_run2 | WO | SM01_EVAL_NEAR_001 | evaluation | eval_near | 0.400 | 1.000 | 0.000 | 1.000 | - | False | 0.250 | 0 | 0 | False | 0.000 | 0.000 | 19.3 | 832 | 388 | ok |
| 20261119_sm01_run2 | WO | SM01_EVAL_FAR_001 | evaluation | eval_far | 0.400 | 1.000 | 0.000 | 1.000 | - | False | 0.900 | 0 | 0 | False | 0.000 | 0.000 | 20.5 | 941 | 509 | ok |
| 20261119_sm01_run2 | WO | SM01_CONTROL_002 | control | control | 0.800 | 1.000 | 0.500 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 33.0 | 1759 | 633 | ok |
| 20261119_sm01_run2 | WO | SM01_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 23.7 | 1201 | 411 | ok |
| 20261119_sm01_run2 | WO | SM01_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 19.2 | 800 | 412 | ok |
| 20261119_sm01_run3 | W | SM01_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 18.7 | 762 | 535 | ok |
| 20261119_sm01_run3 | W | SM01_LEARN_A_001 | learn | learn_a | 0.760 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 1 | 0 | False | 1.000 | 1.000 | 35.5 | 1997 | 692 | ok |
| 20261119_sm01_run3 | W | SM01_LEARN_B_001 | learn | learn_b | 0.760 | 1.000 | 0.000 | 1.000 | - | False | 0.500 | 0 | 1 | True | 1.000 | 1.000 | 18.5 | 731 | 436 | ok |
| 20261119_sm01_run3 | W | SM01_LEARN_B_001_REFLECT | reflection | reflection | 0.000 | - | - | - | - | - | - | 0 | - | - | - | - | 15.9 | 768 | 716 | ok |
| 20261119_sm01_run3 | W | SM01_EVAL_NEAR_001 | evaluation | eval_near | 0.704 | 1.000 | 0.000 | 1.000 | - | False | 0.500 | 0 | 1 | True | 1.000 | 1.000 | 18.8 | 789 | 506 | ok |
| 20261119_sm01_run3 | W | SM01_EVAL_FAR_001 | evaluation | eval_far | 0.704 | 1.000 | 0.000 | 1.000 | - | False | 0.700 | 0 | 1 | True | 1.000 | 1.000 | 20.1 | 878 | 536 | ok |
| 20261119_sm01_run3 | W | SM01_CONTROL_002 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 26.2 | 1315 | 402 | ok |
| 20261119_sm01_run3 | W | SM01_CONTROL_001 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 0.500 | 0 | 0 | False | 0.000 | 0.000 | 18.9 | 792 | 499 | ok |
| 20261119_sm01_run3 | W | SM01_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 21.0 | 853 | 445 | ok |
| 20261119_sm01_run3 | WO | SM01_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 18.7 | 762 | 535 | ok |
| 20261119_sm01_run3 | WO | SM01_LEARN_A_001 | learn | learn_a | 0.560 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 29.0 | 1491 | 752 | ok |
| 20261119_sm01_run3 | WO | SM01_LEARN_B_001 | learn | learn_b | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 0.500 | 0 | 0 | False | 0.000 | 0.000 | 19.5 | 843 | 493 | ok |
| 20261119_sm01_run3 | WO | SM01_LEARN_B_001_REFLECT | reflection | reflection | 0.000 | - | - | - | - | - | - | 0 | - | - | - | - | 22.4 | 1120 | 613 | ok |
| 20261119_sm01_run3 | WO | SM01_EVAL_NEAR_001 | evaluation | eval_near | 0.400 | 1.000 | 0.000 | 1.000 | - | False | 0.300 | 0 | 0 | False | 0.000 | 0.000 | 20.0 | 895 | 488 | ok |
| 20261119_sm01_run3 | WO | SM01_EVAL_FAR_001 | evaluation | eval_far | 0.400 | 1.000 | 0.000 | 1.000 | - | False | 0.700 | 0 | 0 | False | 0.000 | 0.000 | 20.2 | 925 | 560 | ok |
| 20261119_sm01_run3 | WO | SM01_CONTROL_002 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 24.6 | 1134 | 398 | ok |
| 20261119_sm01_run3 | WO | SM01_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 31.4 | 1184 | 411 | ok |
| 20261119_sm01_run3 | WO | SM01_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 0.900 | 0 | 0 | False | 0.000 | 0.000 | 19.9 | 884 | 468 | ok |

### 1.4 SM03 有效 run 逐 episode

| run | var | task | bucket | stage | score | g | c | s | slot | pass | judge | mw | inj | used | aq | rule_q | wall_s | out_tok | chars | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20261118_sm03_hermes_smoke | W | SM03_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.000 | 0 | 1 | True | 0.000 | 0.000 | 19.1 | 771 | 294 | ok |
| 20261118_sm03_hermes_smoke | W | SM03_UPDATE_001 | learn | update | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 6 | 1 | True | 0.833 | 0.667 | 40.3 | 2071 | 683 | ok |
| 20261118_sm03_hermes_smoke | W | SM03_EVAL_NEAR_001 | evaluation | eval_near | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 17.6 | 651 | 380 | ok |
| 20261118_sm03_hermes_smoke | W | SM03_EVAL_FAR_001 | evaluation | eval_far | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 0.700 | 0 | 1 | True | 1.000 | 1.000 | 21.2 | 969 | 343 | ok |
| 20261118_sm03_hermes_smoke | W | SM03_CONTROL_002 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 19.5 | 836 | 379 | ok |
| 20261118_sm03_hermes_smoke | W | SM03_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 18.0 | 657 | 334 | ok |
| 20261118_sm03_hermes_smoke | W | SM03_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.800 | 0 | 0 | False | 0.000 | 0.000 | 59.0 | 3256 | 564 | ok |
| 20261118_sm03_hermes_smoke | WO | SM03_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.300 | 0 | 1 | True | 0.000 | 0.000 | 210.2 | 6722 | 722 | slow>200s |
| 20261118_sm03_hermes_smoke | WO | SM03_UPDATE_001 | learn | update | 0.560 | 1.000 | 1.000 | 1.000 | 1.000 | False | 1.000 | 0 | 1 | True | 0.333 | 0.667 | 21.9 | 988 | 641 | ok |
| 20261118_sm03_hermes_smoke | WO | SM03_EVAL_NEAR_001 | evaluation | eval_near | 0.704 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.500 | 0 | 1 | True | 1.000 | 1.000 | 54.8 | 3325 | 685 | ok |
| 20261118_sm03_hermes_smoke | WO | SM03_EVAL_FAR_001 | evaluation | eval_far | 0.704 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.350 | 0 | 1 | True | 1.000 | 1.000 | 240.5 | 10928 | 868 | slow>200s |
| 20261118_sm03_hermes_smoke | WO | SM03_CONTROL_002 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 24.7 | 1226 | 567 | ok |
| 20261118_sm03_hermes_smoke | WO | SM03_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 23.4 | 1120 | 550 | ok |
| 20261118_sm03_hermes_smoke | WO | SM03_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.900 | 0 | 0 | False | 0.000 | 0.000 | 82.2 | 2894 | 727 | ok |
| 20261119_sm03_run4 | W | SM03_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.000 | 0 | 1 | True | 0.000 | 0.000 | 18.5 | 658 | 339 | ok |
| 20261119_sm03_run4 | W | SM03_UPDATE_001 | learn | update | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 1 | 1 | True | 0.833 | 0.667 | 30.4 | 1587 | 653 | ok |
| 20261119_sm03_run4 | W | SM03_EVAL_NEAR_001 | evaluation | eval_near | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 18.5 | 774 | 366 | ok |
| 20261119_sm03_run4 | W | SM03_EVAL_FAR_001 | evaluation | eval_far | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 0.900 | 0 | 1 | True | 1.000 | 1.000 | 18.9 | 799 | 452 | ok |
| 20261119_sm03_run4 | W | SM03_CONTROL_002 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 19.8 | 798 | 416 | ok |
| 20261119_sm03_run4 | W | SM03_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 17.2 | 669 | 341 | ok |
| 20261119_sm03_run4 | W | SM03_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.750 | 0 | 0 | False | 0.000 | 0.000 | 42.1 | 2026 | 556 | ok |
| 20261119_sm03_run4 | WO | SM03_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.200 | 0 | 1 | True | 0.000 | 0.000 | 72.3 | 4411 | 452 | ok |
| 20261119_sm03_run4 | WO | SM03_UPDATE_001 | learn | update | 0.560 | 1.000 | 1.000 | 1.000 | 1.000 | False | 1.000 | 0 | 1 | True | 0.333 | 0.667 | 36.9 | 1056 | 544 | ok |
| 20261119_sm03_run4 | WO | SM03_EVAL_NEAR_001 | evaluation | eval_near | 0.704 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.600 | 0 | 1 | True | 1.000 | 1.000 | 294.3 | 12780 | 757 | slow>200s |
| 20261119_sm03_run4 | WO | SM03_EVAL_FAR_001 | evaluation | eval_far | 0.704 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.400 | 0 | 1 | True | 1.000 | 1.000 | 188.9 | 10080 | 543 | ok |
| 20261119_sm03_run4 | WO | SM03_CONTROL_002 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 54.3 | 1171 | 440 | ok |
| 20261119_sm03_run4 | WO | SM03_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 24.0 | 1172 | 569 | ok |
| 20261119_sm03_run4 | WO | SM03_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.750 | 0 | 0 | False | 0.000 | 0.000 | 47.2 | 2390 | 661 | ok |
| 20261119_sm03_run5 | W | SM03_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.000 | 0 | 1 | True | 0.000 | 0.000 | 18.6 | 713 | 277 | ok |
| 20261119_sm03_run5 | W | SM03_UPDATE_001 | learn | update | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 1 | 1 | True | 0.833 | 0.667 | 26.2 | 1338 | 691 | ok |
| 20261119_sm03_run5 | W | SM03_EVAL_NEAR_001 | evaluation | eval_near | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 48.1 | 726 | 379 | ok |
| 20261119_sm03_run5 | W | SM03_EVAL_FAR_001 | evaluation | eval_far | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 0.900 | 0 | 1 | True | 1.000 | 1.000 | 116.1 | 801 | 373 | ok |
| 20261119_sm03_run5 | W | SM03_CONTROL_002 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 21.9 | 871 | 385 | ok |
| 20261119_sm03_run5 | W | SM03_CONTROL_001 | control | control | 0.760 | 1.000 | 1.000 | 0.000 | 1.000 | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 20.5 | 766 | 396 | ok |
| 20261119_sm03_run5 | W | SM03_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.700 | 0 | 0 | False | 0.000 | 0.000 | 35.2 | 1846 | 654 | ok |
| 20261119_sm03_run5 | WO | SM03_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.100 | 0 | 1 | True | 0.000 | 0.000 | 155.5 | 5619 | 590 | ok |
| 20261119_sm03_run5 | WO | SM03_UPDATE_001 | learn | update | 0.560 | 1.000 | 1.000 | 1.000 | 1.000 | False | 1.000 | 0 | 1 | True | 0.333 | 0.667 | 24.8 | 1220 | 503 | ok |
| 20261119_sm03_run5 | WO | SM03_EVAL_NEAR_001 | evaluation | eval_near | 0.704 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.400 | 0 | 1 | True | 1.000 | 1.000 | 112.6 | 5213 | 694 | ok |
| 20261119_sm03_run5 | WO | SM03_EVAL_FAR_001 | evaluation | eval_far | 0.704 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.500 | 0 | 1 | True | 1.000 | 1.000 | 459.7 | 10420 | 416 | slow>200s |
| 20261119_sm03_run5 | WO | SM03_CONTROL_002 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 26.9 | 1244 | 518 | ok |
| 20261119_sm03_run5 | WO | SM03_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 23.7 | 1087 | 536 | ok |
| 20261119_sm03_run5 | WO | SM03_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.800 | 0 | 0 | False | 0.000 | 0.000 | 121.1 | 3351 | 639 | ok |

### 1.5 有效 run 稳定性

| family | runs | with eval | without eval | paired delta | with pass | without pass | with mechanism | with evolve | without evolve |
|---|---|---|---|---|---|---|---|---|---|
| SM01_preference_adoption | 3 | 0.852 ± 0.148 | 0.400 ± 0.000 | 0.452 ± 0.148 | 0.500 ± 0.500 | 0.000 ± 0.000 | 0.844 ± 0.135 | 0.226 ± 0.157 | 0.000 ± 0.000 |
| SM03_fact_correction | 3 | 1.000 ± 0.000 | 0.704 ± 0.000 | 0.296 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.933 ± 0.058 | 0.373 ± 0.023 | 0.059 ± 0.000 |

## 2. 问题台账

本节把所有问题按同一模板记录，避免只把某一类问题当“大问题”。频率分母：SM01 有效 run 为 3×2×8=48 条非空记录；SM03 有效 run 为 3×2×7=42 条记录；全量额外包含 run2/run3 的无效记录，共 118 条非 reflection 记录。

| ID | 类别 | 问题 | 范围 | 频率 | 原文依据 | 影响 | 性质 | 处理建议 |
|---|---|---|---|---|---|---|---|---|
| ISS-01 | 任务表述/模型行为 | SM01 最终回复没有 TSV 原文 | SM01 全部任务 | 39/48（81.3%）；其中纯格式失败 6/48 | `require_tsv_output=true`；grader 只检查最终文本的 4 列 Tab 行 | `content=0`；`0.704` 而非 `1.0`；`pass=0` | 非预期缺陷 + 任务表述歧义 | 在 prompt 明确“最终回复正文输出 TSV”，或让 grader 接受 artifact；需上游决策 |
| ISS-02 | 模型行为 | SM01 LEARN_A 写入成功但不应用 | SM01_LEARN_A_001 | 3/3 with（100%） | `min_memory_calls=1`、`require_rule_artifact`；`memory_write=1`、`rule_q=1.0` | `content=0`；`0.760` | 非预期缺陷 | 与 ISS-01 同源；先修 ISS-01 |
| ISS-03 | 控制组 | SM01 shortcut control 未达 1.0 | SM01_CONTROL_002 | 6/6（0.6×5、0.8×1） | `family.yaml`：shortcut-only control locally solvable | 控制组失效；无法证明“规则可见即可解” | 非预期缺陷 | 与 ISS-01 同源；修 ISS-01 后复测 |
| ISS-04 | 任务表述/预期基线 | SM01 COLD content=0 | SM01_COLD_001 | 6/6 | cold prompt 不教 TSV；`cold_design` 要求默认格式；但 `require_tsv_output=true` | `0.600`，符合 cold 设计 | 预期基线 + 表述冲突 | 不改；报告注明 |
| ISS-05 | 预期基线 | SM03 WO eval content=0 | SM03_EVAL_NEAR/FAR | 6/6 | 无纠正记忆；`evaluation_only=true` | `0.704`（artifact 加分） | 预期基线 | 不改；报告注明 |
| ISS-06 | 预期基线 | SM03 WO UPDATE 0.560 | SM03_UPDATE_001 | 3/3 | `min_memory_calls=1`；`missing_learning_cap=0.45` | `0.560`，但 `content=1.0` | 预期基线 | 不改；报告注明 |
| ISS-07 | 控制组 | SM03 CTRL_001 发给了 forbidden recipient | SM03_CONTROL_001 | 1/6（run5 with） | `forbidden_recipients=["Marta Hill"]` | `share=0`；`0.760`；`pass=0` | 非预期缺陷 | 记录；可复测 |
| ISS-08 | 执行基础设施 | SM03 403/空响应 | run2 WO、run3 W/WO | 19/28（67.9%）；全量 19/118（16.1%） | `errors.log` 403 `AccessDenied.Unpurchased`；`(no response)` | 该 run 作废；不进入有效均值 | 执行故障 | 已剔除；run4/run5 已有效；后续加前置探测 |
| ISS-09 | 执行基础设施 | 慢 episode `wall>200s` | 全量 | 6/118（5.1%）；有效 4/90（4.4%） | `wall_time_s`；全部完成并打分 | 不改变 `task_score` | 耗时注释，不是失败 | 报告标注；脚本已改为 `slow_gt_200s` |
| ISS-10 | 数据集编排 | `learn_a_seed_stale_fact` 未调度 | SM03 | 1 个目录 | `family.yaml` 的 `episode_order` 不含；`total_episodes=7` | 不影响运行；只是冗余任务 | 数据集遗留 | 不改；记录 |
| ISS-11 | 设计口径 | SM03 WO 仍注入 stale 记忆与诱饵 | SM03 全部 WO | 6/6 WO eval 记录 | `memory_injection_count=1`；`memory_text` 含 `2026-06-14` + marketing/Orion `2026-06-16` | WO 不是零记忆对照；`0.704` 可解释 | 设计口径 | 报告明确写作“stale-memory only” |
| ISS-12 | 评判器 | judge 波动/失败 | 全量 | t3 `judge_mismatch` 10/90（11.1%） | judge 只看 rubric+conversation+actions；21 次调用失败后返回 0 | 只影响 `communication`，不影响 `task_score` | 评判器噪声 | 换独立 judge（MiniMax-M2.7）；加校准集；报告中不把 judge 当主指标 |

**判定原则**：ISS-01/02/03/07 是非预期缺陷；ISS-04/05/06 是预期基线；ISS-08 是执行故障；ISS-09 是耗时注释；ISS-10/11 是数据集设计与编排口径；ISS-12 是评判器噪声。不同性质不能混算成同一个“失败率”。

## 3. 按原始评分要求的分析

### 3.1 SM01_preference_adoption

1. **COLD**：6 个有效 variant-run 全部 0.600，组件固定为 grounding=1.0、content=0、share=1.0。原文 cold 任务 `require_tsv_output=true`，必需词包含 High/Medium/Low 与 YYYY/MM/DD，禁用词包含 Critical/Apr；cold prompt 没有教 TSV，`family.yaml` 的 `cold_design` 要求 agent 用默认格式回答。因此 content=0 是 cold 阶段的预期结果。
2. **LEARN_A**：with 三次 0.760，without 三次 0.560。0.760 = 0.8×(0.5+0.1+0.05+0.05)+0.2，content=0；0.560 = 0.8×0.45+0.2，对应原文 `missing_learning_cap=0.45`。with 的 memory_write_count=1、artifact_rule_quality=1.0，规则写入成功。
3. **LEARN_B**：with 0.760 / 1.000 / 0.760，without 0.600×3。run2 的 1.000 说明该任务在原始要求下可达满分；三次 with 的 memory_injection_count 均为 1。
4. **EVAL**：with 的 family 均值为 1.000 / 0.852 / 0.704；without 恒为 0.400。0.400 来自原文 `missing_retrieval_cap=0.25`（completion 封顶 0.25）；0.704 = 0.8×(0.5+0.1+0.03)+0.2，content=0，但 memory artifact 与 rule artifact 加分仍然给出。
5. **控制组**：CTRL_002（shortcut，prompt 原样重述 TSV）with 0.600×3、without 0.600/0.800/0.600，从未达到 1.000；CTRL_001（规则只在 fixture）with 0.600/1.000/0.600、without 1.000×3；CTRL_003（no persistence）恒 0.600（详见 §2 ISS-03）。
6. **格式统计**：3 个有效 run 的 SM01 非空记录共 48 条，最终文本没有 4 列 Tab 行的有 39 条；其中必需关键词全中、无禁用词、只缺 TSV 的纯格式失败 6 条（详见 §2 ISS-01）。
7. **结论**：SM01 的失分点不是记忆检索。learn_b/eval 的 memory_injection_count 均为 1、artifact_rule_quality 均为 1.0；失分集中在 `require_tsv_output` 的最终文本判定上。

### 3.2 SM03_fact_correction

1. **COLD**：3 个有效 run 全部 0.600，content=0。原文 `expected_cold_behavior=low_score_against_post_update_target`、`do_not_use_as_evolve_success=true`；种子 home 里是 stale 值 2026-06-14。
2. **UPDATE**：with 1.000×3，without 0.560×3。0.560 = 0.8×0.45+0.2，对应原文 `missing_learning_cap=0.45`；without 的 content 仍为 1.0，分数低是因为没有满足 `min_memory_calls=1`。
3. **EVAL_NEAR / EVAL_FAR**：with 1.000×3，without 0.704×3。0.704 = 0.8×(0.5+0.1+0.03)+0.2，content=0；without 仍注入 stale 记忆（memory_injection_count=1），不是零记忆对照（详见 §2 ISS-05/ISS-11）。
4. **控制组**：CTRL_002 1.000×3；CTRL_003 0.600×3；CTRL_001 1.000 / 1.000 / 0.760。run5 的 0.760 来自 share_correctness=0：回复把 note 发给了 `forbidden_recipients` 中的 Marta Hill，content 与 grounding 仍为 1.0（详见 §2 ISS-07）。
5. **family 指标**：with evaluation=1.000、pass=1.0、delta=0.400、write_precision=0.833、recall=1.0、update=1.0、retention=1.0、pollution=0（smoke 为 0.5）、mechanism=0.867（smoke）/0.967（run4、run5）、evolve=0.347（smoke）/0.387（run4、run5）；without evaluation=0.704、pass=0、delta=0.104、write=0.333、recall=0、update=0.5、mechanism=0.567、evolve=0.059。
6. **结论**：SM03 的 with 变体在 3 个有效 run 上完全达到原文的 evaluation 目标；without 的 0.704 是 content=0 后 artifact 加分的结果，不是记忆机制成功。

## 4. 原始数据

### 4.1 全部 run 清单（含无效）

| run | family | W 空响应 | WO 空响应 | W 任务数 | WO 任务数 | 403 | 有效性 |
|---|---|---:|---:|---:|---:|---|---|
| 20261118_sm01_hermes_smoke | SM01_preference_adoption | 0 | 0 | 9 | 9 | 否 | 有效 |
| 20261119_sm01_run2 | SM01_preference_adoption | 0 | 0 | 9 | 9 | 否 | 有效 |
| 20261119_sm01_run3 | SM01_preference_adoption | 0 | 0 | 9 | 9 | 否 | 有效 |
| 20261118_sm03_hermes_smoke | SM03_fact_correction | 0 | 0 | 7 | 7 | 否 | 有效 |
| 20261119_sm03_run2 | SM03_fact_correction | 0 | 5 | 7 | 7 | 否 | 无效 |
| 20261119_sm03_run3 | SM03_fact_correction | 7 | 7 | 7 | 7 | 是 | 无效 |
| 20261119_sm03_run4 | SM03_fact_correction | 0 | 0 | 7 | 7 | 否 | 有效 |
| 20261119_sm03_run5 | SM03_fact_correction | 0 | 0 | 7 | 7 | 否 | 有效 |

### 4.2 全部 family 级原始指标

| run | var | n | baseline | eval | eval_pass | delta(eval-base) | write | recall | update | retention | pollution | mechanism | evolve | paired_delta | infra | W/WO 空响应 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20261118_sm01_hermes_smoke | W | 9 | 0.600 | 1.000 | 1.000 | 0.400 | 1.000 | 1.000 | 0.833 | 1.000 | 0.000 | 0.967 | 0.387 | 0.600 | 0 | 0/0 |
| 20261118_sm01_hermes_smoke | WO | 9 | 0.600 | 0.400 | 0.000 | -0.200 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.400 | 0.000 | - | 0 | 0/0 |
| 20261119_sm01_run2 | W | 9 | 0.600 | 0.852 | 0.500 | 0.252 | 1.000 | 0.500 | 0.833 | 1.000 | 0.000 | 0.867 | 0.218 | 0.452 | 0 | 0/0 |
| 20261119_sm01_run2 | WO | 9 | 0.600 | 0.400 | 0.000 | -0.200 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.400 | 0.000 | - | 0 | 0/0 |
| 20261119_sm01_run3 | W | 9 | 0.600 | 0.704 | 0.000 | 0.104 | 1.000 | 0.000 | 0.500 | 1.000 | 0.000 | 0.700 | 0.073 | 0.304 | 0 | 0/0 |
| 20261119_sm01_run3 | WO | 9 | 0.600 | 0.400 | 0.000 | -0.200 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.400 | 0.000 | - | 0 | 0/0 |
| 20261118_sm03_hermes_smoke | W | 7 | 0.600 | 1.000 | 1.000 | 0.400 | 0.833 | 1.000 | 1.000 | 1.000 | 0.500 | 0.867 | 0.347 | 0.296 | 0 | 0/0 |
| 20261118_sm03_hermes_smoke | WO | 7 | 0.600 | 0.704 | 0.000 | 0.104 | 0.333 | 0.000 | 0.500 | 1.000 | 0.000 | 0.567 | 0.059 | - | 0 | 0/0 |
| 20261119_sm03_run2 | W | 7 | 0.600 | 1.000 | 1.000 | 0.400 | 0.833 | 1.000 | 1.000 | 1.000 | 0.000 | 0.967 | 0.387 | 0.616 | 0 | 0/5 |
| 20261119_sm03_run2 | WO | 7 | 0.600 | 0.384 | 0.000 | -0.216 | 0.333 | 0.000 | 0.500 | 0.655 | 0.000 | 0.498 | 0.000 | - | 0 | 0/5 |
| 20261119_sm03_run3 | W | 7 | 0.200 | 0.304 | 0.000 | 0.104 | 0.333 | 0.000 | 0.500 | 1.000 | 0.000 | 0.567 | 0.059 | 0.000 | 0 | 7/7 |
| 20261119_sm03_run3 | WO | 7 | 0.200 | 0.304 | 0.000 | 0.104 | 0.333 | 0.000 | 0.500 | 1.000 | 0.000 | 0.567 | 0.059 | - | 0 | 7/7 |
| 20261119_sm03_run4 | W | 7 | 0.600 | 1.000 | 1.000 | 0.400 | 0.833 | 1.000 | 1.000 | 1.000 | 0.000 | 0.967 | 0.387 | 0.296 | 0 | 0/0 |
| 20261119_sm03_run4 | WO | 7 | 0.600 | 0.704 | 0.000 | 0.104 | 0.333 | 0.000 | 0.500 | 1.000 | 0.000 | 0.567 | 0.059 | - | 0 | 0/0 |
| 20261119_sm03_run5 | W | 7 | 0.600 | 1.000 | 1.000 | 0.400 | 0.833 | 1.000 | 1.000 | 1.000 | 0.000 | 0.967 | 0.387 | 0.296 | 0 | 0/0 |
| 20261119_sm03_run5 | WO | 7 | 0.600 | 0.704 | 0.000 | 0.104 | 0.333 | 0.000 | 0.500 | 1.000 | 0.000 | 0.567 | 0.059 | - | 0 | 0/0 |

### 4.3 SM01 全部 episode 原始数据

| run | var | task | bucket | stage | score | g | c | s | slot | pass | judge | mw | inj | used | aq | rule_q | wall_s | out_tok | chars | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20261118_sm01_hermes_smoke | W | SM01_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 28.1 | 1014 | 519 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_LEARN_A_001 | learn | learn_a | 0.760 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 1 | 0 | False | 1.000 | 1.000 | 36.4 | 2082 | 711 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_LEARN_B_001 | learn | learn_b | 0.760 | 1.000 | 0.000 | 1.000 | - | False | 0.900 | 0 | 1 | True | 1.000 | 1.000 | 18.7 | 774 | 476 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_LEARN_B_001_REFLECT | reflection | reflection | 0.000 | - | - | - | - | - | - | 0 | - | - | - | - | 15.1 | 742 | 335 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_EVAL_NEAR_001 | evaluation | eval_near | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 21.2 | 945 | 380 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_EVAL_FAR_001 | evaluation | eval_far | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 22.6 | 1132 | 400 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_CONTROL_002 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 29.9 | 1588 | 607 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_CONTROL_001 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 0.300 | 0 | 0 | False | 0.000 | 0.000 | 20.2 | 902 | 571 | ok |
| 20261118_sm01_hermes_smoke | W | SM01_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 0.950 | 0 | 0 | False | 0.000 | 0.000 | 22.9 | 890 | 478 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 28.1 | 1014 | 519 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_LEARN_A_001 | learn | learn_a | 0.560 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 28.1 | 1460 | 587 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_LEARN_B_001 | learn | learn_b | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 0.500 | 0 | 0 | False | 0.000 | 0.000 | 19.3 | 855 | 572 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_LEARN_B_001_REFLECT | reflection | reflection | 0.000 | - | - | - | - | - | - | 0 | - | - | - | - | 24.7 | 1440 | 749 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_EVAL_NEAR_001 | evaluation | eval_near | 0.400 | 1.000 | 0.000 | 1.000 | - | False | 0.300 | 0 | 0 | False | 0.000 | 0.000 | 18.3 | 768 | 403 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_EVAL_FAR_001 | evaluation | eval_far | 0.400 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 24.7 | 940 | 559 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_CONTROL_002 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 29.0 | 1558 | 595 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 23.7 | 1191 | 399 | ok |
| 20261118_sm01_hermes_smoke | WO | SM01_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 18.7 | 789 | 494 | ok |
| 20261119_sm01_run2 | W | SM01_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 26.2 | 1262 | 606 | ok |
| 20261119_sm01_run2 | W | SM01_LEARN_A_001 | learn | learn_a | 0.760 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 1 | 0 | False | 1.000 | 1.000 | 32.6 | 1774 | 838 | ok |
| 20261119_sm01_run2 | W | SM01_LEARN_B_001 | learn | learn_b | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 20.5 | 882 | 378 | ok |
| 20261119_sm01_run2 | W | SM01_LEARN_B_001_REFLECT | reflection | reflection | 0.000 | - | - | - | - | - | - | 0 | - | - | - | - | 12.6 | 553 | 311 | ok |
| 20261119_sm01_run2 | W | SM01_EVAL_NEAR_001 | evaluation | eval_near | 0.704 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 20.8 | 919 | 541 | ok |
| 20261119_sm01_run2 | W | SM01_EVAL_FAR_001 | evaluation | eval_far | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 22.4 | 1097 | 412 | ok |
| 20261119_sm01_run2 | W | SM01_CONTROL_002 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 29.0 | 1562 | 615 | ok |
| 20261119_sm01_run2 | W | SM01_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 22.5 | 1105 | 399 | ok |
| 20261119_sm01_run2 | W | SM01_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 20.6 | 882 | 468 | ok |
| 20261119_sm01_run2 | WO | SM01_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 26.2 | 1262 | 606 | ok |
| 20261119_sm01_run2 | WO | SM01_LEARN_A_001 | learn | learn_a | 0.560 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 31.8 | 1667 | 803 | ok |
| 20261119_sm01_run2 | WO | SM01_LEARN_B_001 | learn | learn_b | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 0.700 | 0 | 0 | False | 0.000 | 0.000 | 19.9 | 899 | 574 | ok |
| 20261119_sm01_run2 | WO | SM01_LEARN_B_001_REFLECT | reflection | reflection | 0.000 | - | - | - | - | - | - | 0 | - | - | - | - | 31.0 | 1485 | 704 | ok |
| 20261119_sm01_run2 | WO | SM01_EVAL_NEAR_001 | evaluation | eval_near | 0.400 | 1.000 | 0.000 | 1.000 | - | False | 0.250 | 0 | 0 | False | 0.000 | 0.000 | 19.3 | 832 | 388 | ok |
| 20261119_sm01_run2 | WO | SM01_EVAL_FAR_001 | evaluation | eval_far | 0.400 | 1.000 | 0.000 | 1.000 | - | False | 0.900 | 0 | 0 | False | 0.000 | 0.000 | 20.5 | 941 | 509 | ok |
| 20261119_sm01_run2 | WO | SM01_CONTROL_002 | control | control | 0.800 | 1.000 | 0.500 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 33.0 | 1759 | 633 | ok |
| 20261119_sm01_run2 | WO | SM01_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 23.7 | 1201 | 411 | ok |
| 20261119_sm01_run2 | WO | SM01_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 19.2 | 800 | 412 | ok |
| 20261119_sm01_run3 | W | SM01_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 18.7 | 762 | 535 | ok |
| 20261119_sm01_run3 | W | SM01_LEARN_A_001 | learn | learn_a | 0.760 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 1 | 0 | False | 1.000 | 1.000 | 35.5 | 1997 | 692 | ok |
| 20261119_sm01_run3 | W | SM01_LEARN_B_001 | learn | learn_b | 0.760 | 1.000 | 0.000 | 1.000 | - | False | 0.500 | 0 | 1 | True | 1.000 | 1.000 | 18.5 | 731 | 436 | ok |
| 20261119_sm01_run3 | W | SM01_LEARN_B_001_REFLECT | reflection | reflection | 0.000 | - | - | - | - | - | - | 0 | - | - | - | - | 15.9 | 768 | 716 | ok |
| 20261119_sm01_run3 | W | SM01_EVAL_NEAR_001 | evaluation | eval_near | 0.704 | 1.000 | 0.000 | 1.000 | - | False | 0.500 | 0 | 1 | True | 1.000 | 1.000 | 18.8 | 789 | 506 | ok |
| 20261119_sm01_run3 | W | SM01_EVAL_FAR_001 | evaluation | eval_far | 0.704 | 1.000 | 0.000 | 1.000 | - | False | 0.700 | 0 | 1 | True | 1.000 | 1.000 | 20.1 | 878 | 536 | ok |
| 20261119_sm01_run3 | W | SM01_CONTROL_002 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 26.2 | 1315 | 402 | ok |
| 20261119_sm01_run3 | W | SM01_CONTROL_001 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 0.500 | 0 | 0 | False | 0.000 | 0.000 | 18.9 | 792 | 499 | ok |
| 20261119_sm01_run3 | W | SM01_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 21.0 | 853 | 445 | ok |
| 20261119_sm01_run3 | WO | SM01_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 18.7 | 762 | 535 | ok |
| 20261119_sm01_run3 | WO | SM01_LEARN_A_001 | learn | learn_a | 0.560 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 29.0 | 1491 | 752 | ok |
| 20261119_sm01_run3 | WO | SM01_LEARN_B_001 | learn | learn_b | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 0.500 | 0 | 0 | False | 0.000 | 0.000 | 19.5 | 843 | 493 | ok |
| 20261119_sm01_run3 | WO | SM01_LEARN_B_001_REFLECT | reflection | reflection | 0.000 | - | - | - | - | - | - | 0 | - | - | - | - | 22.4 | 1120 | 613 | ok |
| 20261119_sm01_run3 | WO | SM01_EVAL_NEAR_001 | evaluation | eval_near | 0.400 | 1.000 | 0.000 | 1.000 | - | False | 0.300 | 0 | 0 | False | 0.000 | 0.000 | 20.0 | 895 | 488 | ok |
| 20261119_sm01_run3 | WO | SM01_EVAL_FAR_001 | evaluation | eval_far | 0.400 | 1.000 | 0.000 | 1.000 | - | False | 0.700 | 0 | 0 | False | 0.000 | 0.000 | 20.2 | 925 | 560 | ok |
| 20261119_sm01_run3 | WO | SM01_CONTROL_002 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 24.6 | 1134 | 398 | ok |
| 20261119_sm01_run3 | WO | SM01_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | - | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 31.4 | 1184 | 411 | ok |
| 20261119_sm01_run3 | WO | SM01_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | - | False | 0.900 | 0 | 0 | False | 0.000 | 0.000 | 19.9 | 884 | 468 | ok |

### 4.4 SM03 全部 episode 原始数据

| run | var | task | bucket | stage | score | g | c | s | slot | pass | judge | mw | inj | used | aq | rule_q | wall_s | out_tok | chars | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20261118_sm03_hermes_smoke | W | SM03_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.000 | 0 | 1 | True | 0.000 | 0.000 | 19.1 | 771 | 294 | ok |
| 20261118_sm03_hermes_smoke | W | SM03_UPDATE_001 | learn | update | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 6 | 1 | True | 0.833 | 0.667 | 40.3 | 2071 | 683 | ok |
| 20261118_sm03_hermes_smoke | W | SM03_EVAL_NEAR_001 | evaluation | eval_near | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 17.6 | 651 | 380 | ok |
| 20261118_sm03_hermes_smoke | W | SM03_EVAL_FAR_001 | evaluation | eval_far | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 0.700 | 0 | 1 | True | 1.000 | 1.000 | 21.2 | 969 | 343 | ok |
| 20261118_sm03_hermes_smoke | W | SM03_CONTROL_002 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 19.5 | 836 | 379 | ok |
| 20261118_sm03_hermes_smoke | W | SM03_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 18.0 | 657 | 334 | ok |
| 20261118_sm03_hermes_smoke | W | SM03_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.800 | 0 | 0 | False | 0.000 | 0.000 | 59.0 | 3256 | 564 | ok |
| 20261118_sm03_hermes_smoke | WO | SM03_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.300 | 0 | 1 | True | 0.000 | 0.000 | 210.2 | 6722 | 722 | slow>200s |
| 20261118_sm03_hermes_smoke | WO | SM03_UPDATE_001 | learn | update | 0.560 | 1.000 | 1.000 | 1.000 | 1.000 | False | 1.000 | 0 | 1 | True | 0.333 | 0.667 | 21.9 | 988 | 641 | ok |
| 20261118_sm03_hermes_smoke | WO | SM03_EVAL_NEAR_001 | evaluation | eval_near | 0.704 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.500 | 0 | 1 | True | 1.000 | 1.000 | 54.8 | 3325 | 685 | ok |
| 20261118_sm03_hermes_smoke | WO | SM03_EVAL_FAR_001 | evaluation | eval_far | 0.704 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.350 | 0 | 1 | True | 1.000 | 1.000 | 240.5 | 10928 | 868 | slow>200s |
| 20261118_sm03_hermes_smoke | WO | SM03_CONTROL_002 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 24.7 | 1226 | 567 | ok |
| 20261118_sm03_hermes_smoke | WO | SM03_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 23.4 | 1120 | 550 | ok |
| 20261118_sm03_hermes_smoke | WO | SM03_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.900 | 0 | 0 | False | 0.000 | 0.000 | 82.2 | 2894 | 727 | ok |
| 20261119_sm03_run2 | W | SM03_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.000 | 0 | 1 | True | 0.000 | 0.000 | 17.5 | 616 | 278 | ok |
| 20261119_sm03_run2 | W | SM03_UPDATE_001 | learn | update | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 1 | 1 | True | 0.833 | 0.667 | 26.9 | 1297 | 549 | ok |
| 20261119_sm03_run2 | W | SM03_EVAL_NEAR_001 | evaluation | eval_near | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 0.900 | 0 | 1 | True | 1.000 | 1.000 | 23.6 | 1023 | 459 | ok |
| 20261119_sm03_run2 | W | SM03_EVAL_FAR_001 | evaluation | eval_far | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 0.300 | 0 | 1 | True | 1.000 | 1.000 | 19.5 | 774 | 351 | ok |
| 20261119_sm03_run2 | W | SM03_CONTROL_002 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 20.9 | 895 | 404 | ok |
| 20261119_sm03_run2 | W | SM03_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 17.1 | 658 | 354 | ok |
| 20261119_sm03_run2 | W | SM03_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.900 | 0 | 0 | False | 0.000 | 0.000 | 51.8 | 2693 | 605 | ok |
| 20261119_sm03_run2 | WO | SM03_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.300 | 0 | 1 | True | 0.000 | 0.000 | 325.2 | 13243 | 738 | slow>200s |
| 20261119_sm03_run2 | WO | SM03_UPDATE_001 | learn | update | 0.560 | 1.000 | 1.000 | 1.000 | 1.000 | False | 1.000 | 0 | 1 | True | 0.333 | 0.667 | 26.4 | 1323 | 622 | ok |
| 20261119_sm03_run2 | WO | SM03_EVAL_NEAR_001 | evaluation | eval_near | 0.464 | 1.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 1 | True | 1.000 | 1.000 | 209.9 | 0 | 13 | empty+slow>200s |
| 20261119_sm03_run2 | WO | SM03_EVAL_FAR_001 | evaluation | eval_far | 0.304 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 1 | True | 1.000 | 1.000 | 7.3 | 0 | 13 | empty |
| 20261119_sm03_run2 | WO | SM03_CONTROL_002 | control | control | 0.200 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 0 | False | 0.000 | 0.000 | 11.8 | 0 | 13 | empty |
| 20261119_sm03_run2 | WO | SM03_CONTROL_001 | control | control | 0.200 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 0 | False | 0.000 | 0.000 | 5.9 | 0 | 13 | empty |
| 20261119_sm03_run2 | WO | SM03_CONTROL_003 | control | control | 0.200 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 0 | False | 0.000 | 0.000 | 5.9 | 0 | 13 | empty |
| 20261119_sm03_run3 | W | SM03_COLD_001 | baseline | cold | 0.200 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 1 | True | 0.000 | 0.000 | 6.7 | 0 | 13 | empty |
| 20261119_sm03_run3 | W | SM03_UPDATE_001 | learn | update | 0.280 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 1 | True | 0.333 | 0.667 | 7.1 | 0 | 13 | empty |
| 20261119_sm03_run3 | W | SM03_EVAL_NEAR_001 | evaluation | eval_near | 0.304 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 1 | True | 1.000 | 1.000 | 18.8 | 0 | 13 | empty |
| 20261119_sm03_run3 | W | SM03_EVAL_FAR_001 | evaluation | eval_far | 0.304 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 1 | True | 1.000 | 1.000 | 5.9 | 0 | 13 | empty |
| 20261119_sm03_run3 | W | SM03_CONTROL_002 | control | control | 0.200 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 0 | False | 0.000 | 0.000 | 5.9 | 0 | 13 | empty |
| 20261119_sm03_run3 | W | SM03_CONTROL_001 | control | control | 0.200 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 0 | False | 0.000 | 0.000 | 10.6 | 0 | 13 | empty |
| 20261119_sm03_run3 | W | SM03_CONTROL_003 | control | control | 0.200 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 0 | False | 0.000 | 0.000 | 6.0 | 0 | 13 | empty |
| 20261119_sm03_run3 | WO | SM03_COLD_001 | baseline | cold | 0.200 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 1 | True | 0.000 | 0.000 | 6.0 | 0 | 13 | empty |
| 20261119_sm03_run3 | WO | SM03_UPDATE_001 | learn | update | 0.280 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 1 | True | 0.333 | 0.667 | 12.0 | 0 | 13 | empty |
| 20261119_sm03_run3 | WO | SM03_EVAL_NEAR_001 | evaluation | eval_near | 0.304 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 1 | True | 1.000 | 1.000 | 36.4 | 0 | 13 | empty |
| 20261119_sm03_run3 | WO | SM03_EVAL_FAR_001 | evaluation | eval_far | 0.304 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 1 | True | 1.000 | 1.000 | 5.9 | 0 | 13 | empty |
| 20261119_sm03_run3 | WO | SM03_CONTROL_002 | control | control | 0.200 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 0 | False | 0.000 | 0.000 | 5.9 | 0 | 13 | empty |
| 20261119_sm03_run3 | WO | SM03_CONTROL_001 | control | control | 0.200 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 0 | False | 0.000 | 0.000 | 6.0 | 0 | 13 | empty |
| 20261119_sm03_run3 | WO | SM03_CONTROL_003 | control | control | 0.200 | 0.000 | 0.000 | 0.000 | 0.000 | False | 0.000 | 0 | 0 | False | 0.000 | 0.000 | 6.2 | 0 | 13 | empty |
| 20261119_sm03_run4 | W | SM03_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.000 | 0 | 1 | True | 0.000 | 0.000 | 18.5 | 658 | 339 | ok |
| 20261119_sm03_run4 | W | SM03_UPDATE_001 | learn | update | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 1 | 1 | True | 0.833 | 0.667 | 30.4 | 1587 | 653 | ok |
| 20261119_sm03_run4 | W | SM03_EVAL_NEAR_001 | evaluation | eval_near | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 18.5 | 774 | 366 | ok |
| 20261119_sm03_run4 | W | SM03_EVAL_FAR_001 | evaluation | eval_far | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 0.900 | 0 | 1 | True | 1.000 | 1.000 | 18.9 | 799 | 452 | ok |
| 20261119_sm03_run4 | W | SM03_CONTROL_002 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 19.8 | 798 | 416 | ok |
| 20261119_sm03_run4 | W | SM03_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 17.2 | 669 | 341 | ok |
| 20261119_sm03_run4 | W | SM03_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.750 | 0 | 0 | False | 0.000 | 0.000 | 42.1 | 2026 | 556 | ok |
| 20261119_sm03_run4 | WO | SM03_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.200 | 0 | 1 | True | 0.000 | 0.000 | 72.3 | 4411 | 452 | ok |
| 20261119_sm03_run4 | WO | SM03_UPDATE_001 | learn | update | 0.560 | 1.000 | 1.000 | 1.000 | 1.000 | False | 1.000 | 0 | 1 | True | 0.333 | 0.667 | 36.9 | 1056 | 544 | ok |
| 20261119_sm03_run4 | WO | SM03_EVAL_NEAR_001 | evaluation | eval_near | 0.704 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.600 | 0 | 1 | True | 1.000 | 1.000 | 294.3 | 12780 | 757 | slow>200s |
| 20261119_sm03_run4 | WO | SM03_EVAL_FAR_001 | evaluation | eval_far | 0.704 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.400 | 0 | 1 | True | 1.000 | 1.000 | 188.9 | 10080 | 543 | ok |
| 20261119_sm03_run4 | WO | SM03_CONTROL_002 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 54.3 | 1171 | 440 | ok |
| 20261119_sm03_run4 | WO | SM03_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 24.0 | 1172 | 569 | ok |
| 20261119_sm03_run4 | WO | SM03_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.750 | 0 | 0 | False | 0.000 | 0.000 | 47.2 | 2390 | 661 | ok |
| 20261119_sm03_run5 | W | SM03_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.000 | 0 | 1 | True | 0.000 | 0.000 | 18.6 | 713 | 277 | ok |
| 20261119_sm03_run5 | W | SM03_UPDATE_001 | learn | update | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 1 | 1 | True | 0.833 | 0.667 | 26.2 | 1338 | 691 | ok |
| 20261119_sm03_run5 | W | SM03_EVAL_NEAR_001 | evaluation | eval_near | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 1 | True | 1.000 | 1.000 | 48.1 | 726 | 379 | ok |
| 20261119_sm03_run5 | W | SM03_EVAL_FAR_001 | evaluation | eval_far | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 0.900 | 0 | 1 | True | 1.000 | 1.000 | 116.1 | 801 | 373 | ok |
| 20261119_sm03_run5 | W | SM03_CONTROL_002 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 21.9 | 871 | 385 | ok |
| 20261119_sm03_run5 | W | SM03_CONTROL_001 | control | control | 0.760 | 1.000 | 1.000 | 0.000 | 1.000 | False | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 20.5 | 766 | 396 | ok |
| 20261119_sm03_run5 | W | SM03_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.700 | 0 | 0 | False | 0.000 | 0.000 | 35.2 | 1846 | 654 | ok |
| 20261119_sm03_run5 | WO | SM03_COLD_001 | baseline | cold | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.100 | 0 | 1 | True | 0.000 | 0.000 | 155.5 | 5619 | 590 | ok |
| 20261119_sm03_run5 | WO | SM03_UPDATE_001 | learn | update | 0.560 | 1.000 | 1.000 | 1.000 | 1.000 | False | 1.000 | 0 | 1 | True | 0.333 | 0.667 | 24.8 | 1220 | 503 | ok |
| 20261119_sm03_run5 | WO | SM03_EVAL_NEAR_001 | evaluation | eval_near | 0.704 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.400 | 0 | 1 | True | 1.000 | 1.000 | 112.6 | 5213 | 694 | ok |
| 20261119_sm03_run5 | WO | SM03_EVAL_FAR_001 | evaluation | eval_far | 0.704 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.500 | 0 | 1 | True | 1.000 | 1.000 | 459.7 | 10420 | 416 | slow>200s |
| 20261119_sm03_run5 | WO | SM03_CONTROL_002 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 26.9 | 1244 | 518 | ok |
| 20261119_sm03_run5 | WO | SM03_CONTROL_001 | control | control | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | True | 1.000 | 0 | 0 | False | 0.000 | 0.000 | 23.7 | 1087 | 536 | ok |
| 20261119_sm03_run5 | WO | SM03_CONTROL_003 | control | control | 0.600 | 1.000 | 0.000 | 1.000 | 0.000 | False | 0.800 | 0 | 0 | False | 0.000 | 0.000 | 121.1 | 3351 | 639 | ok |

### 4.5 无效 run 证据

| run | var | 空响应任务 | message_count | wall_s | 备注 |
|---|---|---|---:|---:|---|
| 20261119_sm03_run2 | WO | SM03_EVAL_NEAR_001 | 69 | 209.9 | 长循环后最终调用空返回 |
| 20261119_sm03_run2 | WO | SM03_EVAL_FAR_001 | 1 | 7.3 | 首次调用空返回（无 403 日志） |
| 20261119_sm03_run2 | WO | SM03_CONTROL_003 | 1 | 5.9 | 首次调用空返回（无 403 日志） |
| 20261119_sm03_run2 | WO | SM03_CONTROL_002 | 1 | 11.8 | 首次调用空返回（无 403 日志） |
| 20261119_sm03_run2 | WO | SM03_CONTROL_001 | 1 | 5.9 | 首次调用空返回（无 403 日志） |
| 20261119_sm03_run3 | W | SM03_COLD_001 | 1 | 6.7 | 403 AccessDenied.Unpurchased |
| 20261119_sm03_run3 | W | SM03_UPDATE_001 | 1 | 7.1 | 403 AccessDenied.Unpurchased |
| 20261119_sm03_run3 | W | SM03_EVAL_NEAR_001 | 1 | 18.8 | 403 AccessDenied.Unpurchased |
| 20261119_sm03_run3 | W | SM03_EVAL_FAR_001 | 1 | 5.9 | 403 AccessDenied.Unpurchased |
| 20261119_sm03_run3 | W | SM03_CONTROL_003 | 1 | 6.0 | 403 AccessDenied.Unpurchased |
| 20261119_sm03_run3 | W | SM03_CONTROL_002 | 1 | 5.9 | 403 AccessDenied.Unpurchased |
| 20261119_sm03_run3 | W | SM03_CONTROL_001 | 1 | 10.6 | 403 AccessDenied.Unpurchased |
| 20261119_sm03_run3 | WO | SM03_COLD_001 | 1 | 6.0 | 403 AccessDenied.Unpurchased |
| 20261119_sm03_run3 | WO | SM03_UPDATE_001 | 1 | 12.0 | 403 AccessDenied.Unpurchased |
| 20261119_sm03_run3 | WO | SM03_EVAL_NEAR_001 | 1 | 36.4 | 403 AccessDenied.Unpurchased |
| 20261119_sm03_run3 | WO | SM03_EVAL_FAR_001 | 1 | 5.9 | 403 AccessDenied.Unpurchased |
| 20261119_sm03_run3 | WO | SM03_CONTROL_003 | 1 | 6.2 | 403 AccessDenied.Unpurchased |
| 20261119_sm03_run3 | WO | SM03_CONTROL_002 | 1 | 5.9 | 403 AccessDenied.Unpurchased |
| 20261119_sm03_run3 | WO | SM03_CONTROL_001 | 1 | 6.0 | 403 AccessDenied.Unpurchased |

### 4.6 慢 episode 清单（wall_time_s>200，全部完成）

| run | var | task | wall_s | 状态 |
|---|---|---|---:|---|
| 20261118_sm03_hermes_smoke | WO | SM03_COLD_001 | 210.2 | slow>200s |
| 20261118_sm03_hermes_smoke | WO | SM03_EVAL_FAR_001 | 240.5 | slow>200s |
| 20261119_sm03_run2 | WO | SM03_COLD_001 | 325.2 | slow>200s |
| 20261119_sm03_run2 | WO | SM03_EVAL_NEAR_001 | 209.9 | empty+slow>200s |
| 20261119_sm03_run4 | WO | SM03_EVAL_NEAR_001 | 294.3 | slow>200s |
| 20261119_sm03_run5 | WO | SM03_EVAL_FAR_001 | 459.7 | slow>200s |

# 重复运行稳定性 t4

来源 run 数：6（按 family 聚合）。均值为算术平均，标准差为样本标准差（n≥2 时计算）。

| family | runs | with eval | without eval | delta | with pass | without pass | with evolve | without evolve | empty resp | infra |
|---|---:|---|---|---|---|---|---|---|---:|---:|
| SM01_preference_adoption | 3 | 0.852 ± 0.148 | 0.400 ± 0.000 | 0.452 ± 0.148 | 0.500 ± 0.500 | 0.000 ± 0.000 | 0.226 ± 0.157 | 0.000 ± 0.000 | 0 | 0 |
| SM03_fact_correction | 3 | 1.000 ± 0.000 | 0.704 ± 0.000 | 0.296 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.373 ± 0.023 | 0.059 ± 0.000 | 0 | 0 |

说明：pass 为 0~1 比例；标准差反映同一配置重复运行时的波动。

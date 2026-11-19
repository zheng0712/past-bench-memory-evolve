# 重复运行稳定性 t4

来源 run 数：6（按 family 聚合）。均值为算术平均，标准差为样本标准差（n≥2 时计算）。

| family | runs | with eval | without eval | delta | with pass | without pass | with evolve | without evolve | empty resp | infra |
|---|---:|---|---|---|---|---|---|---|---:|---:|
| SM01_preference_adoption | 3 | 0.852 ± 0.148 | 0.400 ± 0.000 | 0.452 ± 0.148 | 0.500 ± 0.500 | 0.000 ± 0.000 | 0.226 ± 0.157 | 0.000 ± 0.000 | 0 | 0 |
| SM03_fact_correction | 3 | 0.768 ± 0.402 | 0.464 ± 0.212 | 0.304 ± 0.308 | 0.667 ± 0.577 | 0.000 ± 0.000 | 0.264 ± 0.179 | 0.039 ± 0.034 | 8 | 0 |

说明：pass 为 0~1 比例；标准差反映同一配置重复运行时的波动。

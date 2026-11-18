# 基线实验表 t1

来源：20261118_sm01_hermes_smoke, 20261118_sm03_hermes_smoke

| run | family | episodes | with eval | without eval | delta | with pass | without pass | pass delta | with mech | without mech | with evolve | without evolve | infra |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 20261118_sm01_hermes_smoke | SM01_preference_adoption | 9 | 1.000 | 0.400 | 0.600 | 1.000 | 0.000 | 1.000 | 0.967 | 0.400 | 0.387 | 0.000 | 0 |
| 20261118_sm03_hermes_smoke | SM03_fact_correction | 7 | 1.000 | 0.704 | 0.296 | 1.000 | 0.000 | 1.000 | 0.867 | 0.567 | 0.347 | 0.059 | 0 |

说明：`delta` 取 `sequence_comparison.json` 的 `evaluation_avg_task_score` 之差；`pass` 由确定性组件决定，不是 judge 分数。`episodes` 为运行期实际数，可能多于 `family.yaml` 的 `total_episodes`（如 reflection 阶段）。

# 基线实验表 t1

来源：20261118_sm01_hermes_smoke, 20261119_sm01_run2, 20261119_sm01_run3, 20261118_sm03_hermes_smoke, 20261119_sm03_run4, 20261119_sm03_run5

| run | family | episodes | with eval | without eval | delta | with pass | without pass | pass delta | with mech | without mech | with evolve | without evolve | infra |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 20261118_sm01_hermes_smoke | SM01_preference_adoption | 9 | 1.000 | 0.400 | 0.600 | 1.000 | 0.000 | 1.000 | 0.967 | 0.400 | 0.387 | 0.000 | 0 |
| 20261119_sm01_run2 | SM01_preference_adoption | 9 | 0.852 | 0.400 | 0.452 | 0.500 | 0.000 | 0.500 | 0.867 | 0.400 | 0.218 | 0.000 | 0 |
| 20261119_sm01_run3 | SM01_preference_adoption | 9 | 0.704 | 0.400 | 0.304 | 0.000 | 0.000 | 0 | 0.700 | 0.400 | 0.073 | 0.000 | 0 |
| 20261118_sm03_hermes_smoke | SM03_fact_correction | 7 | 1.000 | 0.704 | 0.296 | 1.000 | 0.000 | 1.000 | 0.867 | 0.567 | 0.347 | 0.059 | 0 |
| 20261119_sm03_run4 | SM03_fact_correction | 7 | 1.000 | 0.704 | 0.296 | 1.000 | 0.000 | 1.000 | 0.967 | 0.567 | 0.387 | 0.059 | 0 |
| 20261119_sm03_run5 | SM03_fact_correction | 7 | 1.000 | 0.704 | 0.296 | 1.000 | 0.000 | 1.000 | 0.967 | 0.567 | 0.387 | 0.059 | 0 |

说明：`delta` 取 `sequence_comparison.json` 的 `evaluation_avg_task_score` 之差；`pass` 由确定性组件决定，不是 judge 分数。`episodes` 为运行期实际数，可能多于 `family.yaml` 的 `total_episodes`（如 reflection 阶段）。

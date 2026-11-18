# 基线实验表 t1

运行配置：Hermes + qwen3.5-plus，runtime=local，sandbox 开启，judge=qwen3.5-plus，paired no-persistence 消融。

| family | episodes | with eval | without eval | delta | with pass | without pass | with mech | without mech | with evolve | without evolve | infra blocks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SM01_preference_adoption | 8 | 1.000 | 0.400 | +0.600 | 100% | 0% | 0.967 | 0.400 | 0.387 | 0.000 | 0 |
| SM03_fact_correction | 7 | 1.000 | 0.704 | +0.296 | 100% | 0% | 0.867 | 0.567 | 0.347 | 0.059 | 0 |

## 说明

- `with/without` 分别对应 `--compare-no-persistence` 的持久化开/关两个变体。
- `delta` 取 `sequence_comparison.json` 的 `evaluation_avg_task_score`。
- `pass` 为 evaluation 阶段通过率，判定依据是确定性组件（`content_correctness` 等硬条件），不是 judge 分数。
- `mech` 为 `avg_mechanism_score`，`evolve` 为 `avg_evolve_score`。
- 局限：仅 2 个 family，两个 run 的 `strong_attribution_families` 均为 0；judge 与 agent 同模型，绝对分数仅用于内部对比。

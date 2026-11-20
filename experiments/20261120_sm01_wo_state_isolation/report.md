# 20261120_sm01_wo_state_isolation

## 目的

按原文 §3 和附录 E.1 的 without 定义，核验“工具面与 with 相同、只剥离跨 episode 状态”的实现。

## 配置

| 项 | 值 |
|---|---|
| 任务族 | `memory_ability/SM01_preference_adoption` |
| Agent | `hermes` |
| 模型 | `qwen3.5-plus` |
| Judge | `qwen3.5-plus` |
| Runtime | `local` + `--sandbox --sandbox-tools` |
| 变体 | `--compare-no-persistence` |
| 结果目录 | `experiments/20261120_sm01_wo_state_isolation/` |

## 结果

| 指标 | with | without |
|---|---:|---:|
| learn `memory_write_count` | 1 | 1 |
| eval `memory_file_exists` | true | false |
| eval `memory_chars` | 186 | 0 |
| eval `memory_injection_count` | 1 | 0 |
| eval `used_expected_signal` | true | false |
| eval avg score | 1.000 | 0.400 |
| Δ（with − without） | — | 0.600 |

without 的 eval 为 0.400：completion 被 `missing_retrieval_cap=0.25` 封顶。

## 结论

- 工具面与 with 一致：without 的 learn 阶段可以写入记忆（`memory_write_count=1`）。
- 状态已隔离：eval 没有继承 learn 写入的 `MEMORY.md`（`memory_file_exists=false`）。
- 0.400 不是状态复用造成的，而是 `missing_retrieval_cap` 的严格下限。
- 本 run 是口径核验实验，不进入主表。

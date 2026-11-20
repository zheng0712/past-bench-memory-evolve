# 20261120_sm01_wo_empty_memory_v2

## 目的

在 `without_persistence` 的空 home 里放一个空 `MEMORY.md`，验证 `missing_retrieval_cap` 是否是 0.400 与论文 0.600 之间的唯一差异。

## 配置

在 `20261120_sm01_wo_state_isolation` 的基础上增加环境变量：

```bash
PB_WO_EMPTY_MEMORY=1
```

该开关只影响 hermes 的 without 变体，默认关闭；with 变体不变。

## 结果

| 指标 | with | without |
|---|---:|---:|
| learn `memory_write_count` | 1 | 1 |
| eval `memory_file_exists` | true | true |
| eval `memory_chars` | 233 | 0 |
| eval `memory_injection_count` | 1 | 1 |
| eval `used_expected_signal` | true | true |
| eval avg score | 1.000 | 0.680 |
| Δ（with − without） | — | 0.320 |

without 的 eval 分解：

```text
grounding=1.0, content_correctness=0.0, share_correctness=1.0
基础 completion = 0.50
空 MEMORY.md 触发 memory artifact presence，+0.10
completion = 0.60
task_score = 0.8 × 0.60 + 0.2 × 1.0 = 0.68
```

## 结论

- 空记忆文件让 `used_expected_signal=true`，解除了 0.25 cap（0.400 → 0.600）。
- 空文件同时被 `require_memory_artifact` 计为 artifact presence，额外 +0.08 task（0.600 → 0.680）。
- 论文 SM01 without 0.600 对应“used=true、无 artifact 加分”，最可能来自 agent 主动调用 memory 工具；qwen 在 eval 的 `memory_read_count=0`，不会主动读取。
- 本 run 是口径核验实验，不进入主表。

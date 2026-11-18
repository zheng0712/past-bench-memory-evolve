# SM03 冒烟运行报告

## 1. 基本信息

| 项 | 值 |
|---|---|
| 任务族 | `update_ability/SM03_fact_correction` |
| Episode 数 | 7（cold 1 / update 1 / eval_near 1 / eval_far 1 / control 3） |
| Agent | `hermes` |
| 模型 | `qwen3.5-plus`（中转站 `https://uniapi.thingo.com.cn/v1`） |
| Judge | `qwen3.5-plus`（与 agent 同模型，评分噪声偏大） |
| Runtime | `local` + `--sandbox --sandbox-tools` |
| 变体 | `--compare-no-persistence`（with / without 配对） |
| 结果目录 | `experiments/20261118_sm03_hermes_smoke/` |

复现命令：

```bash
cd ~/work/pbme/benchmarks/PAST-Bench
source .venv/bin/activate
export QWEN_API_KEY='...'
past-bench evolve \
  --family update_ability/SM03_fact_correction \
  --agent hermes --agent-profile qwen \
  --runtime local --sandbox --sandbox-tools \
  --compare-no-persistence \
  --registry ~/work/pbme/configs/agents.yaml \
  --config ~/work/pbme/config.yaml \
  --trace-dir ~/work/pbme/experiments/20261118_sm03_hermes_smoke
```

## 2. 汇总结果

| 指标 | with_persistence | without_persistence |
|---|---|---|
| baseline（cold）平均分 | 0.6 | 0.6 |
| evaluation 平均分 | **1.0** | 0.704 |
| evaluation 通过率 | **100%** | 0% |
| 相对基线 delta | +0.4 | +0.104 |
| write precision | 0.833 | 0.333 |
| recall accuracy | 1.0 | 0.0 |
| update correctness | 1.0 | 0.5 |
| retention horizon | 1.0 | 1.0 |
| memory pollution rate | 0.5 | 0.0 |
| mechanism score | 0.867 | 0.567 |
| evolve score | 0.347 | 0.059 |

`sequence_comparison.json` 的 delta：

| 字段 | 值 |
|---|---|
| `evaluation_avg_task_score` | +0.296 |
| `evaluation_pass_rate` | +1.0 |
| `avg_outcome_delta` | +0.296 |
| `ablation_evolve_score` | +0.257 |
| `avg_mechanism_score` | +0.3 |
| `strong_attribution_families` | 0 |

## 3. 逐 episode

| task_id | with 分数 | with 通过 | without 分数 | without 通过 |
|---|---|---|---|---|
| SM03_COLD_001 | 0.6 | 否 | 0.6 | 否 |
| SM03_UPDATE_001 | 1.0 | 是 | 0.56 | 否 |
| SM03_EVAL_NEAR_001 | 1.0 | 是 | 0.704 | 否 |
| SM03_EVAL_FAR_001 | 1.0 | 是 | 0.704 | 否 |
| SM03_CONTROL_001 | 1.0 | 是 | 1.0 | 是 |
| SM03_CONTROL_002 | 1.0 | 是 | 1.0 | 是 |
| SM03_CONTROL_003 | 0.6 | 否 | 0.6 | 否 |

关键点：without 的 eval 平均分有 0.704，但 `content_correctness` 全为 0，`corrected_freeze_date` 全为 0，所以通过率为 0。**分数不等于通过，"改对了日期"这个硬条件没满足。**

## 4. 异常与待核查

| 现象 | 观察 | 判断 |
|---|---|---|
| without 仍有 memory/skill 文件 | 两个变体的 cold 阶段都有 676 字符初始 memory 和 `phoenix-rollout-review` skill | 属于任务预置 fixture，不是串数据；区分点是 without 的 memory 停在 676 字符未更新，with 更新为 647 |
| memory pollution rate = 0.5 | with 变体一半记忆条目被判为污染 | 需要看 SM03 expectations 的污染判定口径，暂不当作 bug |
| judge 分数抖动 | without 的 eval judge 只有 0.35~0.5，task_score 仍为 0.704 | qwen 兼任 judge 不稳定；pass 由确定性组件决定，暂不影响结论 |
| 耗时离群 | without 的 COLD 210s、EVAL_FAR 240s，其余约 20~80s | 疑似中转站超时重试，需在日志里确认是否有 retry |

## 5. 结论与下一步

1. 两个 family 方向一致：关掉持久化后，eval 阶段通过率从 100% 掉到 0。
2. SM03 的 delta（+0.296）小于 SM01（+0.6），符合"事实纠正比偏好采纳更难"的预期。
3. 待办：
   - 核查 without 变体里记忆为何能写入（write precision 0.333），确认 no-persistence 的语义边界；
   - 核查 EVAL_FAR 的 240s 是否伴随 API 重试；
   - 与 SM01 合并出第一张实验表。

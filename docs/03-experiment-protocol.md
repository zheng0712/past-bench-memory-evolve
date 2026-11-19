# 实验协议

## 1. 配对运行

每个 run 用 `--compare-no-persistence` 同时跑两个变体：

- `with_persistence`：持久化开启，允许跨 episode 复用记忆/技能/会话；
- `without_persistence`：持久化关闭，用于 paired 对照。

```text
experiments/<run>/
├── cmd.txt
├── with_persistence/sequence_results.json
├── with_persistence/sequence_summary.json
├── without_persistence/sequence_results.json
├── without_persistence/sequence_summary.json
└── shared_cold/                 # SM01 的共享 cold baseline
```

## 2. 有效 run 判定

一个 run 只有在以下条件全部满足时才进入有效实验表：

1. with 与 without 两个变体都完整产出；
2. 两个变体都没有 `(no response)` 空响应；
3. 没有 `infra_blocked`；
4. 没有 provider 403（`AccessDenied.Unpurchased`）。

不满足的 run 保留原始目录，在报告中单列为无效证据，不进入均值。

## 3. Bucket

| bucket | 作用 |
|---|---|
| `baseline`（cold） | 教任何东西之前的冷启动 |
| `learn` | 注入信号；`learn_b` 后会插入 reflection（SM01） |
| `update` | 纠正旧事实（SM03） |
| `evaluation` | `eval_near` / `eval_far`，移除触发语 |
| `control` | `no_persistence` / `shortcut` / `wrong_mechanism` |
| `reflection` | 运行期生成，无评分，不进入 t3 分母 |

## 4. 指标

- `task_score = 0.8 × completion + 0.2 × robustness`
- `completion = 0.2 × grounding + 0.5 × content_correctness + 0.3 × share_correctness`
- `hard_pass` 要求 `task_score ≥ 1.0`
- family 级字段：`baseline_avg_score`、`evaluation_avg_score`、`avg_family_task_score_delta`、`evaluation_pass_rate`、`avg_write_precision`、`avg_recall_accuracy`、`avg_update_correctness`、`avg_retention_horizon`、`avg_memory_pollution_rate`、`avg_mechanism_score`、`avg_evolve_score`

逐字段定义见 `reports/experiment-report.md` §3 和 PAST-Bench `runner/self_evolve.py`。

## 5. 问题记录

所有问题统一记录在 `reports/experiment-report.md` §2「问题台账」，同一模板：

```text
ID / 类别 / 问题 / 范围 / 频率 / 原文依据 / 影响 / 性质 / 处理建议
```

性质分为：非预期缺陷、预期基线、执行故障、耗时注释、设计口径、评判器噪声。不同性质不混算成同一个失败率。

## 6. Judge

- 当前 judge 与被测 agent 同为 `qwen3.5-plus`；
- judge 只看 `task.prompt`、conversation、actions、`judge_rubric`，不读 `expectations.json`；
- `judge_score` 只进入 `communication`，不进入 `task_score` / `hard_pass`；
- 换独立 judge（论文用 MiniMax-M2.7）并做校准后，才把 judge 值用于分析。

## 7. 复现

```bash
cd ~/work/pbme
python scripts/profile_dataset.py --out reports/tables
python scripts/collect_results.py \
  --runs experiments/<run1> experiments/<run2> \
  --out reports/tables
```

不要覆盖历史 run；新实验用新的 `--run-id`。

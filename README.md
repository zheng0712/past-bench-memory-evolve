# past-bench-memory-evolve

在 **PAST-Bench** 上跑「Agent 运行时记忆自进化」基线：固定 **Hermes + qwen3.5-plus**，比较持久化开启（with）与关闭（without）的差异。

当前覆盖两个 family：

- `SM01_preference_adoption`（memory_ability）
- `SM03_fact_correction`（update_ability）

完整实验报告见 **[reports/experiment-report.md](reports/experiment-report.md)**。

## 结果速览

只统计有效 run（with/without 都无空响应、无 infra、无 403）。每个 family 3 个有效 run。

| family | with eval | without eval | Δ（with − without） | with pass |
|---|---:|---:|---:|---:|
| SM01_preference_adoption | 0.852 ± 0.148 | 0.400 | 0.452 ± 0.148 | 50% |
| SM03_fact_correction | 1.000 ± 0.000 | 0.704 | 0.296 ± 0.000 | 100% |

三点说明：

- `judge_score` 只写入 `communication`，不进入 `task_score`，也不与论文 judge 对比。
- SM03 run2 的 without 变体、run3 的两个变体有空响应（run3 伴随 403），已作为无效 run 剔除；原始数据在报告 §5。
- without 口径核验实验单独列在报告 §4，不并入上表。

## 目录

```text
.
├── benchmarks/PAST-Bench/   # submodule，只读
├── configs/agents.yaml      # agent registry（含 qwen profile）
├── config.yaml              # judge 配置
├── scripts/
│   ├── run_baseline.sh      # 跑一个 family 的 paired run
│   ├── collect_results.py   # 生成 t1–t4
│   └── profile_dataset.py   # 生成数据集画像 t0
├── experiments/<run>/       # 每次运行一个目录
├── patches/                 # 为对齐原文做的上游代码改动
├── reports/                 # 实验报告与表格
└── docs/                    # dataset card / Hermes 接入 / 实验协议
```

## 跑一次实验

前置：WSL2 + Docker、`benchmarks/PAST-Bench` 已装好 Python 环境、`past-bench-agent:latest` 镜像已构建。详见 [docs/02-hermes-setup.md](docs/02-hermes-setup.md)。

```bash
cd ~/work/pbme
export QWEN_API_KEY=...

# 跑一个 family（会同时跑 with / without）
bash scripts/run_baseline.sh \
  --family memory_ability/SM01_preference_adoption \
  --run-id 20261119_sm01_run4

# 汇总多个 run
python scripts/collect_results.py \
  --runs experiments/20261118_sm01_hermes_smoke \
         experiments/20261119_sm01_run2 \
         experiments/20261119_sm01_run3 \
  --out reports/tables
```

每次 run 产出：

```text
experiments/<run>/
├── cmd.txt                     # 本次运行的完整命令
├── with_persistence/
│   ├── sequence_results.json   # 逐 episode 原始结果
│   ├── sequence_summary.json   # family 指标
│   └── ...
├── without_persistence/
└── shared_cold/                # SM01 的共享 cold baseline
```

## 怎么看结果

1. **主报告**：`reports/experiment-report.md`
   - §1 有效实验表
   - §2 问题台账（所有问题统一记录）
   - §3 按原始评分要求的分析
   - §4 without 口径核验实验
   - §5 全部原始数据（含无效 run）
2. **表格**：`reports/tables/t0_dataset_profile.*`、`t1_baseline.*`、`t2_episodes.*`、`t3_failures.*`、`t4_stability.*`
3. **单次运行**：`experiments/<run>/with_persistence/sequence_results.json`

## 已知问题

- **SM01 最终回复没有 TSV**：39/48 条非空记录（81.3%），其中 6 条只差 TSV；见报告 §2 `ISS-01`。
- **SM01 without 恒为 0.400**：空 state 下没有记忆注入，qwen 也不主动调用 memory，触发 `missing_retrieval_cap`；核验见报告 §4。
- **SM03 403/空响应**：run2 without 5/7、run3 14/14；已从有效表剔除，原始证据在报告 §5.5。
- **慢 episode**：`wall_time_s>200s` 只标注，不当作失败；报告 §5.6。

## 下一步

1. 换独立 judge（论文用 MiniMax-M2.7），做 12 条校准，重判已有 trace。
2. 扩大 family 与 run 数，统计大规模问题比例。
3. 如需改上游 prompt/grader（SM01 TSV 表述），先单独开分支，避免影响与官方基线的可比性。
4. 如需复现论文 SM01 without 0.600，换 MiniMax-M2.7 验证主动检索行为。

# past-bench-memory-evolve

PAST-Bench 上「Agent 运行时记忆自进化」的基线实验工程（当前为骨架）。

- 基准：PAST-Bench（git submodule，位于 `benchmarks/PAST-Bench`，只读）
- Agent：Hermes full setup（WSL2 + Docker）
- 模型：qwen3.5-plus（主）/ qwen3-coder-plus（代码类任务）
- 任务：SM01_preference_adoption、SM03_fact_correction

## 目录结构

```text
.
├── benchmarks/PAST-Bench/     # submodule，锁定 commit，不修改
├── configs/                   # 模型 / agent / 任务配置
├── docs/                      # 数据集卡片、实验协议、Hermes 接入说明
├── experiments/               # 一次运行一个目录
│   └── _template/
├── prompts/                   # judge / 任务包装提示词（带版本号）
├── reports/                   # 汇总表格与图
├── scripts/                   # 只做编排，逻辑放 src/pbme
└── src/pbme/                  # dataset / adapters / runner / judge / analysis
```

## 快速开始

```bash
git clone --recursive <repo-url>
cp .env.example .env          # 填入 Qwen Key 与 WSL 内路径
make env-check                # 环境自检
make profile                  # 数据集剖析 -> reports/tables
make smoke                    # 生成小批量样本清单
make run                      # 跑基线
make collect                  # 汇总 results.jsonl
make table                    # 出实验表
```

## 实验目录约定

`experiments/YYYYMMDD_<task>_<agent>_<scale>/`，例如 `20261118_sm01_hermes_smoke30/`。

每次运行固定四件套：

| 文件 | 内容 |
|---|---|
| `config.yaml` | 本次运行的完整配置快照（含样本清单哈希） |
| `results.jsonl` | 逐条结果 |
| `errors/` | 失败样本原始日志 |
| `report.md` | 失败类型分布与比例、结论 |

## results.jsonl 字段

| 字段 | 说明 |
|---|---|
| `run_id` | 运行标识 |
| `task_id` | 数据集内任务 ID |
| `split` | learn / eval_near / eval_far / control |
| `agent` | hermes_full / pi / no_memory |
| `model` | 模型名 |
| `turn` | 轮次 |
| `metric` | 指标名 |
| `score` | 得分 |
| `passed` | 是否通过 |
| `error_type` | 失败分类，见 docs/03-experiment-protocol.md |
| `latency_ms` | 耗时 |
| `input_tokens` / `output_tokens` | token 消耗 |

## 当前状态

- [x] 数据集剖析与 dataset card
- [ ] Hermes 容器接入
- [x] SM01 小批量冒烟
- [ ] SM01 全量基线
- [x] SM03 小批量冒烟
- [ ] SM03 全量基线

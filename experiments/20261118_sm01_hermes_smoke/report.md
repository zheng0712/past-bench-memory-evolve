# SM01 冒烟运行报告

## 1. 基本信息

| 项 | 值 |
|---|---|
| 任务族 | `memory_ability/SM01_preference_adoption` |
| Episode 数 | 8（cold 1 / learn 2 / eval_near 1 / eval_far 1 / control 3） |
| Agent | `hermes` |
| 模型 | `qwen3.5-plus`（中转站 `https://uniapi.thingo.com.cn/v1`） |
| Judge | `qwen3.5-plus` |
| Runtime | `local` + `--sandbox --sandbox-tools`（镜像 `past-bench-agent:latest`） |
| 变体 | `--compare-no-persistence`（with / without 配对） |
| 结果目录 | `experiments/20261118_sm01_hermes_smoke/` |

复现命令：

```bash
cd ~/work/pbme/benchmarks/PAST-Bench
source .venv/bin/activate
export QWEN_API_KEY='...'
past-bench evolve \
  --family memory_ability/SM01_preference_adoption \
  --agent hermes --agent-profile qwen \
  --runtime local --sandbox --sandbox-tools \
  --compare-no-persistence \
  --registry ~/work/pbme/configs/agents.yaml \
  --config ~/work/pbme/config.yaml \
  --trace-dir ~/work/pbme/experiments/20261118_sm01_hermes_smoke
```

## 2. 结果

cold episode 只跑一次（`shared_cold/`），两个变体共用同一基线，因此 baseline 分数一致。

| 指标 | with_persistence | without_persistence |
|---|---|---|
| baseline（cold）平均分 | 0.6 | 0.6 |
| evaluation 平均分 | **1.0** | 0.4 |
| evaluation 通过率 | **100%** | 0% |
| 相对基线 delta | +0.4 | -0.2 |
| memory artifacts（family 数） | 1 | 0 |
| write precision | 1.0 | 0.0 |
| recall accuracy | 1.0 | 0.0 |
| update correctness | 0.833 | 0.0 |
| retention horizon | 1.0 | 1.0 |
| memory pollution rate | 0.0 | 0.0 |
| mechanism score | 0.967 | 0.4 |
| evolve score | 0.387 | 0.0 |

`sequence_comparison.json` 的 delta：

| 字段 | 值 |
|---|---|
| `evaluation_avg_task_score` | +0.6 |
| `evaluation_pass_rate` | +1.0 |
| `avg_outcome_delta` | +0.6 |
| `ablation_evolve_score` | +0.58 |
| `avg_mechanism_score` | +0.567 |
| `strong_attribution_families` | 0 |

## 3. 失败与异常

| 项 | 情况 |
|---|---|
| 基础设施失败 | `families_with_infra_blocks = 0`，容器、mock service、模型调用均正常 |
| bootstrap | 首次运行需 `pip install -e agents/hermes-agent`，成功后写入 `.runtime_cache/hermes.ready` |
| 样本量 | 仅 1 个 family，`strong_attribution_families = 0`，不能作为强归因结论 |

## 4. 结论与下一步

1. 链路已打通：sandbox、mock service（notes）、模型调用、配对消融均正常。
2. 去掉持久化后 eval 阶段从 1.0 掉到 0.4、通过率从 100% 掉到 0，记忆作用被分离出来，方向符合预期。
3. 下一步：
   - 用同样配置跑 `update_ability/SM03_fact_correction`；
   - 两个 family 结果合并成第一张实验表（`reports/tables/t1_baseline.csv`）；
   - 若有 MiniMax key，将 judge 换回 `MiniMax-M2.7` 后复跑，核对 judge 偏差。

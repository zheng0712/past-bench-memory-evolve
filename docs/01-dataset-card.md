# 数据集卡片：PAST-Bench（待填）

> 讲解用文档，结论全部以 `benchmarks/PAST-Bench` 实际文件为准。

## 1. 来源与构建方式

- 仓库：`benchmarks/PAST-Bench`
- 任务定义：`self-evolve-tasks-v2/`
- 任务族：memory_ability / update_ability / procedural_ability / proactive_information_gathering
- 构建流程：TODO（读 README 与生成脚本后补）

## 2. 任务结构

| 字段 | 说明 |
|---|---|
| `family.yaml` | TODO |
| learn_* | TODO |
| eval_near / eval_far | TODO |
| control_* | TODO |

## 3. 我负责的任务

- SM01_preference_adoption：`self-evolve-tasks-v2/memory_ability/SM01_preference_adoption`
- SM03_fact_correction：`self-evolve-tasks-v2/update_ability/SM03_fact_correction`

## 4. 指标

TODO：名称、判定方式、脚本位置、是否 LLM judge、随机性控制。

## 5. 统计

TODO：样本量、轮次分布、learn/eval 配比、控制组设计。

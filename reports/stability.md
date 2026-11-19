# 重复运行稳定性分析

对象：SM01、SM03 各 3 次同配置运行（Hermes + qwen3.5-plus，runtime local，sandbox 开启，paired no-persistence）。

## 1. 逐 run 结果

| run | family | with eval | without eval | delta | with pass | without pass |
|---|---|---:|---:|---:|---:|---:|
| 20261118_sm01_hermes_smoke | SM01 | 1.000 | 0.400 | 0.600 | 100% | 0% |
| 20261119_sm01_run2 | SM01 | 0.852 | 0.400 | 0.452 | 50% | 0% |
| 20261119_sm01_run3 | SM01 | 0.704 | 0.400 | 0.304 | 0% | 0% |
| 20261118_sm03_hermes_smoke | SM03 | 1.000 | 0.704 | 0.296 | 100% | 0% |
| 20261119_sm03_run2 | SM03 | 1.000 | 0.384 | 0.616 | 100% | 0% |
| 20261119_sm03_run3 | SM03 | 0.304 | 0.304 | 0.000 | 0% | 0% |

## 2. 聚合

| family | runs | with eval | delta | with pass | evolve score |
|---|---:|---|---|---|---|
| SM01 | 3 | 0.852 ± 0.148 | 0.452 ± 0.148 | 0.500 ± 0.500 | 0.226 ± 0.157 |
| SM03 | 3 | 0.768 ± 0.402 | 0.304 ± 0.308 | 0.667 ± 0.577 | 0.264 ± 0.179 |

标准差接近甚至超过均值，说明**单次运行不足以支撑结论**。

## 3. 根因

### SM01 run3：记忆注入成功，但格式没遵守

`SM01_EVAL_NEAR_001`（with）：

- `memory_injection_count = 1`、`used_expected_signal = True`、`artifact_quality_score = 1.0`
- `task_score = 0.704`，`content_correctness = 0`，`recall_accuracy = 0`

对比两次最终输出：

- run1：输出 **TSV**（`owner\tpriority\ttask\tdue_date`），符合学到的偏好
- run3：输出 **Markdown 表格**，与偏好冲突

说明失败点不在检索或记忆写入，而在**模型对已注入偏好的遵循不稳定**。

### SM03 run3：空响应，属于无效 run

- `SM03_UPDATE_001`、`SM03_EVAL_NEAR_001`、`SM03_EVAL_FAR_001` 在 with/without 两个变体里都是 `"(no response)"`，共 8 条
- 对应 `task_score` 0.28 / 0.304，`judge_score = 0.0`，但 `infra_blocked = false`

也就是说：**运行器没有把它标记为基础设施失败，评测却给了低分**，容易被误读成"记忆无效"。这类 run 应判为无效并重跑。

## 4. 对结论的影响

1. 之前基于 run1 的"记忆带来 +0.6 / +0.296 提升"不能直接作为结论，只能作为方向性观察。
2. 需要以 3 次以上**有效 run** 的均值 ± 标准差报告；SM03 run3 应剔除后补跑。
3. 失败分类已新增 `empty_response`：当前 90 条有评分 episode 中 8 条（8.9%），SM03 全部来自 run3。

## 5. 下一步

1. 补跑 SM03（run4）和 SM01（run4），确保每个 family 有 3 个有效 run
2. 每次 run 后先检查 `empty_response` 与 `timeout` 数量，异常 run 直接重跑
3. 若格式遵循问题持续出现，再考虑在实验记录中区分"检索成功但未采纳"与"未检索"两类失败

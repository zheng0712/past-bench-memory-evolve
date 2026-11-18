# 失败分类与比例 t3

分母：30 条有评分的 episode（with/without 合计）；另有 2 条 reflection 等无评分记录不参与比例。每条只记一个主类别，优先级：infra > timeout > pass_score_mismatch > judge_mismatch > persistence_anomaly。

| error_type | 条数 | 占比 | 典型案例 |
|---|---:|---:|---|
| infra_blocked | 0 | 0.0% | - |
| timeout | 2 | 6.7% | SM03_COLD_001; SM03_EVAL_FAR_001 |
| pass_score_mismatch | 3 | 10.0% | SM01_LEARN_A_001; SM01_LEARN_B_001; SM03_EVAL_NEAR_001 |
| judge_mismatch | 3 | 10.0% | SM01_LEARN_A_001; SM01_EVAL_FAR_001; SM03_UPDATE_001 |
| persistence_anomaly | 0 | 0.0% | - |
| none | 22 | 73.3% | SM01_COLD_001; SM01_EVAL_NEAR_001; SM01_EVAL_FAR_001 |

## family 级异常

| run | family | variant | pollution | write_precision | recall | infra_blocks |
|---|---|---|---:|---:|---:|---:|
| 20261118_sm01_hermes_smoke | SM01_preference_adoption | with_persistence | 0.000 | 1.000 | 1.000 | 0 |
| 20261118_sm01_hermes_smoke | SM01_preference_adoption | without_persistence | 0.000 | 0.000 | 0.000 | 0 |
| 20261118_sm03_hermes_smoke | SM03_fact_correction | with_persistence | 0.500 | 0.833 | 1.000 | 0 |
| 20261118_sm03_hermes_smoke | SM03_fact_correction | without_persistence | 0.000 | 0.333 | 0.000 | 0 |

口径说明：`write_precision` 取自 learn 阶段的 `avg_artifact_quality_score`，衡量 artifact 质量，不是写入次数；no-persistence 下非 0 属正常。

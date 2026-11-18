# 数据集画像 t0

任务根目录：`benchmarks/PAST-Bench/self-evolve-tasks-v2`

| ability | families | episodes | orphan dirs | missing task.yaml |
|---|---:|---:|---:|---:|
| memory_ability | 5 | 41 | 0 | 0 |
| proactive_information_gathering | 6 | 48 | 6 | 0 |
| procedural_ability | 8 | 64 | 0 | 0 |
| update_ability | 7 | 51 | 7 | 0 |

| family | ability | episodes | cold | learn | update | near | far | control | grader | expectations | services |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| EP01_prior_case_recall | memory_ability | 8 | 1 | 2 | 0 | 1 | 1 | 3 | 8 | 8 | notes |
| EP02_exception_list_recall | memory_ability | 8 | 1 | 2 | 0 | 1 | 1 | 3 | 8 | 8 | config |
| SM01_preference_adoption | memory_ability | 8 | 1 | 2 | 0 | 1 | 1 | 3 | 8 | 8 | notes |
| SM02_constraint_retention | memory_ability | 8 | 1 | 2 | 0 | 1 | 1 | 3 | 8 | 8 | notes |
| SM05_weak_trigger_preference_adoption | memory_ability | 9 | 1 | 2 | 1 | 1 | 1 | 3 | 9 | 9 | notes |
| PG01_release_decision_followup | proactive_information_gathering | 8 | 0 | 0 | 1 | 2 | 1 | 2 | 8 | 8 | notes |
| PG02_ops_exception_desk | proactive_information_gathering | 8 | 0 | 0 | 1 | 2 | 1 | 2 | 8 | 8 | helpdesk |
| PG03_oncall_handoff_lookup | proactive_information_gathering | 8 | 0 | 0 | 1 | 2 | 1 | 2 | 8 | 8 | helpdesk |
| PG04_temporary_waiver_audit | proactive_information_gathering | 8 | 0 | 0 | 1 | 2 | 1 | 2 | 8 | 8 | notes |
| PG05_change_freeze_followup | proactive_information_gathering | 8 | 0 | 0 | 1 | 2 | 1 | 2 | 8 | 8 | notes |
| PG06_kappa_integration_review | proactive_information_gathering | 8 | 0 | 0 | 1 | 2 | 1 | 2 | 8 | 8 | notes |
| PC01_sop_bootstrap_01 | procedural_ability | 8 | 1 | 1 | 1 | 1 | 1 | 3 | 8 | 8 | helpdesk;kb |
| PC01_sop_bootstrap_02 | procedural_ability | 8 | 1 | 1 | 1 | 1 | 1 | 3 | 8 | 8 | helpdesk;kb |
| PC01_sop_bootstrap_03 | procedural_ability | 8 | 1 | 1 | 1 | 1 | 1 | 3 | 8 | 8 | helpdesk;kb |
| PC01_sop_bootstrap_04 | procedural_ability | 8 | 1 | 1 | 1 | 1 | 1 | 3 | 8 | 8 | helpdesk;kb |
| PC01_sop_bootstrap_05 | procedural_ability | 8 | 1 | 1 | 1 | 1 | 1 | 3 | 8 | 8 | plonk;kb |
| PC01_sop_bootstrap_06 | procedural_ability | 8 | 1 | 1 | 1 | 1 | 1 | 3 | 8 | 8 | x_mock;kb |
| PC03_latent_rule_induction_01 | procedural_ability | 7 | 1 | 2 | 0 | 1 | 1 | 2 | 7 | 7 | helpdesk;kb |
| PC04_failure_to_rule_01 | procedural_ability | 9 | 1 | 0 | 0 | 1 | 1 | 3 | 9 | 9 | helpdesk;kb |
| EP03_recall_then_modify | update_ability | 7 | 1 | 0 | 1 | 1 | 1 | 3 | 7 | 7 | notes |
| PC02_sop_patch_01 | update_ability | 7 | 1 | 0 | 1 | 1 | 1 | 3 | 7 | 7 | helpdesk;kb |
| PC02_sop_patch_02 | update_ability | 7 | 1 | 0 | 1 | 1 | 1 | 3 | 7 | 7 | helpdesk;kb |
| SM03_fact_correction | update_ability | 7 | 1 | 0 | 1 | 1 | 1 | 3 | 7 | 7 | notes |
| SM04_rule_migration | update_ability | 7 | 1 | 0 | 1 | 1 | 1 | 3 | 7 | 7 | notes |
| SM06_temporary_exception_pollution | update_ability | 8 | 1 | 0 | 1 | 2 | 1 | 3 | 8 | 8 | notes |
| SM07_scoped_rule_migration | update_ability | 8 | 1 | 0 | 1 | 2 | 1 | 3 | 8 | 8 | notes |

说明：`orphan dirs` 指目录存在但不在 `episode_order` 中的 episode 目录；`missing task.yaml` 指 `episode_order` 中缺少任务定义的条目。

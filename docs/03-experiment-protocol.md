# 实验协议

## 1. 两阶段执行

1. **冒烟**：每任务抽 30 条（覆盖 learn/eval/control），只验证链路。
2. **全量**：冒烟通过且失败原因归类完毕后执行。

冒烟阶段产出一份 `experiments/<run>/report.md`，内容包括：

- 成功条数 / 失败条数 / 失败比例
- 每个 `error_type` 的条数与典型案例
- 是否阻塞全量（结论：可跑 / 需修 / 需换配置）

## 2. 失败分类（固定口径）

| error_type | 含义 |
|---|---|
| `env_error` | 容器、路径、依赖、模型鉴权 |
| `agent_crash` | agent 进程异常退出 |
| `tool_error` | 工具调用报错（含代码执行） |
| `timeout` | 单任务超时 |
| `judge_error` | 评测脚本或 judge 失败 |
| `memory_miss` | 链路正常但记忆未生效 |
| `policy_violation` | 违反任务约束 |
| `data_bad` | 数据集本身缺文件/格式错 |

## 3. 可复现要求

- 每个 run 目录保存完整 `config.yaml` 与样本清单哈希
- 温度固定 0.0，seed 固定；模型名写全称
- 结果只追加，不覆盖历史 run

# Judge Prompt 模板（v0，待按论文附录补齐）

用途：判定 SM01 / SM03 单条轨迹是否达成目标。

## 输入

- 任务描述
- 对话轨迹 / 工具调用记录
- 期望行为

## 输出（严格 JSON）

```json
{"passed": true, "reason": "..."}
```

## 注意

- 判定只依据轨迹，不脑补
- 不确定时输出 passed=false，并在 reason 说明

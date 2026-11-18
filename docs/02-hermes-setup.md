# Hermes 接入说明（WSL2 + Docker full setup）

## 1. 运行位置

- Hermes 安装在 WSL2 内，通过 Docker 运行 full setup。
- 本仓库在 Windows 工作区，WSL 内通过 `/mnt/c/...` 访问；跑实验时建议在 WSL 内 clone 一份，避免跨文件系统 I/O 影响。

## 2. 调用方式

TODO：补充实际命令（容器名、挂载目录、环境变量、结果回读路径）。

```bash
# 示例占位，按实际环境修改
docker exec -it hermes bash
```

## 3. 与 runner 的约定

- 输入：任务目录 + 模型配置 + 运行目录
- 输出：`results.jsonl`、原始日志到 `experiments/<run>/logs/`
- 失败必须落 `error_type`，禁止静默跳过

## 4. 已知问题

TODO：小批量冒烟时逐条记录。

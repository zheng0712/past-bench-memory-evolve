# Hermes 接入说明

## 1. 用的是哪个 Hermes

PAST-Bench 的 self-evolve v2 使用仓库自带的 **`agents/hermes-agent`（pip 包）**，通过 `--runtime local` 直接调用。

它**不使用**用户自己的 Hermes full setup / Docker 容器。Docker 只用于 `--sandbox` 的工具沙箱（shell / file / browser），镜像为 `past-bench-agent:latest`。

## 2. 首次准备（WSL2）

```bash
cd ~/work/pbme/benchmarks/PAST-Bench

# 1) Python 3.11+ 虚拟环境
python3.11 -m venv .venv
source .venv/bin/activate

# 2) 安装 PAST-Bench 与自带 Hermes
pip install -e .
pip install -e agents/hermes-agent

# 3) 构建 sandbox 工具镜像
past-bench build-image --kind sandbox

# 如果 Docker Hub 不通，用镜像加速：
# docker build --build-arg REGISTRY=docker.m.daocloud.io \
#   -t past-bench-agent:latest -f Dockerfile.agent .
```

## 3. 运行

```bash
export QWEN_API_KEY=...
cd ~/work/pbme

bash scripts/run_baseline.sh \
  --family memory_ability/SM01_preference_adoption \
  --run-id 20261119_sm01_run4
```

`run_baseline.sh` 会固定：

```text
--runtime local --sandbox --sandbox-tools --compare-no-persistence
--registry <repo>/configs/agents.yaml
--config <repo>/config.yaml
--trace-dir <repo>/experiments/<run-id>
```

## 4. 常见问题

- **必须在 `benchmarks/PAST-Bench` 目录下启动**，否则 bootstrap 找不到 `agents/hermes-agent`。
- **不要用 `--runtime container`**：self-evolve 序列只支持 `--runtime local`；Docker 只作为 sandbox。
- **403 `AccessDenied.Unpurchased`**：中转站账号/渠道没有该模型权限，不是 max_tokens；先单请求探测，再重跑。

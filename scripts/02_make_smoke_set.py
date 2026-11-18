"""02 生成小批量冒烟样本清单（分层抽样，覆盖 learn/eval/control）。"""

from __future__ import annotations

import sys


def main() -> int:
    # TODO: 按 configs/tasks/*.yaml 的 smoke_size 分层抽样
    #       输出 data/samples/<task>_smoke<N>.jsonl（记录样本 id 与哈希）
    print("[TODO] 冒烟样本生成未实现")
    return 1


if __name__ == "__main__":
    sys.exit(main())

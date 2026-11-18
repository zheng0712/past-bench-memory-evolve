#!/usr/bin/env python3
"""扫描 PAST-Bench 任务目录，生成数据集画像 t0。"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    raise SystemExit("需要 PyYAML：请在 PAST-Bench 的 venv 中运行，或 pip install pyyaml")


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] 读取失败 {path}: {exc}")
        return {}


def bucket_values(instances: dict[str, Any]) -> tuple[int, int, int, int, int, int]:
    """返回 cold / learn / update / eval_near / eval_far / control 的实例数。"""
    cold = int(instances.get("cold", 0) or 0)
    learn = sum(int(v or 0) for k, v in instances.items() if str(k).startswith("learn"))
    update = sum(int(v or 0) for k, v in instances.items() if "update" in str(k) or "stabilize" in str(k))
    eval_near = int(instances.get("eval_near", 0) or 0)
    eval_far = int(instances.get("eval_far", 0) or 0)
    control = int(instances.get("control", 0) or 0)
    return cold, learn, update, eval_near, eval_far, control


def family_row(family_dir: Path, ability: str) -> dict[str, Any]:
    family = load_yaml(family_dir / "family.yaml")
    episode_order = family.get("episode_order") or []
    dirs = sorted(p.name for p in family_dir.iterdir() if p.is_dir())
    orphans = sorted(set(dirs) - set(episode_order))
    cold, learn, update, near, far, control = bucket_values(family.get("instances_per_bucket") or {})

    services: list[str] = []
    with_grader = 0
    with_expectations = 0
    missing_task_yaml: list[str] = []
    for name in episode_order:
        ep_dir = family_dir / name
        if not (ep_dir / "task.yaml").exists():
            missing_task_yaml.append(name)
            continue
        task = load_yaml(ep_dir / "task.yaml")
        for svc in task.get("services") or []:
            svc_name = svc.get("name") if isinstance(svc, dict) else None
            if svc_name and svc_name not in services:
                services.append(svc_name)
        if (ep_dir / "grader.py").exists():
            with_grader += 1
        if (ep_dir / "expectations.json").exists():
            with_expectations += 1

    return {
        "family": family.get("family_id") or family_dir.name,
        "ability": family.get("ability_dir") or ability,
        "title": family.get("title"),
        "total_episodes": family.get("total_episodes") or len(episode_order),
        "episode_dirs": len(dirs),
        "episode_order": len(episode_order),
        "orphan_dirs": len(orphans),
        "cold": cold,
        "learn": learn,
        "update": update,
        "eval_near": near,
        "eval_far": far,
        "control": control,
        "with_grader": with_grader,
        "with_expectations": with_expectations,
        "missing_task_yaml": len(missing_task_yaml),
        "services": ";".join(services),
        "trigger_strength": family.get("trigger_strength"),
        "transfer_distance": family.get("transfer_distance"),
        "noise_profile": family.get("noise_profile"),
        "overwrite_mode": family.get("overwrite_mode"),
        "orphan_names": ";".join(orphans),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="生成 PAST-Bench 数据集画像 t0")
    parser.add_argument(
        "--tasks-root",
        default="benchmarks/PAST-Bench/self-evolve-tasks-v2",
        help="self-evolve-tasks-v2 目录",
    )
    parser.add_argument("--out", default="reports/tables", help="输出目录")
    args = parser.parse_args()

    root = Path(args.tasks_root)
    if not root.exists():
        raise SystemExit(f"找不到任务目录：{root}")

    rows = []
    for ability_dir in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith("_")):
        for family_dir in sorted(p for p in ability_dir.iterdir() if p.is_dir()):
            if not (family_dir / "family.yaml").exists():
                continue
            rows.append(family_row(family_dir, ability_dir.name))

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with (out_dir / "t0_dataset_profile.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    abilities: dict[str, dict[str, int]] = {}
    for row in rows:
        bucket = abilities.setdefault(row["ability"], {"families": 0, "episodes": 0, "orphans": 0, "missing_task": 0})
        bucket["families"] += 1
        bucket["episodes"] += int(row["total_episodes"] or 0)
        bucket["orphans"] += int(row["orphan_dirs"] or 0)
        bucket["missing_task"] += int(row["missing_task_yaml"] or 0)

    lines = [
        "# 数据集画像 t0",
        "",
        f"任务根目录：`{root}`",
        "",
        "| ability | families | episodes | orphan dirs | missing task.yaml |",
        "|---|---:|---:|---:|---:|",
    ]
    for ability, stats in sorted(abilities.items()):
        lines.append(
            f"| {ability} | {stats['families']} | {stats['episodes']} | {stats['orphans']} | {stats['missing_task']} |"
        )
    lines += [
        "",
        "| family | ability | episodes | cold | learn | update | near | far | control | grader | expectations | services |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['family']} | {row['ability']} | {row['total_episodes']} | {row['cold']} | {row['learn']} | "
            f"{row['update']} | {row['eval_near']} | {row['eval_far']} | {row['control']} | "
            f"{row['with_grader']} | {row['with_expectations']} | {row['services'] or '-'} |"
        )
    lines += [
        "",
        "说明：`orphan dirs` 指目录存在但不在 `episode_order` 中的 episode 目录；`missing task.yaml` 指 `episode_order` 中缺少任务定义的条目。",
        "",
    ]
    (out_dir / "t0_dataset_profile.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"families: {len(rows)}  -> {out_dir/'t0_dataset_profile.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

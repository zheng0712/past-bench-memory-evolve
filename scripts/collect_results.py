#!/usr/bin/env python3
"""把 PAST-Bench 的 paired-run 输出汇总成 t1 / t2 / t3 三张表。

输入：`experiments/<run>/sequence_comparison.json`
输出：`reports/tables/t1_baseline.{md,csv}`、`t2_episodes.{md,csv}`、`t3_failures.{md,csv}`
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path
from typing import Any

VARIANTS = ("with_persistence", "without_persistence")
TIMEOUT_WALL_S = 200.0
# 只有 learn / evaluation 阶段参与"分数-通过"与 judge 一致性判定；
# baseline、control、reflection 按设计就是非通过态或诊断态。
MEASURED_BUCKETS = {"learn", "evaluation"}


def load_comparison(run_dir: Path) -> dict[str, Any]:
    path = run_dir / "sequence_comparison.json"
    if not path.exists():
        raise SystemExit(f"缺少文件：{path}")
    return json.loads(path.read_text(encoding="utf-8"))


def first_family(variant: dict[str, Any]) -> str:
    families = variant.get("family_summary") or {}
    if families:
        return next(iter(families))
    episodes = variant.get("episodes") or []
    return episodes[0]["family_id"] if episodes else "unknown"


def episode_field(ep: dict[str, Any], *keys: str, default: Any = None) -> Any:
    cur: Any = ep
    for key in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(key)
    return default if cur is None else cur


def build_rows(run_name: str, comp: dict[str, Any]) -> tuple[list[dict], list[dict]]:
    family_rows: list[dict] = []
    episode_rows: list[dict] = []

    for variant_name in VARIANTS:
        variant = comp[variant_name]
        signal = variant.get("benchmark_signal") or {}
        family = first_family(variant)
        episodes = variant.get("episodes") or []

        family_rows.append(
            {
                "run": run_name,
                "family": family,
                "variant": variant_name,
                "episodes": len(episodes),
                "baseline_score": signal.get("baseline_avg_score"),
                "eval_score": signal.get("evaluation_avg_score"),
                "eval_pass_rate": signal.get("evaluation_pass_rate"),
                "delta_score": signal.get("avg_family_task_score_delta"),
                "mechanism_score": signal.get("avg_mechanism_score"),
                "evolve_score": signal.get("avg_evolve_score"),
                "write_precision": signal.get("avg_write_precision"),
                "recall_accuracy": signal.get("avg_recall_accuracy"),
                "update_correctness": signal.get("avg_update_correctness"),
                "pollution_rate": signal.get("avg_memory_pollution_rate"),
                "infra_blocks": signal.get("families_with_infra_blocks"),
            }
        )

        for ep in episodes:
            episode_rows.append(
                {
                    "run": run_name,
                    "family": family,
                    "variant": variant_name,
                    "task_id": ep.get("task_id"),
                    "bucket": ep.get("bucket") or ep.get("stage"),
                    "task_score": ep.get("task_score"),
                    "passed": ep.get("passed"),
                    "hard_pass": ep.get("hard_pass"),
                    "judge_score": ep.get("judge_score"),
                    "content_correctness": episode_field(ep, "task_components", "content_correctness"),
                    "grounding": episode_field(ep, "task_components", "grounding"),
                    "share_correctness": episode_field(ep, "task_components", "share_correctness"),
                    "turns": ep.get("total_turns"),
                    "wall_s": episode_field(ep, "timing", "wall_time_s"),
                    "input_tokens": episode_field(ep, "token_usage", "input_tokens", default=0),
                    "output_tokens": episode_field(ep, "token_usage", "output_tokens", default=0),
                    "infra_blocked": bool(ep.get("infra_blocked")),
                    "response_chars": len((ep.get("final_response_text") or "").strip()),
                    "memory_chars": episode_field(ep, "artifacts", "memory_chars", default=0),
                    "skill_count": episode_field(ep, "artifacts", "skill_count", default=0),
                }
            )

    return family_rows, episode_rows


def pct(count: int, total: int) -> str:
    return f"{(count / total * 100):.1f}%" if total else "0.0%"


def classify(rows: list[dict]) -> list[dict]:
    """每条 episode 只记一个主类别，优先级自上而下。"""
    cold_memory: dict[tuple[str, str], int] = {}
    for row in rows:
        if row["bucket"] == "baseline" and row["variant"] == "without_persistence":
            cold_memory[(row["run"], row["family"])] = row["memory_chars"] or 0

    result = []
    for row in rows:
        error = "none"
        wall = row["wall_s"] or 0
        judge = row["judge_score"] or 0
        measured = row["bucket"] in MEASURED_BUCKETS
        if row["infra_blocked"]:
            error = "infra_blocked"
        elif row["response_chars"] == 0 and measured:
            error = "empty_response"
        elif wall > TIMEOUT_WALL_S:
            error = "timeout"
        elif measured and row["task_score"] is not None and row["task_score"] >= 0.7 and not row["passed"]:
            error = "pass_score_mismatch"
        elif measured and ((judge >= 0.7 and not row["hard_pass"]) or (judge < 0.5 and row["hard_pass"])):
            error = "judge_mismatch"
        elif measured and row["variant"] == "without_persistence":
            base = cold_memory.get((row["run"], row["family"]), 0)
            if (row["memory_chars"] or 0) != base:
                error = "persistence_anomaly"
        result.append({**row, "error_type": error})
    return result


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fields})


def fmt(value: Any, digits: int = 3) -> str:
    if value is None:
        return "-"
    if isinstance(value, bool):
        return "是" if value else "否"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def main() -> int:
    parser = argparse.ArgumentParser(description="汇总 PAST-Bench paired-run 结果为 t1/t2/t3")
    parser.add_argument("--runs", nargs="+", required=True, help="一个或多个 experiments/<run> 目录")
    parser.add_argument("--out", default="reports/tables", help="输出目录")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    family_rows: list[dict] = []
    episode_rows: list[dict] = []
    signals: list[dict] = []

    for raw in args.runs:
        run_dir = Path(raw)
        comp = load_comparison(run_dir)
        f_rows, e_rows = build_rows(run_dir.name, comp)
        family_rows.extend(f_rows)
        episode_rows.extend(e_rows)
        for variant_name in VARIANTS:
            variant = comp[variant_name]
            signals.append(
                {
                    "run": run_dir.name,
                    "family": first_family(variant),
                    "variant": variant_name,
                    **(variant.get("benchmark_signal") or {}),
                }
            )

    classified = classify(episode_rows)

    # t1：family 级对照
    t1_fields = [
        "run", "family", "episodes",
        "with_eval", "without_eval", "delta",
        "with_pass", "without_pass", "pass_delta",
        "with_mech", "without_mech", "with_evolve", "without_evolve",
        "infra_blocks",
    ]
    t1_rows = []
    pairs: dict[tuple[str, str], dict[str, dict]] = {}
    for row in family_rows:
        pairs.setdefault((row["run"], row["family"]), {})[row["variant"]] = row
    for (run, family), variants in pairs.items():
        w = variants.get("with_persistence", {})
        o = variants.get("without_persistence", {})
        t1_rows.append(
            {
                "run": run,
                "family": family,
                "episodes": w.get("episodes") or o.get("episodes"),
                "with_eval": w.get("eval_score"),
                "without_eval": o.get("eval_score"),
                "delta": (w.get("eval_score") or 0) - (o.get("eval_score") or 0),
                "with_pass": w.get("eval_pass_rate"),
                "without_pass": o.get("eval_pass_rate"),
                "pass_delta": (w.get("eval_pass_rate") or 0) - (o.get("eval_pass_rate") or 0),
                "with_mech": w.get("mechanism_score"),
                "without_mech": o.get("mechanism_score"),
                "with_evolve": w.get("evolve_score"),
                "without_evolve": o.get("evolve_score"),
                "infra_blocks": (w.get("infra_blocks") or 0) + (o.get("infra_blocks") or 0),
            }
        )

    write_csv(out_dir / "t1_baseline.csv", t1_rows, t1_fields)
    lines = [
        "# 基线实验表 t1",
        "",
        f"来源：{', '.join(r['run'] for r in t1_rows)}",
        "",
        "| run | family | episodes | with eval | without eval | delta | with pass | without pass | pass delta | with mech | without mech | with evolve | without evolve | infra |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in t1_rows:
        lines.append(
            "| {run} | {family} | {episodes} | {with_eval} | {without_eval} | {delta} | {with_pass} | {without_pass} | {pass_delta} | {with_mech} | {without_mech} | {with_evolve} | {without_evolve} | {infra} |".format(
                run=row["run"], family=row["family"], episodes=row["episodes"],
                with_eval=fmt(row["with_eval"]), without_eval=fmt(row["without_eval"]),
                delta=fmt(row["delta"]),
                with_pass=fmt(row["with_pass"]), without_pass=fmt(row["without_pass"]),
                pass_delta=fmt(row["pass_delta"]),
                with_mech=fmt(row["with_mech"]), without_mech=fmt(row["without_mech"]),
                with_evolve=fmt(row["with_evolve"]), without_evolve=fmt(row["without_evolve"]),
                infra=row["infra_blocks"],
            )
        )
    lines += [
        "",
        "说明：`delta` 取 `sequence_comparison.json` 的 `evaluation_avg_task_score` 之差；`pass` 由确定性组件决定，不是 judge 分数。`episodes` 为运行期实际数，可能多于 `family.yaml` 的 `total_episodes`（如 reflection 阶段）。",
        "",
    ]
    (out_dir / "t1_baseline.md").write_text("\n".join(lines), encoding="utf-8")

    # t4：同一 family 重复运行的稳定性（均值 / 标准差）
    t4_rows = []
    empty_by_family: dict[str, int] = {}
    for row in classified:
        if row["error_type"] == "empty_response":
            empty_by_family[row["family"]] = empty_by_family.get(row["family"], 0) + 1
    by_family: dict[str, list[dict]] = {}
    for row in t1_rows:
        by_family.setdefault(row["family"], []).append(row)

    def stat(values: list[Any]) -> tuple[float, float, int]:
        clean = [float(v) for v in values if v is not None]
        if not clean:
            return 0.0, 0.0, 0
        return statistics.mean(clean), (statistics.stdev(clean) if len(clean) > 1 else 0.0), len(clean)

    for family, rows in sorted(by_family.items()):
        w_eval = stat([r["with_eval"] for r in rows])
        o_eval = stat([r["without_eval"] for r in rows])
        delta = stat([r["delta"] for r in rows])
        w_pass = stat([r["with_pass"] for r in rows])
        o_pass = stat([r["without_pass"] for r in rows])
        w_evolve = stat([r["with_evolve"] for r in rows])
        o_evolve = stat([r["without_evolve"] for r in rows])
        t4_rows.append(
            {
                "family": family,
                "runs": len(rows),
                "with_eval_mean": round(w_eval[0], 6),
                "with_eval_std": round(w_eval[1], 6),
                "without_eval_mean": round(o_eval[0], 6),
                "without_eval_std": round(o_eval[1], 6),
                "delta_mean": round(delta[0], 6),
                "delta_std": round(delta[1], 6),
                "with_pass_mean": round(w_pass[0], 6),
                "with_pass_std": round(w_pass[1], 6),
                "without_pass_mean": round(o_pass[0], 6),
                "without_pass_std": round(o_pass[1], 6),
                "with_evolve_mean": round(w_evolve[0], 6),
                "with_evolve_std": round(w_evolve[1], 6),
                "without_evolve_mean": round(o_evolve[0], 6),
                "without_evolve_std": round(o_evolve[1], 6),
                "empty_responses": empty_by_family.get(family, 0),
                "infra_blocks": sum(r["infra_blocks"] or 0 for r in rows),
            }
        )

    t4_fields = list(t4_rows[0].keys()) if t4_rows else ["family"]
    write_csv(out_dir / "t4_stability.csv", t4_rows, t4_fields)
    lines = [
        "# 重复运行稳定性 t4",
        "",
        f"来源 run 数：{len(t1_rows)}（按 family 聚合）。均值为算术平均，标准差为样本标准差（n≥2 时计算）。",
        "",
        "| family | runs | with eval | without eval | delta | with pass | without pass | with evolve | without evolve | empty resp | infra |",
        "|---|---:|---|---|---|---|---|---|---|---:|---:|",
    ]
    for row in t4_rows:
        def show(mean_key: str, std_key: str) -> str:
            return f"{row[mean_key]:.3f} ± {row[std_key]:.3f}"

        lines.append(
            f"| {row['family']} | {row['runs']} | {show('with_eval_mean', 'with_eval_std')} | "
            f"{show('without_eval_mean', 'without_eval_std')} | {show('delta_mean', 'delta_std')} | "
            f"{show('with_pass_mean', 'with_pass_std')} | {show('without_pass_mean', 'without_pass_std')} | "
            f"{show('with_evolve_mean', 'with_evolve_std')} | {show('without_evolve_mean', 'without_evolve_std')} | "
            f"{row['empty_responses']} | {row['infra_blocks']} |"
        )
    lines += [
        "",
        "说明：pass 为 0~1 比例；标准差反映同一配置重复运行时的波动。",
        "",
    ]
    (out_dir / "t4_stability.md").write_text("\n".join(lines), encoding="utf-8")

    # t2：逐 episode
    t2_fields = [
        "run", "family", "variant", "task_id", "bucket", "task_score", "passed",
        "hard_pass", "judge_score", "content_correctness", "grounding",
        "share_correctness", "turns", "wall_s", "input_tokens", "output_tokens",
        "infra_blocked", "response_chars", "memory_chars", "skill_count",
    ]
    write_csv(out_dir / "t2_episodes.csv", classified, t2_fields)
    lines = [
        "# 逐 episode 结果 t2",
        "",
        f"共 {len(classified)} 行（with/without 两个变体分别计数，含 reflection 等无评分阶段）。",
        "",
        "| run | variant | task_id | bucket | score | passed | hard | judge | content | turns | wall_s | tokens |",
        "|---|---|---|---|---:|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in classified:
        tokens = (row["input_tokens"] or 0) + (row["output_tokens"] or 0)
        lines.append(
            f"| {row['run']} | {row['variant']} | {row['task_id']} | {row['bucket']} | "
            f"{fmt(row['task_score'])} | {fmt(row['passed'])} | {fmt(row['hard_pass'])} | "
            f"{fmt(row['judge_score'])} | {fmt(row['content_correctness'])} | {row['turns']} | "
            f"{fmt(row['wall_s'], 1)} | {tokens} |"
        )
    lines.append("")
    (out_dir / "t2_episodes.md").write_text("\n".join(lines), encoding="utf-8")

    # t3：失败分类
    order = [
        "infra_blocked", "empty_response", "timeout", "pass_score_mismatch",
        "judge_mismatch", "persistence_anomaly", "none",
    ]
    eligible = [row for row in classified if row["bucket"] != "reflection" and row["task_score"] is not None]
    excluded = len(classified) - len(eligible)
    counts = {key: [] for key in order}
    for row in eligible:
        counts[row["error_type"]].append(row)
    total = len(eligible)

    t3_rows = [
        {
            "error_type": key,
            "count": len(counts[key]),
            "denominator": total,
            "pct": pct(len(counts[key]), total),
            "examples": "; ".join(str(r["task_id"]) for r in counts[key][:3]) or "-",
        }
        for key in order
    ]
    write_csv(out_dir / "t3_failures.csv", t3_rows, ["error_type", "count", "denominator", "pct", "examples"])

    lines = [
        "# 失败分类与比例 t3",
        "",
        f"分母：{total} 条有评分的 episode（with/without 合计）；另有 {excluded} 条 reflection 等无评分记录不参与比例。每条只记一个主类别，优先级：infra > empty_response > timeout > pass_score_mismatch > judge_mismatch > persistence_anomaly。",
        "",
        "| error_type | 条数 | 占比 | 典型案例 |",
        "|---|---:|---:|---|",
    ]
    for row in t3_rows:
        lines.append(f"| {row['error_type']} | {row['count']} | {row['pct']} | {row['examples']} |")

    lines += [
        "",
        "## family 级异常",
        "",
        "| run | family | variant | pollution | write_precision | recall | infra_blocks |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for sig in signals:
        lines.append(
            f"| {sig['run']} | {sig['family']} | {sig['variant']} | "
            f"{fmt(sig.get('avg_memory_pollution_rate'))} | {fmt(sig.get('avg_write_precision'))} | "
            f"{fmt(sig.get('avg_recall_accuracy'))} | {sig.get('families_with_infra_blocks')} |"
        )
    lines += [
        "",
        "口径说明：`write_precision` 取自 learn 阶段的 `avg_artifact_quality_score`，衡量 artifact 质量，不是写入次数；no-persistence 下非 0 属正常。",
        "",
    ]
    (out_dir / "t3_failures.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"t1: {len(t1_rows)} 行  t2: {len(classified)} 行  t3: {len(t3_rows)} 类  t4: {len(t4_rows)} 行")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

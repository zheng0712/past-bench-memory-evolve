# 数据集卡片：PAST-Bench v2（self-evolve-tasks-v2）

> 本卡片结论以 `benchmarks/PAST-Bench` 当前锁定 commit `f822351` 的实际文件与有效运行结果为准。

## 1. 来源与构建方式

- 仓库：`Gen-Verse/PAST-Bench`，本地 submodule 锁定 `f8223517`
- 任务根目录：`self-evolve-tasks-v2/`
- 规模：**26 个 family、204 个 episode**

| ability 目录 | families | episodes |
|---|---:|---:|
| `memory_ability/` | 5 | 41 |
| `procedural_ability/` | 8 | 64 |
| `proactive_information_gathering/` | 6 | 48 |
| `update_ability/` | 7 | 51 |

### 目录组织

```text
self-evolve-tasks-v2/<ability>/<family_id>/
├── family.yaml                 # 序列定义：bucket 配比、顺序、历史分支、控制组
├── <episode_dir>/task.yaml     # 单轮任务：prompt、tools、services、fixtures
├── <episode_dir>/expectations.json  # 判定契约：关键词、必需收件人、artifact 约束
├── <episode_dir>/grader.py     # 确定性判分组件
└── <episode_dir>/fixtures/     # mock 服务数据（notes.json 等）
```

### family.yaml 的关键字段

| 字段 | 作用 |
|---|---|
| `episode_order` | 作者编排的 episode 执行顺序 |
| `instances_per_bucket` | cold / learn / update / eval_near / eval_far / control 的数量配比 |
| `history_plan` | 三个分支：`continue`、`from_anchor`、`fresh` |
| `episode_overrides` | 单 episode 的 mechanism、持久化开关、初始 fixture |
| `control_set` | 控制组类型：`no_persistence`、`shortcut`、`wrong_mechanism` |
| `trigger_injection_plan` | 触发信号在哪个阶段注入、哪个阶段移除 |

### 运行期 manifest 生成

`--family <ability>/<id>` 会由 `family.yaml` 动态生成 manifest（[manifest.py](file:///c:/Users/zgz/Desktop/新人培养/PAST-Bench/src/past_bench/self_evolve_v2/manifest.py)），其中：

- `reflection_required = bucket_key in {"reflection", "learn_b"}`
- `reflection_enabled = True`

因此 **learn_b 阶段后会自动插入一次反思 episode**，它不在数据集目录里，是运行期产生的。SM01 因此是 8 个编排 episode + 1 个 `SM01_LEARN_B_001_REFLECT`。

## 2. 任务结构

### bucket 类型

| bucket | 作用 |
|---|---|
| `baseline`（cold） | 教任何东西之前的冷启动基线，两个变体共享同一次运行 |
| `learn` | 注入信号：learn_a 首次引入，learn_b 做同义强化 |
| `update` | 在 update_ability 中承担“纠正旧事实/旧规则”的学习阶段 |
| `evaluation` | eval_near 测近迁移，eval_far 测远迁移；提示词移除触发语 |
| `control` | 三类控制：no_persistence、shortcut、wrong_mechanism |
| `reflection` | 运行期生成，复盘 learn_b 的轨迹并写入持久化 |

### 历史分支

- `continue`：在同一 session 历史上继续
- `from_anchor`：从 learn 结束后的锚点恢复
- `fresh`：全新 session（评估与控制组使用）

### 我负责的两个 family

**SM01_preference_adoption（memory_ability，8 个编排 episode）**

| 顺序 | episode | bucket |
|---:|---|---|
| 1 | `cold_style_baseline` | baseline |
| 2 | `learn_a_tsv_preference` | learn |
| 3 | `learn_b_preference_reinforcement` | learn（触发 reflection） |
| 4 | `eval_near_apply_saved_style` | evaluation |
| 5 | `eval_far_transfer_saved_style` | evaluation |
| 6 | `control_shortcut_visible_style_rule` | control |
| 7 | `control_style_preference_control` | control |
| 8 | `control_no_persistence_style` | control |

运行期实际 9 条（含 reflection）。

**SM03_fact_correction（update_ability，7 个编排 episode）**

| 顺序 | episode | bucket |
|---:|---|---|
| 1 | `cold_fact_baseline` | baseline |
| 2 | `update_corrected_freeze_date` | learn（update 阶段） |
| 3 | `eval_near_use_corrected_fact` | evaluation |
| 4 | `eval_far_use_corrected_fact` | evaluation |
| 5 | `control_no_persistence_fact` | control |
| 6 | `control_shortcut_visible_corrected_fact` | control |
| 7 | `control_fact_correction_control` | control |

学习阶段不是 learn_b，所以**没有 reflection**，运行期也是 7 条。

## 3. 评测指标

### episode 级

`task_score` 由若干确定性组件加权得到，例如：

- SM01：`grounding`、`content_correctness`、`share_correctness`
- SM03：在上述基础上增加 `corrected_freeze_date`

`passed` 由硬条件决定，**不是 judge 分数**。SM03 without 出现过 `task_score=0.704` 但 `content_correctness=0`、`corrected_freeze_date=0`，因此 `passed=false`。

### family 级（`benchmark_signal`）

| 指标 | 含义 |
|---|---|
| `baseline_avg_score` | cold 阶段平均分 |
| `evaluation_avg_score` | 评估阶段平均分 |
| `avg_family_task_score_delta` | evaluation − baseline |
| `evaluation_pass_rate` | 评估阶段通过率 |
| `avg_write_precision` | learn 阶段 `avg_artifact_quality_score`，衡量 artifact 质量，**不是写入次数** |
| `avg_recall_accuracy` | 评估阶段“用到期望信号且内容正确”的比例 |
| `avg_update_correctness` | 更新阶段“抗旧值 + 内容正确”的平均 |
| `avg_retention_horizon` | eval_far / eval_near 的保持率 |
| `avg_memory_pollution_rate` | 新增/更新规则中不含 required keywords 的比例 |
| `avg_mechanism_score` | 上述五项机制指标的平均 |
| `avg_evolve_score` | `max(0, delta) × mechanism_score` |

`write_precision` 与 `evolve_score` 的定义见 [self_evolve.py](file:///c:/Users/zgz/Desktop/新人培养/PAST-Bench/src/past_bench/runner/self_evolve.py#L2095-L2138)。

### 实验数据

有效 run、逐 episode 结果与问题分类见 `reports/experiment-report.md`；数据集层面的统计画像见 `reports/tables/t0_dataset_profile.md`。

## 4. 已发现的数据集问题

完整清单见 `reports/experiment-report.md` 的“问题台账”一节。核心几项：

- SM03 的 `learn_a_seed_stale_fact` 存在于磁盘但不在 `episode_order` 中，运行期不执行。
- SM01 cold 的 prompt 要求 “clear and readable”，但 expectations 里 `require_tsv_output=true`。
- SM03 的 `without_persistence` 仍注入 stale 记忆与诱饵日期，不是零记忆对照。
- 控制组区分度不足：SM01 shortcut control 在有效 run 中从未达到 1.000。

## 5. 复现入口

```bash
cd ~/work/pbme
source benchmarks/PAST-Bench/.venv/bin/activate

python scripts/profile_dataset.py                       # t0
python scripts/collect_results.py \
  --runs experiments/20261118_sm01_hermes_smoke \
         experiments/20261119_sm01_run2 \
         experiments/20261119_sm01_run3 \
         experiments/20261118_sm03_hermes_smoke \
         experiments/20261119_sm03_run4 \
         experiments/20261119_sm03_run5 \
  --out reports/tables                                  # t1–t4

bash scripts/run_baseline.sh \
  --family memory_ability/SM01_preference_adoption \
  --run-id 20261119_sm01_run4                           # 新 run
```

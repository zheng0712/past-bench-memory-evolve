PY ?= python
FAMILY ?= update_ability/SM03_fact_correction
RUN_ID ?= $(shell date +%Y%m%d)_smoke
RUNS ?=

.PHONY: profile baseline collect

# 数据集画像 -> reports/tables/t0_dataset_profile.*
profile:
	$(PY) scripts/profile_dataset.py --out reports/tables

# 跑一个 family 的 with / without paired run
baseline:
	bash scripts/run_baseline.sh --family $(FAMILY) --run-id $(RUN_ID)

# 汇总 run，生成 t1–t4；用法：make collect RUNS="experiments/run1 experiments/run2"
collect:
	$(PY) scripts/collect_results.py --runs $(RUNS) --out reports/tables

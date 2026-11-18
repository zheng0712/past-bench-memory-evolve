PY ?= python

.PHONY: env-check profile smoke run collect table

env-check:
	$(PY) scripts/00_check_env.py

profile:
	$(PY) scripts/01_profile_dataset.py

smoke:
	$(PY) scripts/02_make_smoke_set.py

run:
	$(PY) scripts/03_run.py

collect:
	$(PY) scripts/04_collect.py

table:
	$(PY) scripts/05_make_tables.py

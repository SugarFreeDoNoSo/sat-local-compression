PYTHON ?= python3
LAKE ?= lake
.PHONY: check test experiments pdf formal verify clean
check: test
	$(PYTHON) scripts/check_research.py
	$(PYTHON) experiments/obdd_residuals.py --check
	$(PYTHON) experiments/graph_order_widths.py --check
test:
	$(PYTHON) -m unittest discover -s tests -v
experiments:
	$(PYTHON) experiments/obdd_residuals.py
	$(PYTHON) experiments/graph_order_widths.py
pdf:
	$(PYTHON) scripts/build_paper.py
formal:
	$(PYTHON) scripts/check_formal.py --lake "$(LAKE)"
verify: check pdf formal
	$(PYTHON) scripts/check_tex_log.py
clean:
	$(PYTHON) -c "import shutil; shutil.rmtree('build', ignore_errors=True)"

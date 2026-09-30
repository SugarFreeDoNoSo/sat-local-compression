PYTHON ?= python3
.PHONY: check test experiments pdf verify clean
check: test
	$(PYTHON) scripts/check_research.py
	$(PYTHON) experiments/obdd_residuals.py --check
test:
	$(PYTHON) -m unittest discover -s tests -v
experiments:
	$(PYTHON) experiments/obdd_residuals.py
pdf:
	$(PYTHON) scripts/build_paper.py
verify: check pdf
	$(PYTHON) scripts/check_tex_log.py
clean:
	$(PYTHON) -c "import shutil; shutil.rmtree('build', ignore_errors=True)"

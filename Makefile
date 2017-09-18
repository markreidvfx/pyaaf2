COVERAGE_EXEC := $(shell command -v coverage 2> /dev/null)

test: python-version
	@python -m unittest discover tests

python-version:
	@python --version

clean:
	rm */*.pyc */*/*.pyc

coverage: python-version
ifndef COVERAGE_EXEC
	$(error "coverage command missing: https://coverage.readthedocs.io/en/coverage-4.2/install.html")
endif
	@${COVERAGE_EXEC} run --source=aaf2 -m unittest discover tests
	@${COVERAGE_EXEC} report -m

PHONY: fmt
fmt:
	autoflake --recursive --remove-all-unused-imports --remove-unused-variables --expand-star-imports --in-place scansort/
	isort scansort/
	black scansort/

PHONY: requirements
build:
	hatch build

clean:
	rm -rf .mypy_cache .ruff_cache dist

lint:
	mypy
	ruff .

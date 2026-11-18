.PHONY: validate lint test

validate:
	python3 scripts/validate_skill.py .
	python3 scripts/validate.py .

lint:
	bash scripts/test_review_diff.sh

test: validate lint
	python3 scripts/run_local_validation.py

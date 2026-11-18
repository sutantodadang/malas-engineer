.PHONY: validate lint test

validate:
	python3 scripts/build_installer.py --check
	python3 scripts/validate_skill.py skills/malas-engineer
	python3 scripts/validate.py .

lint:
	bash scripts/test_review_diff.sh

test: validate lint
	python3 scripts/run_local_validation.py

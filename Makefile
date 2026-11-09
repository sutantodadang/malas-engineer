.PHONY: validate lint test

validate:
	python3 scripts/validate_skill.py .

lint:
	bash -n scripts/review_diff.sh

test: validate lint
	echo "OK"

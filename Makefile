.PHONY: doctor test bench serve clean

doctor:
	python -m arbiter doctor

test:
	python -m unittest discover -s tests

bench:
	python -m arbiter bench

serve:
	python -m arbiter serve

clean:
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true

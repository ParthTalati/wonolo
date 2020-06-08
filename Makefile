

build:
	docker build --tag wonolo .

test:
	docker run wonolo pytest tests/test_*.py
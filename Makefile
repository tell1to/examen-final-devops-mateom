.PHONY: build run docker-build docker-run

build:
	pip install -r requirements.txt

run:
	python app.py

docker-build:
	docker build -t finalquintoa .

docker-run:
	docker run -d -p 5000:5000 --name finalquintoa finalquintoa

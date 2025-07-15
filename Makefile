build-docker:
	docker build -t background_remover .

run-docker:
	docker run -p 8000:8000 --env-file .env background_remover

build-run-docker: build-docker run-docker

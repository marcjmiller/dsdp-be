FROM python:slim-buster
WORKDIR /app

deps:
  COPY Pipfile* .
  RUN pip install --upgrade pip
  RUN pip install pipenv
  RUN pipenv install --dev --system

build-dev-image:
  FROM +deps
  SAVE IMAGE backend:dev-build
  ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=8080"]

run-dev:
  LOCALLY
  RUN earthly +build-dev-image 
  RUN docker-compose up
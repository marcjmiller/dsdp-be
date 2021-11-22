FROM python:slim-buster
WORKDIR /app

all:
  BUILD +test

deps:
  ENV PATH=/home/python3/.local/bin:$PATH
  ENV PYTHONIOENCODING=UTF-8
  ENV PYTHONDONTWRITEBYTECODE=1
  ENV PYTHONUNBUFFERED=1
  COPY Pipfile* .
  RUN pip install --upgrade pip
  RUN pip install --upgrade wheel
  RUN pip install pipenv
  RUN pipenv install --dev --system

lint:
  FROM +deps
  RUN flake8 --count --show-source --statistics

format:
  LOCALLY
  RUN black src/ --diff --color --check
  
test:
  FROM +deps
  COPY ./src/ ./
  RUN pytest

build-dev-image:
  FROM +deps
  COPY ./src/ ./
  ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
  SAVE IMAGE backend:dev-build

run-dev:
  LOCALLY
  RUN earthly +build-dev-image 
  RUN docker-compose up
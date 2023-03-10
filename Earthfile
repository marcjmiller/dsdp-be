FROM python:3.9-slim-buster
WORKDIR /app

all:
  BUILD +integration-test

deps:
  ENV PATH=/home/python3/.local/bin:$PATH
  ENV PYTHONIOENCODING=UTF-8
  ENV PYTHONDONTWRITEBYTECODE=1
  ENV PYTHONUNBUFFERED=1
  COPY Pipfile* ./
  RUN pip install --upgrade pip
  RUN pip install pipenv
  RUN pipenv install --dev --system

lint:
  FROM +deps
  RUN flake8 --count --show-source --statistics

format:
  LOCALLY
  RUN black ./ --diff --color --check
  
# unit-test:
#   FROM +deps
#   COPY . ./backend
#   RUN pytest backend/tests/unit/*

integration-test:
  FROM +deps
  COPY main.py __init__.py docker-compose.yml pytest.ini .coveragerc ./backend
  COPY api ./backend/api
  COPY tests ./backend/tests
  WITH DOCKER --compose ./backend/docker-compose.yml
    RUN pytest backend/tests/*
  END

build-dev-image:
  FROM +deps
  COPY . ./backend
  ENTRYPOINT ["uvicorn", "backend.main:app", "--reload", "--host", "0.0.0.0"]
  SAVE IMAGE backend:dev-build

run-dev:
  LOCALLY
  RUN earthly +build-dev-image 
  RUN docker-compose up
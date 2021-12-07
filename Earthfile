FROM python:3.9-slim-buster
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
  RUN black ./ --diff --color --check
  
test:
  FROM +deps
  COPY . ./backend
  RUN pytest

build-dev-image:
  FROM +deps
  COPY . ./backend
  ENTRYPOINT ["uvicorn", "backend.main:app", "--reload", "--host", "0.0.0.0"]
  SAVE IMAGE backend:dev-build

run-dev:
  LOCALLY
  RUN earthly +build-dev-image 
  RUN docker-compose up
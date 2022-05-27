VERSION 0.6
FROM python:3.10.4-slim-buster
WORKDIR /home/python

all:
  BUILD +format
  BUILD +test
  BUILD +lint

dev-deps:
  ENV PATH=/home/python/.local/bin:$PATH
  ENV PYTHONIOENCODING=UTF-8 
  ENV PYTHONDONTWRITEBYTECODE=1 
  ENV PYTHONUNBUFFERED=1 
  ENV PYTHONPATH=/home/python 
  ENV PYTHONHASHSEED=random 
  ENV PYTHONFAULTHANDLER=1
  COPY pyproject.toml poetry.lock ./
  RUN pip install --upgrade pip; \
      pip install poetry; \
      poetry config virtualenvs.create false; \ 
      poetry install --no-interaction --no-ansi;

prod-deps:
  FROM registry1.dso.mil/ironbank/opensource/python:v3.10.4
  USER root
  ENV PATH=/home/python/.local/bin:$PATH
  ENV PYTHONIOENCODING=UTF-8
  ENV PYTHONDONTWRITEBYTECODE=1
  ENV PYTHONUNBUFFERED=1
  ENV PYTHONPATH=/home/python/python-packages
  COPY requirements.txt ./
  RUN yum update
  RUN yum install gcc libffi-devel -y
  USER python
  RUN pip install --upgrade pip==20.2.4
  RUN pip install --progress-bar off --disable-pip-version-check --no-cache-dir --target ./python-packages --requirement requirements.txt 

lint:
  FROM +dev-deps
  COPY . .
  RUN pylint ./**/*.py

format:
  LOCALLY
  RUN python -m black .

test:
  FROM +dev-deps
  COPY . .
  WITH DOCKER --compose docker-compose.test.yml --service minio
    RUN pytest
  END
  
build-dev-image:
  FROM +dev-deps
  COPY . .
  ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
  SAVE IMAGE backend:dev-build

build-prod-image:
  FROM +prod-deps
  COPY . .
  ENTRYPOINT ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]
  SAVE IMAGE backend:prod-build

run-dev:
  LOCALLY
  RUN earthly +build-dev-image
  RUN docker compose --profile dev up

run-prod:
  LOCALLY 
  RUN earthly +build-prod-image
  RUN docker compose --profile prod up 
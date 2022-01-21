FROM python:3.9-slim-buster
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
  COPY Pipfile* ./
  RUN pip install --upgrade pip
  RUN pip install pipenv
  RUN pipenv install --dev --system
  

prod-deps:
  FROM registry1.dso.mil/ironbank/opensource/python/python39:v3.9.9
  ENV PATH=/home/python/.local/bin:$PATH
  ENV PYTHONIOENCODING=UTF-8
  ENV PYTHONDONTWRITEBYTECODE=1
  ENV PYTHONUNBUFFERED=1
  ENV PYTHONPATH=/home/python/python-packages
  COPY requirements.txt ./
  RUN pip install --upgrade pip
  RUN pip install --progress-bar off --disable-pip-version-check --no-cache-dir --target ./python-packages --requirement requirements.txt 

lint:
  FROM +dev-deps
  COPY . .
  RUN pylint ./*.py

format:
  LOCALLY
  RUN black .

# unit-test:
#   FROM +dev-deps
#   COPY . .
#   RUN pytest backend/tests/unit/*

test:
  FROM +dev-deps
  COPY . .
  WITH DOCKER --compose ./docker-compose.test.yml
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
  RUN docker-compose --profile dev up

run-prod:
  LOCALLY 
  RUN earthly +build-prod-image
  RUN docker-compose --profile prod up 
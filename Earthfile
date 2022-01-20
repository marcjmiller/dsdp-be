FROM registry1.dso.mil/ironbank/opensource/python/python39:v3.9.9
WORKDIR /home/python

all:
  BUILD +integration-test

deps:
  ENV PATH=/home/python/.local/bin:$PATH
  ENV PYTHONIOENCODING=UTF-8
  ENV PYTHONDONTWRITEBYTECODE=1
  ENV PYTHONUNBUFFERED=1
  ENV PYTHONPATH=/home/python/python-packages
  COPY requirements.txt ./
  RUN pip install --upgrade pip
  RUN pip install --progress-bar off --disable-pip-version-check --no-cache-dir --target ./python-packages --requirement requirements.txt 

# lint:
#   FROM +deps
#   COPY . .
#   RUN pylint ./*.py

format:
  LOCALLY
  RUN black .

# unit-test:
#   FROM +deps
#   COPY . ./backend
#   RUN pytest backend/tests/unit/*

# integration-test:
#   FROM +deps
#   COPY main.py __init__.py docker-compose.yml pytest.ini .coveragerc ./
#   COPY api api
#   COPY tests tests
#   WITH DOCKER --compose ./docker-compose.yml
#     RUN pytest tests/*
#   END

build-dev-image:
  FROM +deps
  COPY . .
  ENTRYPOINT ["python", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
  SAVE IMAGE backend:dev-build

run-dev:
  LOCALLY
  RUN earthly +build-dev-image
  RUN docker-compose up
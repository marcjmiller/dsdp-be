FROM registry1.dso.mil/ironbank/opensource/python/python39:v3.9.7

WORKDIR /home/python/

ENV PATH=/home/python/.local/bin:$PATH
ENV PYTHONIOENCODING=UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --chown=python:python  Pipfile* ./
RUN pip install pipenv==2021.11.23 && pipenv install --system

COPY --chown=python:python  main.py ./
COPY --chown=python:python  __init__.py ./
COPY --chown=python:python  api/ ./api

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

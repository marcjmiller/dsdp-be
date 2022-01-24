FROM registry1.dso.mil/ironbank/opensource/python/python39:v3.9.9

WORKDIR /home/python/

ENV PATH=/home/python/.local/bin:$PATH
ENV PYTHONIOENCODING=UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --chown=python:python  main.py ./
COPY --chown=python:python  __init__.py ./
COPY --chown=python:python  api/ ./api
COPY --chown=python:python  logger.py ./logger.py
COPY --chown=python:python  log_config.yaml ./log_config.yaml
COPY --chown=python:python  .cache/python-packages ./python-packages

ENV PYTHONPATH=/home/python/python-packages

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]

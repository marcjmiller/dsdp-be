FROM registry1.dso.mil/ironbank/opensource/python/python39:v3.9.7

WORKDIR /home/python

COPY --chown=python:python  main.py ./
COPY --chown=python:python  __init__.py ./
COPY --chown=python:python  api/ ./api
COPY --chown=python:python  .cache/python-packages ./python-packages

ENV PYTHONPATH=/home/python/python-packages

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

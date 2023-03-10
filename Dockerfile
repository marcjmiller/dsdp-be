FROM registry1.dso.mil/ironbank/opensource/python/python39:v3.9.7

WORKDIR /home/python

COPY --chown=python:python  . .
COPY --chown=python:python  backend/ backend/
COPY --chown=python:python  .cache/python-packages ./python-packages

ENV PYTHONPATH=/home/python/python-packages

CMD ["python", "/home/python/main.py"]

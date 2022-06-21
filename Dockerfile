FROM registry1.dso.mil/ironbank/opensource/python/python39:v3.9.13

WORKDIR /home/python/

ENV PATH=/home/python/.local/bin:$PATH
ENV PYTHONIOENCODING=UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --chown=python:python  app/ ./app
COPY --chown=python:python  .cache/python-packages ./python-packages

ENV PYTHONPATH=/home/python/python-packages

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0"]

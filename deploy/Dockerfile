FROM python:3.12

ENV PYTHONPATH /backend

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-cache

ADD . backend

WORKDIR backend

ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]

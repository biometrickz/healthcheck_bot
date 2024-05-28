FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1 \
    COLUMNS=200 \
    TZ=Asia/Almaty \
    # Poetry
    POETRY_VERSION=1.2.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'


RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y curl \
    && curl -sSL 'https://install.python-poetry.org' | python - \
    && poetry --version \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    && ln -fs /usr/share/zoneinfo/Asia/Almaty /etc/localtime \
    && echo "Asia/Almaty" > /etc/timezone

COPY poetry.lock pyproject.toml /src/

WORKDIR /src


RUN echo poetry version \
  # Install deps:
  && poetry run pip install -U pip \
  && poetry install --no-dev --no-interaction \
  && rm -rf $POETRY_CACHE_DIR

COPY ./src /src

RUN chmod +x '/src/main.py'

CMD ["python3", "/src/main.py"]
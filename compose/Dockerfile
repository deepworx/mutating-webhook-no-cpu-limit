FROM python:3.10.7 AS builder
ARG DEV=false

# RUN apk update && apk add make gcc musl-dev libffi-dev openssl-dev ca-certificates

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.2.2

RUN pip install "poetry==$POETRY_VERSION"

RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./

RUN if $DEV; then /bin/sh -c 'poetry export --without-hashes -f requirements.txt --dev | /venv/bin/pip install -r /dev/stdin'; else /bin/sh -c 'poetry export --without-hashes -f requirements.txt | /venv/bin/pip install -r /dev/stdin'; fi

FROM python:3.10.7-slim

RUN groupadd fastapi && useradd -g fastapi -s /bin/sh fastapi

COPY ./compose/entrypoint.sh /entrypoint.sh
COPY ./compose/start /start
COPY --from=builder /venv /venv
COPY ./app /app/app

RUN chmod +x /entrypoint.sh \
    && chmod +x /start \
    && chown fastapi /app

RUN sed -i -e 's/\r$//' /entrypoint.sh
RUN sed -i -e 's/\r$//' /start

USER fastapi
WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start"]

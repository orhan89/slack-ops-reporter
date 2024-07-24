FROM python:3.11-alpine AS builder

WORKDIR /app

ADD pyproject.toml poetry.lock /app/

RUN apk add build-base libffi-dev

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-ansi

FROM python:3.11-alpine AS runner
WORKDIR /app

COPY --from=builder /app /app
ADD . /app

RUN addgroup --gid 1000 app
RUN adduser app -h /app -u 1000 -G app -DH
USER 1000

CMD ["/app/.venv/bin/gunicorn", "--bind", ":80", "slack_ops_reporter:create_app"]
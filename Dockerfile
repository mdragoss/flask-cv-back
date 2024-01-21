FROM python:3.11-slim AS builder

RUN apt update && apt install -y git gcc libpq-dev

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv requirements > requirements.txt

RUN pip install -r requirements.txt

FROM python:3.11-slim AS default

COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY . /app
WORKDIR /app
RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
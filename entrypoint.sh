#!/bin/sh
flask --app src/app init-mongo-db

exec "$@"

#!/bin/bash

sudo sh -c "echo 3 > /proc/sys/vm/drop_caches"

git checkout develop
git pull origin develop

docker compose exec app poetry install --no-root --no-dev
docker compose exec app poetry run inv migrate

docker compose -f compose.yml -f compose.override.dev.yml restart

if [ $? -eq 0 ]; then
  echo success
else
  docker compose -f compose.yml -f compose.override.dev.yml up -d
fi

#!/usr/bin/env sh

printf "\033[1m Running mypy run\033[0m on eden only, not on dependancies\n"
mypy -p eden # don't check dependancies
printf "\033[1mmypy exited with exit code $?\033[0m\n"
printf "\033[1m Running ruff run\033[0m on eden only, not on dependancies\n"
ruff check eden/
printf "\033[1mruff exited with exit code $?\033[0m\n"
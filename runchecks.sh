#!/usr/bin/env sh

printf "\033[1m Running mypy run\033[0m on eden only, not on dependancies\n"
echo "Beginning eden shared library typecheck"
mypy -p eden # don't check dependancies
echo "Beginnning eden server library typecheck"
mypy -p server
echo "Beginning eden client typecheck"
mypy -m client
printf "\033[1mmypy exited with exit code $?\033[0m\n"
printf "\033[1m Running ruff run\033[0m on eden only, not on dependancies\n"
ruff check eden/ server/ client.py
printf "\033[1mruff exited with exit code $?\033[0m\n"
pytest test.py
printf "\033[1mpylint exited with exit code $?\033[0m\n"
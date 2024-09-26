#!/usr/bin/env sh

echo 'Installing Python dependencies...'

poetry completions bash >>~/.bash_completion
sudo chown vscode .venv
poetry config virtualenvs.in-project true
poetry install

echo 'Finished postCreateCommand'

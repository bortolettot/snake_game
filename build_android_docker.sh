#!/bin/bash
# Compila o Snake Game para Android usando Docker e Buildozer

set -euo pipefail

IMAGE="kivy/buildozer:latest"

# Executa o build dentro do container Buildozer
# Monta o diretório do projeto em /home/user/app

docker run --rm -v "$(pwd)":/home/user/app -w /home/user/app "$IMAGE" \
    buildozer android debug

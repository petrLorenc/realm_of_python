FROM python:3.13-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /clean_workspace

ENTRYPOINT ["/bin/bash"]
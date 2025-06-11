FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE=only-managed

RUN uv python install 3.13

WORKDIR /src

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --locked --no-install-project --no-dev

COPY . /src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

FROM debian:bookworm-slim

COPY --from=builder --chown=app:app /python /python
COPY --from=builder --chown=app:app /src /app

ENV PATH="/python/bin:/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

CMD ["python", "-m", "src"]

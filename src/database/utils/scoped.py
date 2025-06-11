from contextvars import ContextVar


session_context: ContextVar[str | None] = ContextVar(
    "session_context", default=None
)


def get_context() -> str | None:
    return session_context.get()


def set_context(context: str | None):
    session_context.set(context)


def reset_context() -> None:
    session_context.set(None)

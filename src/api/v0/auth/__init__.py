from fastapi import HTTPException, status, Request


def auth_required(request: Request):
    user = getattr(request.state, "user", None)
    if not user or not getattr(user, "is_authenticated", False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

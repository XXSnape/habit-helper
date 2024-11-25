from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError


from utils import auth

http_bearer = HTTPBearer()


def get_token_payload(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]
) -> dict[str, str | int]:
    try:
        payload = auth.decode_jwt(
            token=credentials.credentials,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def get_user_id(payload: Annotated[dict, Depends(get_token_payload)]) -> int:
    return int(payload.get("sub"))

from uuid import UUID, uuid4
from fastapi import Cookie, Response

async def get_anonymous_id(
    response: Response,
    anonymous_id: UUID | None = Cookie(default=None),
) -> UUID:
    if anonymous_id is None:
        anonymous_id = uuid4()

        response.set_cookie(
            key="anonymous_id",
            value=str(anonymous_id),
            httponly=True,
            samesite="lax",
        )

    return anonymous_id
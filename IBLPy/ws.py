try:
    from fastapi import APIRouter, Header, Request
    from starlette.exceptions import HTTPException as StarletteHTTPException
    from pydantic import BaseModel
    from typing import Optional, Union

    router = APIRouter(include_in_schema = False)

    def abort(code: int) -> StarletteHTTPException:
        raise StarletteHTTPException(status_code=code)

    class Vote(BaseModel):
        timeStamp: str
        userID: str
        botID: str
        type: str

    @router.post("/")
    async def iblpy_webhook(vote: Vote, Authorization: str = Header("INVALID_SECRET")):
        if secret is None or secret == Authorization:
            pass
        else:
            return abort(401)
        vote.timeStamp = int(vote.timeStamp)
        return await wh_func(vote, secret)

except:
    pass


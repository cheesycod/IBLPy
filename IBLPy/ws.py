try:
    from fastapi import APIRouter, Header, Request
    from starlette.exceptions import HTTPException as StarletteHTTPException
    from pydantic import BaseModel
    from typing import Optional, Union

    router = APIRouter(include_in_schema = False)

    def abort(code: int) -> StarletteHTTPException:
        raise StarletteHTTPException(status_code=code)

    class Vote(BaseModel):
        """
            Represents a IBL Vote

            :param timeStamp: This is an internal field that is not present in the final Vote

            :param userID: The User ID of the vote

            :param botID: The Bot ID of the vote

            :param type: The type of the vote

            :param timestamp: The timestamp of the vote. Despite the typehint here, it wil always be a integer and will never be None
        """
        timeStamp: str
        userID: str
        botID: str
        type: str
        timestamp: Optional[int] = None

    @router.post("/")
    async def iblpy_webhook(vote: Vote, Authorization: str = Header("INVALID_SECRET")):
        if secret is None or secret == Authorization:
            pass
        else:
            return abort(401)
        vote.timestamp = int(vote.timeStamp)
        del vote.__dict__["timeStamp"]
        return await wh_func(vote, secret)

except:
    pass


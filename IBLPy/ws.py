try:
    from fastapi import APIRouter, Header, Request
    from starlette.exceptions import HTTPException as StarletteHTTPException
    from pydantic import BaseModel
    from typing import Optional, Union

    router = APIRouter(include_in_schema = False)

    def abort(code: int) -> StarletteHTTPException:
        raise StarletteHTTPException(status_code=code)

    class VoteInternal(BaseModel):
        """
            Represents a internal IBL Vote. IBLPy will make this a Vote class
        """
        timeStamp: str
        userID: str
        botID: str
        type: str
        timestamp: Optional[int] = None

    class Vote():
        """
            Represents a vote on IBL

            :param bot_id: The Bot ID of the vote

            :param user_id: The ID of the user who voted for your bot. In test mode, this will be 0

            :param test: Whether this is a test webhook or not

            :param timestamp: The timestamp (epoch) when the vote happened
        """
        def __init__(self, bot_id: int, user_id: int, test: bool, timestamp: int):
            self.bot_id = bot_id
            self.user_id = user_id
            self.test = test
            self.timestamp = timestamp

    @router.post("/")
    async def iblpy_webhook(vote_internal: VoteInternal, Authorization: str = Header("INVALID_SECRET")):
        if secret is None or secret == Authorization:
            pass
        else:
            return abort(401)
        timestamp = int(vote_internal.timeStamp)
        
        if vote_internal.type.lower() == "test":
            bot_id = botcli.id
            user_id = 0
            test = True
        else:
            bot_id = int(vote_internal.botID)
            user_id = int(vote_internal.userID)
            test = False
        vote = Vote(bot_id = bot_id, user_id = user_id, test = test, timestamp = timestamp)
        return await wh_func(vote, secret)

except:
    pass


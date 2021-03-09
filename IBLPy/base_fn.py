import IBLPy.config as cfg
from IBLPy import api_modes
import json

class NoSuitableModesFound(Exception):
    def __init__(self):
        super().__init__("In order to use IBLPy, you must have either requests (sync) or aiohttp_requests (async) installed")

class InvalidMode(Exception):
    def __init__(self, mode):
        if mode == "async":
            super().__init__("In order to use IBLPy asynchronous API requests, you must have aiohttp_requests installed")
        elif mode == "sync":
            super().__init__("In order to use IBLPy synchronous API requests, you must have requests installed")
        elif mode == "fastapi":
            super().__init__("In order to use IBLPy webhooks, you must have fastapi and uvicorn installed")

class IBLAPIResponse():
    def __init__(self, *, raw_res, success, message, data, status):
        self.response = raw_res
        self.success = success
        self.message = message
        self.data = data
        self.status = status

class IBLAPIRatelimit(Exception):
    def __init__(self):
        super().__init__("You are being ratelimited by the Infinity Bots (IBL) API. For future reference, the ratelimit for posting stats is 3 requests per 5 minutes and is unknown/variable for getting stats!")

class IBLInvalidEndpoint(Exception):
    def __init__(self, required, current):
        super().__init__(f"This endpoint can only be used by a {required} however you are a {current}")

class IBLBot():
    """
        Represents a bot on IBL
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.guild_count = self.analytics["servers"]
        self.shard_count = self.analytics["shards"]
        self.votes = self.analytics["votes"]
        self.invites = self.analytics["invites"]
        del self.__dict__["analytics"]

    def dict(self):
        return self.__dict__

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

def async_api():
    if "async" not in api_modes:
        raise InvalidMode("async")

def sync_api():
    if "sync" not in api_modes:
        raise InvalidMode("sync")

def bot_only(user):
    if user != "bot": 
        raise IBLInvalidEndpoint("bot", user)


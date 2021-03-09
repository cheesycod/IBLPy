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

class IBLAPIResponse():
    def __init__(self, *, raw_res, success, message, data, status):
        self.response = raw_res
        self.success = success
        self.message = message
        self.data = data
        self.status = status

class IBLAPIRatelimit(Exception):
    def __init__(self):
        super().__init__("You are being ratelimited by the Infinity Bots (IBL) API. For future reference, the ratelimit is 3 requests per 5 minutes!")

def async_api(fn):
    async def wrapper(*args, **kwargs):
        if "async" not in api_modes:
            raise InvalidMode("async")
        return await fn(*args, **kwargs)
    return wrapper

def sync_api(fn):
    def wrapper(*args, **kwargs):
        if "sync" not in api_modes:
            raise InvalidMode("sync")
        return fn(*args, **kwargs)
    return wrapper


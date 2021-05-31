import IBLPy.config as cfg
from IBLPy import api_modes, requests, aiohttp
import json
from typing import Union, Optional

class NoSuitableModesFound(Exception):
    """Raised when neither requests, aiohttp_requests or fastapi+uvicorn was found"""
    def __init__(self):
        super().__init__("In order to use IBLPy, you must have either requests (sync) or aiohttp_requests (async) installed")

class InvalidMode(Exception):
    """Raised when you don't have the required mode (package) to perform the action such as trying to do an asynchronous API request without having aiohttp_requests installed or trying to do a webhook without fastapi+uvicorn"""
    def __init__(self, mode):
        if mode == "async":
            super().__init__("In order to use IBLPy asynchronous API requests, you must have aiohttp_requests installed")
        elif mode == "sync":
            super().__init__("In order to use IBLPy synchronous API requests, you must have requests installed")
        elif mode == "fastapi":
            super().__init__("In order to use IBLPy webhooks, you must have fastapi and uvicorn installed")

class IBLAPIRatelimit(Exception):
    """Raised when you are being ratelimited by IBL. The ratelimit for posting stats is 3 requests per 5 minutes and is unknown/variable for getting stats from the API"""
    def __init__(self):
        super().__init__("You are being ratelimited by the Infinity Bots (IBL) API. For future reference, the ratelimit for posting stats is 3 requests per 5 minutes and is unknown/variable for getting stats from the API!")

class IBLAPIResponse():
    """
        IBLAPIResponse represents an API response in the IBLPy library
        
        :param raw_res: This is the raw response from the API. This will either be a requests Response (sync API functions) or a aiohttp ClientSession (async API functions)

        :param success: Whether the API response has succeeded or not.

        :param message: Any messages returned by the API in the message field. Can be None if there are no messages

        :param data: The JSON object sent by the API

        :param status: The status code of the HTTP response received from the API
    """
    def __init__(self, *, raw_res: Union[requests.Response, aiohttp.ClientSession], success: bool, message: Optional[str], data: dict, status: int):
        self.response = raw_res
        self.success = success
        self.message = message
        self.data = data
        self.status = status

class IBLBaseUser():
    """
        This is a base user on IBL from which all bots and users extend from
    """
    def __init__(self):
        pass

    def dict(self) -> dict:
        """Returns the class as a dict using the dict dunder property of the class"""
        return self.__dict__

    def __str__(self) -> str:
        """Returns the name of the bot or user"""
        return self.name

    def __int__(self) -> int:
        """Returns the bot or user ID"""
        return self.id

class IBLBot(IBLBaseUser):
    """
        IBLBot is internally a part of the base_fn module (which provides all of IBLPy's base classes and functions). It represents a bot on IBL. The exact parameters of an IBLBot may change and IBLPy is designed to handle such changes automatically. Here are the parameters that we know of right now:

        :param id: The id of the bot. This will be a integer

        :param username: The name of the bot. This will be a string

        :param tags: The tags of the bot. To make it easier for you, IBLPy makes this a list instead of the comma seperated string returned by the IBL API. This will be a list

        :param prefix: This is the prefix of the bot. This will be a string

        :param owner: The name of the owner of the bot. For some reason, the IBL API does not give the owner ID. This will be a string

        :param short: The short description of the bot. This will be a string

        :param long: The long description of the bot. This will be a string

        :param library: The library the bot is coded in. This will be a string

        :param premium: Whether the bot is premium or not. This will be a boolean

        :param staff: Whether the bot is a staff bot or not. This will be a boolean

        :param nsfw: Whether the bot is marked as an NSFW (Not Safe For Work) bot or not. This will be a boolean

        :param certified: Whether the bot is certified or not. This will be a boolean

        :param guild_count: The server count of the bot. The API puts this in a analytics JSON object, but for simplicity, we provide this as just guild_count. This will be a integer

        :param shard_count: The server count of the bot. The API puts this in a analytics JSON object, but for simplicity, we provide this as just shard_count. This will be a integer

        :param votes: The amount of votes the bot has. The API puts this in a analytics JSON object, but for simplicity, we provide this as just votes. This will be a integer

        :param invites: The amount of people who have invited your bot. The API puts this in a analytics JSON object, but for simplicity, we provide this as just invites. This will be a integer

        :param banner: The bots banner. The API puts this in a links JSON object, but for simplicity, we provide this as just banner. This will be a string or None (if not found)

        :param github: The bots github. The API puts this in a links JSON object, but for simplicity, we provide this as just github. This will be a string or None (if not found)

        :param website: The bots website. The API puts this in a links JSON object, but for simplicity, we provide this as just website. This will be a string or None (if not found)

        :param donate: The bots donation link. The API puts this in a links JSON object, but for simplicity, we provide this as just donate. This will be a string or None (if not found)

        :param support: The bots support server. The API puts this in a links JSON object, but for simplicity, we provide this as just support. This will be a string or None (if not found)
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

        # Handle analytics
        self.guild_count = int(self.analytics["servers"])
        self.shard_count = int(self.analytics["shards"])
        self.votes = int(self.analytics["votes"])
        self.invites = int(self.analytics["invites"])
        del self.__dict__["analytics"]

        # Handle links
        for key in self.links.keys():
            self.__dict__[key] = self.links.get(key)
            if self.__dict__[key].lower() == "none":
                self.__dict__[key] = None
        del self.__dict__["links"]

        # Handle tags
        self.tags = self.tags.replace(" ", "").split(",")

        # Handle name -> username convert
        self.username = self.name
        del self.__dict__["name"]

class IBLUser(IBLBaseUser):
    """
        IBLUser is internally a part of the base_fn module (which provides all of IBLPy's base classes and functions). It represents a user on IBL. The exact parameters of an IBLUser may change and IBLPy is designed to handle such changes automatically. Here are the parameters that we know of right now:

        :param id: The id of the user. This will be a integer

        :param username: The name of the user. This will be a string

        :param nickname: The nickname of the user. This will be a string or None (if not found)

        :param about: The users description/about text. This will be a string

        :param certified_dev: Whether the user is a certified developer or not. This will be a boolean

        :param developer: Whether the user is a developer or not. This will be a boolean

        :param staff: Whether the user is an IBL staff member or not. This will be a boolean

        :param website: The users listed website. The API puts this in a links JSON object, but for simplicity, we provide this as just website. This will be a string or None (if not found)
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        if self.nickname.lower() == 'none':
            self.nickname = None
        self.website = self.links["website"]
        if self.website.lower() == 'none':
            self.website = None
        del self.__dict__["links"]


def async_api():
    if "async" not in api_modes:
        raise InvalidMode("async")

def sync_api():
    if "sync" not in api_modes:
        raise InvalidMode("sync")

def bot_only(user):
    if user != "bot": 
        raise IBLInvalidEndpoint("bot", user)


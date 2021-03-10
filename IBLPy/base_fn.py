import IBLPy.config as cfg
from IBLPy import api_modes, requests, aiohttp
import json
from typing import Union, Optional

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

class IBLAPIRatelimit(Exception):
    def __init__(self):
        super().__init__("You are being ratelimited by the Infinity Bots (IBL) API. For future reference, the ratelimit for posting stats is 3 requests per 5 minutes and is unknown/variable for getting stats!")

class IBLInvalidEndpoint(Exception):
    def __init__(self, required, current):
        super().__init__(f"This endpoint can only be used by a {required} however you are a {current}")

class IBLBot():
    """
        IBLBot is internally a part of the base_fn module (which provides all of IBLPy's base classes and functions). It represents a bot on IBL. The exact parameters of an IBLBot may change and IBLPy is designed to handle such changes automatically. Here are the parameters that we know of right now:

        :param id: The id of your bot. This will be a integer

        :param name: The name of the bot. This will be a string

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

        :param banner: The bots banner. The API puts this in a links JSON object, but for simplicity, we provide this as just banner. This will be a string

        :param github: The bots github. The API puts this in a links JSON object, but for simplicity, we provide this as just github. This will be a string

        :param website: The bots website. The API puts this in a links JSON object, but for simplicity, we provide this as just website. This will be a string

        :param donate: The bots donation link. The API puts this in a links JSON object, but for simplicity, we provide this as just donate. This will be a string

        :param support: The bots support server. The API puts this in a links JSON object, but for simplicity, we provide this as just support. This will be a string
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

        # Handle analytics
        self.guild_count = self.analytics["servers"]
        self.shard_count = self.analytics["shards"]
        self.votes = self.analytics["votes"]
        self.invites = self.analytics["invites"]
        del self.__dict__["analytics"]

        # Handle links
        self.website = self.links["website"]
        if self.website == 'None':
            self.website = None
        self.donate = self.links["donate"]
        if self.donate == 'None':
            self.donate = None
        self.support = self.links["support"]
        if self.support == 'None':
            self.support = None
        self.github = self.links["github"]
        if self.github == 'None':
            self.github = None
        self.banner = self.links["banner"]
        if self.banner == 'None':
            self.banner = None
        del self.__dict__["links"]

        # Handle tags
        self.tags = self.tags.replace(" ", "").split(",")

    def dict(self) -> dict:
        """Returns the class as a dict using the dict dunder property of the class"""
        return self.__dict__

    def __str__(self):
        """Returns the name of the bot"""
        return self.name

    def __int__(self):
        """Returns the bots ID"""
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


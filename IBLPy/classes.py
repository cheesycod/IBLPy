import IBLPy.config as cfg
from IBLPy import api_modes, aiohttp
from typing import Union, Optional

class InvalidMode(Exception):
    """Raised when you don't have the required mode (package) to perform the action such as trying to do an asynchronous API request without having aiohttp_requests installed or trying to do a webhook without fastapi+uvicorn"""
    def __init__(self, mode):
        if mode == "async":
            super().__init__("In order to use IBLPy asynchronous API requests, you must have aiohttp, requests and aiohttp_requests installed")
        elif mode == "fastapi":
            super().__init__("In order to use IBLPy webhooks, you must have fastapi and uvicorn installed")
        elif mode == "misc":
            super().__init__("Parts of IBLPy rely on requests to fetch information such as user fetching...")

try:
    import requests
except:
    raise InvalidMode("misc")

class IBLAPIRatelimit(Exception):
    """Raised when you are being ratelimited by IBL. The ratelimit for posting stats is 3 requests per 5 minutes and is unknown/variable for getting stats from the API"""
    def __init__(self):
        super().__init__("You are being ratelimited by the Infinity Bots (IBL) API. For future reference, the ratelimit for posting stats is 3 requests per 5 minutes and is unknown/variable for getting stats from the API!")

class IBLAPIResponse():
    """
        IBLAPIResponse represents an API response in the IBLPy library
        
        :param res: This is the raw response from the API. 
            This will be a aiohttp ClientResponse

        :param success: Whether the API response has succeeded or not (status less than 400)
        
        :param error_msg: The error message reported by the Infinity Bot List API

        :param message: Any messages returned by the API in the message field. Can be None if there are no messages

        :param json: The JSON object sent by the API

        :param status: The status code of the HTTP response received from the API
    """
    def __init__(self, *, res: aiohttp.ClientResponse, json: dict):
        self.res = res
        self.success = True if res.status < 400 else False
        self.message = json.get("message")
        self.error = json.get("error")
        self.json = json
        self.status = res.status

class IBLBaseUser():
    """
        This is a base user on IBL from which all bots and users extend from
    """
    def __init__(self, id, json):
        self.__dict__.update(**json)
        self.id = id
        self.clean()
    
    def dict(self) -> dict:
        """Returns the class as a dict using the dict dunder property of the class"""
        return self.__dict__

    def __str__(self) -> str:
        """Returns the name of the bot or user"""
        try:
            return self.username
        except AttributeError:
            return str(self.dict())

    def __int__(self) -> int:
        """Returns the bot or user ID"""
        return self.id
    
    def clean(self):
        """Cleans up all the ugly stuff from the IBL API"""
        for k, v in self.__dict__.items():
            self.__dict__[k] = self._cleaner(attr=v)
    
    def _cleaner(self, attr: str):
        if isinstance(attr, str):
            if attr.lower() == "none":
                return None
            elif attr.lower() == "false":
                return False
            elif attr.lower() == "true":
                return True
            elif attr.isdigit():
                return int(attr)
        
        elif isinstance(attr, dict):
            _tmp = {}
            for k, v in attr.items():
                _tmp[k] = self._cleaner(attr=v)
            return _tmp
        
        return attr
    
class IBLBot(IBLBaseUser):
    """
        IBLBot is internally a part of the base_fn module (which provides all of IBLPy's base classes and functions). 
        It represents a bot on IBL. The exact parameters of an IBLBot may change and IBLPy is designed to handle such changes automatically. 
        Here are the parameters that we know of right now:

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

        :param servers: The server count of the bot. The API puts this in a analytics JSON object, but for simplicity, we provide this as just guild_count. This will be a integer

        :param shards: The server count of the bot. The API puts this in a analytics JSON object, but for simplicity, we provide this as just shard_count. This will be a integer

        :param votes: The amount of votes the bot has. The API puts this in a analytics JSON object, but for simplicity, we provide this as just votes. This will be a integer

        :param invites: The amount of people who have invited your bot. The API puts this in a analytics JSON object, but for simplicity, we provide this as just invites. This will be a integer

        :param banner: The bots banner. The API puts this in a links JSON object, but for simplicity, we provide this as just banner. This will be a string or None (if not found)

        :param github: The bots github. The API puts this in a links JSON object, but for simplicity, we provide this as just github. This will be a string or None (if not found)

        :param website: The bots website. The API puts this in a links JSON object, but for simplicity, we provide this as just website. This will be a string or None (if not found)

        :param donate: The bots donation link. The API puts this in a links JSON object, but for simplicity, we provide this as just donate. This will be a string or None (if not found)

        :param support: The bots support server. The API puts this in a links JSON object, but for simplicity, we provide this as just support. This will be a string or None (if not found)
    """
    def __init__(self, id, json):
        super().__init__(id, json)
        
        # Handle analytics
        for k, v in self.analytics.items():
            self.__dict__[k] = v
        for k, v in self.links.items():
            self.__dict__[k] = v

        del self.__dict__["analytics"]
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

        :param user: A JAPI user object (see [here](https://docs.japi.rest/#discord-user)). This will be a dict (the value of 'data') or None if not fetchable. **This internally comes from japi.rest**

        :param nickname: The nickname of the user. This will be a string or None (if not found)

        :param about: The users description/about text. This will be a string

        :param certified_dev: Whether the user is a certified developer or not. This will be a boolean

        :param developer: Whether the user is a developer or not. This will be a boolean

        :param staff: Whether the user is an IBL staff member or not. This will be a boolean

        :param website: The users listed website. The API puts this in a links JSON object, but for simplicity, we provide this as just website. This will be a string or None (if not found)
    """
    def __init__(self, id, json, japi_data):
        if japi_data:
            self.user = japi_data["data"]
        else:
            self.user = None
        
        if not self.user:
            self.username = ""
        else:
            self.username = self.user["username"]

        super().__init__(id, json)  

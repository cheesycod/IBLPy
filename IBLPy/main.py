import IBLPy.config as cfg
import IBLPy.api_brain as api_brain
from IBLPy.base_fn import async_api, sync_api, bot_only, InvalidMode
from IBLPy import api_modes, fastapi, uvicorn, ws
from typing import Optional
import os
import asyncio

class BotClient():
    """
        Initialize a Infinity Bots List (IBL) Bot Client
            
        :param id: The Bot ID you wish to use with the IBL API

        :param api_token: The API Token of the bot. You can find this by clicking API Token under the "Owner Section". This is optional however you will not be able to post stats if you do not pass a API Token

        :param error_on_ratelimit: A boolean to indicate whether we should error with a IBLAPIRatelimit or simply return a IBLAPIResponse on a ratelimit error

    """

    def __init__(self, id: int, api_token: Optional[str] = "", error_on_ratelimit: bool = True):
        self.id = id
        self.api_token = api_token
        self.api_url = cfg.api
        self.error_on_ratelimit = error_on_ratelimit

    async def set_stats_async(self, guild_count: int, shard_count: Optional[int] = None):
        """
            Posts bot stats to the IBL API asynchronously
            
            :param guild_count: Amount of servers your bot is in

            :param shard_count: Amount of shards your bot is in. This is optional

            :return: This will always be returned unless something goes wrong, in which case you will get an exception
            :rtype: IBLAPIResponse 
        """
        async_api()
        return await api_brain.set_stats_async(bot_id = self.id, api_token = self.api_token, guild_count = guild_count, shard_count = shard_count, error_on_ratelimit = self.error_on_ratelimit)
    
    def set_stats_sync(self, guild_count: int, shard_count: Optional[int] = None):
        """
            Posts bot stats to the IBL API synchronously

            :param guild_count: Amount of servers your bot is in

            :param shard_count: Amount of shards your bot is in. This is optional

            :return: This will always be returned unless something goes wrong, in which case you will get an exception
            :rtype: IBLAPIResponse
        """
        sync_api()
        return api_brain.set_stats_sync(bot_id = self.id, api_token = self.api_token, guild_count = guild_count, shard_count = shard_count, error_on_ratelimit = self.error_on_ratelimit)
    
    def set_stats(self, guild_count: int, shard_count: Optional[int] = None):
        """This is a shortcut to the ``set_stats_sync`` function. Please see that functions documentation"""
        sync_api()
        return self.set_stats_sync(guild_count, shard_count) # Shortcut to set_stats_sync

    def get_bot_sync(self):
        """
            Synchronously get a bot. This does not take any parameters.

            :return: If the bot was not found or if IBLPy could not parse the JSON request for any reason
            :rtype: None

            :return: This will be returned if you are ratelimited
            :rtype: IBLAPIResponse

            :return: This is the bot object returned from the API
            :rtype: IBLBot

        """
        sync_api()
        return api_brain.get_bot_sync(bot_id = self.id, error_on_ratelimit = self.error_on_ratelimit)

    def get_bot(self):
        """This is a shortcut to the ``get_bot_sync`` function. Please see that functions documentation"""
        sync_api()
        return self.get_bot_sync()

    async def get_bot_async(self):
        """
            Asynchronously get a bot. This does not take any parameters.

            **Return Types**

            None - If the bot was not found or if IBLPy could not parse the JSON request for any reason

            IBLAPIResponse - This will be returned if you are ratelimited

            IBLBot - This is the bot object returned from the API
        """
        async_api()
        return await api_brain.get_bot_async(bot_id = self.id, error_on_ratelimit = self.error_on_ratelimit)

class Webhook():
    def __init__(self, botcli: BotClient, secret: str = None):
        if "webhook" not in api_modes:
            raise InvalidMode("fastapi")
        self.botcli = botcli
        self.secret = secret

    def start_ws_task(self, route, func, port = 8012):
        asyncio.create_task(self.start_ws(route, port = port, func = func))

    def start_ws_normal(self, route, func, port = 8012):
        asyncio.run(self.start_ws(route, port = port, func = func))

    async def start_ws(self, route, func, port = 8012):
        ws.wh_func = func
        ws.botcli = self.botcli
        ws.secret = self.secret
        app = fastapi.FastAPI(docs_url = None, redoc_url = None)
        app.include_router(
            router = ws.router,
            prefix=route,
        )
        server = uvicorn.Server(uvicorn.Config(app, host = "0.0.0.0", port = port))
        await server.serve()
        try:
            os._exit()
        except:
            os._exit(0)


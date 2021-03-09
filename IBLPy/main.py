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

        **Parameters**
            
        *id* - The Bot ID you wish to use with the IBL API

        *api_token* - The API Token of your bot.

        *error_on_ratelimit* - A boolean to indicate whether we should error with a IBLAPIRatelimit or simply return a IBLAPIResponse on a ratelimit error

    """

    def __init__(self, bot_id: int, api_token: str, error_on_ratelimit: bool = True):
        self.id = bot_id
        self.api_token = api_token
        self.api_url = cfg.api
        self.error_on_ratelimit = error_on_ratelimit

    async def set_stats_async(self, guild_count: int, shard_count: Optional[int] = None):
        """
            Posts bot stats to the IBL API asynchronously

            **Parameters**
            
            *guild_count* - Amount of servers your bot is in

            *shard_count* - Amount of shards your bot is in. This is optional

        """
        async_api()
        return await api_brain.set_stats_async(bot_id = self.id, api_token = self.api_token, guild_count = guild_count, shard_count = shard_count, error_on_ratelimit = self.error_on_ratelimit)
    
    def set_stats_sync(self, guild_count: int, shard_count: Optional[int] = None):
        """
            Posts bot stats to the IBL API synchronously

            **Parameters**
            
            *guild_count* - Amount of servers your bot is in

            *shard_count* - Amount of shards your bot is in. This is optional

        """
        sync_api()
        return api_brain.set_stats_sync(bot_id = self.id, api_token = self.api_token, guild_count = guild_count, shard_count = shard_count, error_on_ratelimit = self.error_on_ratelimit)
    
    def set_stats(self, guild_count: int, shard_count: Optional[int] = None):
        """This is a shortcut to the ``set_stats_sync`` function"""
        sync_api()
        return self.set_stats_sync(guild_count, shard_count) # Shortcut to set_stats_sync

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


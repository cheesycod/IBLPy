import IBLPy.config as cfg
import IBLPy.api_brain as api_brain
from IBLPy.base_fn import async_api, sync_api, bot_only, InvalidMode, IBLAPIResponse
from IBLPy import api_modes, fastapi, uvicorn, ws, autoposter, discord
from typing import Optional
import os
import asyncio
import time

class BotClient():
    """
        Initialize a Infinity Bots List (IBL) Bot Client. You can use this to get/post bot stats and fetch a bot!
            
        :param id: The Bot ID you wish to use with the IBL API

        :param api_token: The API Token of the bot. You can find this by clicking API Token under the "Owner Section". This is optional however you will not be able to post stats if you do not pass a API Token

        :param error_on_ratelimit: A boolean to indicate whether we should error with a IBLAPIRatelimit or simply return a IBLAPIResponse on a ratelimit error. Defaults to True

        :param debug: Whether to run in debug mode or not. Defaults to False.
    """

    def __init__(self, id: int, api_token: Optional[str] = "", error_on_ratelimit: bool = True, debug: bool = False):
        self.id = id
        self.api_token = api_token
        self.error_on_ratelimit = error_on_ratelimit
        self.debug = debug

    async def set_stats_async(self, guild_count: int, shard_count: Optional[int] = None) -> IBLAPIResponse:
        """
            Posts bot stats to the IBL API asynchronously
            
            :param guild_count: Amount of servers your bot is in

            :param shard_count: Amount of shards your bot is in. This is optional

            :return: This will always be returned unless something goes wrong, in which case you will get an exception
            :rtype: IBLAPIResponse 
        """
        async_api()
        return await api_brain.set_stats_async(bot_id = self.id, api_token = self.api_token, guild_count = guild_count, shard_count = shard_count, error_on_ratelimit = self.error_on_ratelimit, debug = self.debug)
    
    def set_stats(self, guild_count: int, shard_count: Optional[int] = None) -> IBLAPIResponse:
        """
            Posts bot stats to the IBL API synchronously

            :param guild_count: Amount of servers your bot is in

            :param shard_count: Amount of shards your bot is in. This is optional

            :return: This will always be returned unless something goes wrong, in which case you will get an exception
            :rtype: IBLAPIResponse
        """
        sync_api()
        return api_brain.set_stats_sync(bot_id = self.id, api_token = self.api_token, guild_count = guild_count, shard_count = shard_count, error_on_ratelimit = self.error_on_ratelimit, debug = self.debug)
    
    def get_bot(self):
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
        return api_brain.get_bot_sync(bot_id = self.id, error_on_ratelimit = self.error_on_ratelimit, debug = self.debug)

    async def get_bot_async(self):
        """
            Asynchronously get a bot. This does not take any parameters.

            :return: If the bot was not found or if IBLPy could not parse the JSON request for any reason
            :rtype: None

            :return: This will be returned if you are ratelimited
            :rtype: IBLAPIResponse

            :return: This is the bot object returned from the API
            :rtype: IBLBot
        """
        async_api()
        return await api_brain.get_bot_async(bot_id = self.id, error_on_ratelimit = self.error_on_ratelimit, debug = self.debug)

class UserClient():
    """
        Initialize a Infinity Bots List (IBL) User Client. You can use this to get user stats!
            
        :param id: The User ID you wish to use with the IBL API

        :param error_on_ratelimit: A boolean to indicate whether we should error with a IBLAPIRatelimit or simply return a IBLAPIResponse on a ratelimit error. Defaults to True
    
        :param debug: Whether to run in debug mode. Defaults to False.
    """
    def __init__(self, id: int, error_on_ratelimit: bool = True, debug: bool = False):
        self.id = id
        self.error_on_ratelimit = error_on_ratelimit
        self.debug = debug

    def get_user(self):
        """
            Synchronously get a user. This does not take any parameters.

            :return: If the user was not found or if IBLPy could not parse the JSON request for any reason
            :rtype: None

            :return: This will be returned if you are ratelimited
            :rtype: IBLAPIResponse

            :return: This is the user object returned from the API
            :rtype: IBLUser

        """
        sync_api()
        return api_brain.get_user_sync(user_id = self.id, error_on_ratelimit = self.error_on_ratelimit, debug = self.debug)

    async def get_user_async(self):
        """
            Asynchronously get a user. This does not take any parameters.

            :return: If the user was not found or if IBLPy could not parse the JSON request for any reason
            :rtype: None

            :return: This will be returned if you are ratelimited
            :rtype: IBLAPIResponse

            :return: This is the user object returned from the API
            :rtype: IBLUser
        """
        async_api()
        return await api_brain.get_user_async(user_id = self.id, error_on_ratelimit = self.error_on_ratelimit, debug = self.debug)

class AutoPoster():
    """
        This is IBL Auto Poster. It will post stats for you on an interval you decide and it will then run a function of your choice (if requested) after posting each time.

        You can stop a Auto Poster by calling the ``stop`` function.

        :param interval: How long to wait each time you post. It is required to use at least 5 minutes which is 300 seconds. Specifying a value below 300 seconds will set the interval to 300 seconds anyways

        :param botcli: The IBL BotClient of the bot you want to post stats for. It must have the API token set either during initialization or afterwards by setting the api_token parameter

        :param discli: The discord.Client (or like interfaces like discord.Bot/discord.AutoShardedBot) of the bot you want to post stats for. If you wish to add shard counts, please give a discord.AutoShardedClient and pass sharding = True

        :param on_post: The function to call after posting. Set to None if you don't want this. This function needs to accept three arguments, the guild count sent, the shard count set and the response (which will either be a IBLAPIResponse, a IBLAPIRatelimit or None). Shard count will be None if sharding is disabled

        :param sharding: Whether we should post sharding as well. Requires a discord.AutoShardedClient
    """
    def __init__(self, interval: int, botcli: BotClient, discli: discord.Client, sharding = None, on_post = None):
        if interval > 300:
            self.interval = interval
        else:
            self.interval = 300
        self.botcli = botcli
        self.discli = discli
        self.on_post = on_post
        self.sharding = sharding
        self.keep_running = True
        self.task = None

    async def autoposter(self):
        """This is the autoposting function that is run by the ``start`` function here (using asyncio.create_task)"""
        while True:
            if not self.keep_running:
                self.keep_running = True
                print("IBLPy: AutoPoster has exited successfully!")
                return

            if self.interval < 300:
                self.interval = 300

            try:
                if self.sharding in [False, None]:
                    res = await self.botcli.set_stats_async(len(self.discli.guilds))
                else:
                    res = await self.botcli.set_stats_async(len(self.discli.guilds), len(self.discli.shards))
                if self.on_post:
                    if self.sharding in [False, None]:
                        await self.on_post(len(self.discli.guilds), None, res)
                    else:
                        await self.on_post(len(self.discli.guilds), len(self.discli.shards), res)
                print(f"IBLPy: Stats posted successfully at {time.time()}")
            except Exception as ex:
                print(f"IBLPy: Could not post stats because: {ex}")
            await asyncio.sleep(self.interval)

    def start(self):
        """Starts the auto poster using asyncio.create_task and returns the created task. This must be done in the on_ready function in discord.py"""
        self.task = asyncio.create_task(self.autoposter())
        return self.task

    def stop(self):
        """
            Stops the auto poster by setting the ``keep_running`` attribute to False. Since the exact name may change, it is recommended to use ``stop`` instead of manually setting the attribute.

            The autoposter will only stopped after the interval specified

            This will return the autoposter asyncio task
        """
        self.keep_running = False
        print("IBLPy: AutoPoster is stopping... Waiting for it to next wake up to post stats")
        return self.task

class Webhook():
    """
        This is an IBLPy webhook. It takes a BotClient, your webhook secret and the awaitable/asyncio corouting to call after getting a vote. To start your webhook:

            Use start_ws_task if you are running this in discord.py. make sure you start the webhook in your on_ready event (at the very end of it since it's blocking)

            Use start_ws_normal if you are running this seperately from discord.py. It will be run using asyncio.run instead of asyncio.create_task

            Use the start_ws coroutine if you want to run the webhook yourself using asyncio

            Use create_app if you want to get the FastAPI ASGI app and deploy the webhook using your own server. Uvicorn still needs to be installed even if you use a different ASGI server
    """
    def __init__(self, botcli: BotClient, coro: object, secret: str = None):
        if "webhook" not in api_modes:
            raise InvalidMode("fastapi")
        self.botcli = botcli
        self.secret = secret
        self.coro = coro

    def start_ws_task(self, route, port = 8012):
        """
            Start webhook using asyncio.create_task (discord.py). Use this in a discord.py on_ready event (at the very end of it since it's blocking).
        """
        asyncio.create_task(self.start_ws(route, port = port))

    def start_ws_normal(self, route, port = 8012):
        """
            Start webhook using asyncio.run for normal non-discord.py usecases
        """
        asyncio.run(self.start_ws(route, port = port))

    def create_app(self, route):
        """Creates a FastAPI ASGI app and returns it so you can deploy it how you want to deploy it"""
        ws.wh_func = self.coro
        ws.botcli = self.botcli
        ws.secret = self.secret
        app = fastapi.FastAPI(docs_url = None, redoc_url = None)
        app.include_router(
            router = ws.router,
            prefix=route,
        )
        return app

    async def start_ws(self, route, port = 8012):
        """
            Coroutine to start webhook using any asyncio method you want.
        """
        server = uvicorn.Server(uvicorn.Config(self.create_app(route), host = "0.0.0.0", port = port))
        await server.serve()
        try:
            os._exit()
        except:
            os._exit(0)

import IBLPy.config as cfg
import IBLPy.api_brain as api_brain
from IBLPy.base_fn import async_api, sync_api
from typing import Optional
class Client():
    """
        Initialize a Infinity Bots List (IBL) Client

        **Parameters**
            
        *id* - The Bot/User ID you wish to use with the IBL API

        *api_token* - The API Token of your bot. Do not provide this if you are using the IBL API as a user

        *error_on_ratelimit* - A boolean to indicate whether we should error with a IBLAPIRatelimit or simply return a IBLAPIResponse on a ratelimit error

        *user* - What type of user we are. This should be one of "bot" or "user"

    """

    def __init__(self, id: int, api_token: Optional[str] = "", error_on_ratelimit: bool = True, user: str = "bot"):
        self.id = id
        self.api_token = api_token
        self.api_url = cfg.api
        self.user = user
        self.error_on_ratelimit = error_on_ratelimit

    async def set_stats_async(self, guild_count: int, shard_count: Optional[int] = None):
        """
            Posts bot stats to the IBL API asynchronously

            **Parameters**
            
            *guild_count* - Amount of servers your bot is in

            *shard_count* - Amount of shards your bot is in. This is optional

        """
        async_api()
        bot_only(user)
        return await api_brain.set_stats_async(bot_id = self.id, api_token = self.api_token, guild_count = guild_count, shard_count = shard_count, error_on_ratelimit = self.error_on_ratelimit)
    
    def set_stats_sync(self, guild_count: int, shard_count: Optional[int] = None):
        """
            Posts bot stats to the IBL API synchronously

            **Parameters**
            
            *guild_count* - Amount of servers your bot is in

            *shard_count* - Amount of shards your bot is in. This is optional

        """
        sync_api()
        bot_only(user)
        return api_brain.set_stats_sync(bot_id = self.id, api_token = self.api_token, guild_count = guild_count, shard_count = shard_count, error_on_ratelimit = self.error_on_ratelimit)
    
    def set_stats(self, guild_count: int, shard_count: Optional[int] = None):
        """This is a shortcut to the ``set_stats_sync`` function"""
        sync_api()
        bot_only(user)
        return self.set_stats_sync(guild_count, shard_count) # Shortcut to set_stats_sync


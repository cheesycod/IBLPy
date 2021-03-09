import IBLPy.config as cfg
import IBLPy.api_brain as api_brain
from IBLPy.base_fn import async_api, sync_api
from typing import Optional
class InfinityBotsClient():
    def __init__(self, bot_id: int, api_token: str, error_on_ratelimit = True):
        """Initialize an Infinity Bots List Client"""
        self.bot_id = bot_id
        self.api_token = api_token
        self.api_url = cfg.api
        self.error_on_ratelimit = error_on_ratelimit

    @async_api
    async def set_stats_async(self, guild_count: int, shard_count: Optional[int] = None):
        return await api_brain.set_stats_async(bot_id = self.bot_id, api_token = self.api_token, guild_count = guild_count, shard_count = shard_count, error_on_ratelimit = self.error_on_ratelimit)
    
    @sync_api
    def set_stats_sync(self, guild_count: int, shard_count: Optional[int] = None):
        return api_brain.set_stats_sync(bot_id = self.bot_id, api_token = self.api_token, guild_count = guild_count, shard_count = shard_count, error_on_ratelimit = self.error_on_ratelimit)
    
    @sync_api
    def set_stats(self, guild_count: int, shard_count: Optional[int] = None):
        return self.set_stats_sync(guild_count, shard_count) # Shortcut to set_stats_sync

class IBLCli(InfinityBotsClient):
    pass # This is just a shortcut to InfinityBotsClient

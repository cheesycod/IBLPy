import IBLPy.config as cfg
from IBLPy.base_fn import async_api, sync_api, IBLAPIResponse, IBLAPIRatelimit, IBLBot, IBLUser
import aiohttp
from typing import Optional
from loguru import logger
try:
    import orjson as json_lib
except:
    logger.warning("Orjson could not be imported... falling back to json. Performance will be decreased")
    import json as json_lib

class IBLHTTP():
    user_agent = f"IBLPy/{cfg.version}"
    
    def __init__(self):
        self.logged_in = False

    def login(self, bot_id, api_token):
        self.bot_id = bot_id
        self.api_token = api_token
        self.logged_in = True
        
    
    async def _request(self, method, url, json, headers, auth = None):
        if auth:
            headers["authorization"] = auth
            
        async with aiohttp.ClientSession() as sess:
            f = getattr(sess, method.lower())
            async with f(url, headers = headers, json = json) as res:
                if res.status == 429:
                    raise IBLAPIRatelimit()
           
                # Convert it to json
                i = 0
                json = await res.body()
                while isinstance(json, (bytes, str)) and i < 100:
                    json = json_lib.loads(json)
                    i+=1
                
                success = True if res.status == 200 else False           
                message = json.get("message")
            
                logger.debug(json)
            
            return IBLAPIResponse(raw_res = res, success = success, json = json, message = message, status = res.status)
        
    async def set_stats(
        guild_count: int, 
        shard_count: Optional[int] = 0
    ):
        if not self.logged_in:
            raise ValueError("Not logged in to IBL yet")
        
        json = {"servers": guild_count, "shards": shard_count}
        headers = {"authorization": self.api_token, "User-Agent": user_agent}
        return await self._request("POST",

    
async def get_bot(bot_id: int):
    headers = {"User-Agent": user_agent, "Content-Type": "application/json"}
    res = await requests_async.get(f"{cfg.api}/bot/{bot_id}", headers = headers)
    try:
        json = json_lib.loads((await res.json()))
    except:
        try:
            json = await res.json()
        except:
            json = {"message": "IBLPy: Could not deserialize data. Potential server error or malformed request", "error": True}

    if res.status == 429 and error_on_ratelimit:
        raise IBLAPIRatelimit()
    if res.status == 429:
        return IBLAPIResponse(raw_res = res, success = False, data = json, message = json.get("message"), status = res.status)
    if json.get("error"):
        return None
    if debug:
        print(f"DEBUG: {json}")
    del json["error"] # Delete the error
    json["id"] = bot_id
    return IBLBot(**json)


async def get_user(user_id: int, debug: bool = False):
    headers = {"User-Agent": user_agent, "Content-Type": "application/json"}
    res = await requests_async.get(f"{cfg.api}/user/{user_id}", headers = headers)
    # Workaround requests.json() sometimes giving string instead of dict due to IBL putting \\'s in API Responses and breaking Python JSON serialization
    try:
        json = json_lib.loads((await res.json()))
    except:
        try:
            json = await res.json()
        except:
            json = {"message": "IBLPy: Could not deserialize data. Potential server error or malformed request", "error": True}

    if res.status == 429 and error_on_ratelimit:
        raise IBLAPIRatelimit()
    if res.status == 429:
        return IBLAPIResponse(raw_res = res, success = False, data = json, message = json.get("message"), status = res.status)
    if json.get("error"):
        return None
    if debug:
        print(f"DEBUG: {json}")
    del json["error"] # Delete the error
    json["id"] = user_id
    return IBLUser(**json)


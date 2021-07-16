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

user_agent = f"IBLPy/{cfg.version}"


async def set_stats(
    api_token: str, 
    bot_id: int, 
    guild_count: int, 
    shard_count: Optional[int] = 0
):
    json = {"servers": guild_count, "shards": shard_count}
    headers = {"Authorization": api_token, "User-Agent": user_agent}
    
    async with aiohttp.ClientSession() as sess:
        async with sess.post(f"{cfg.api}/bot/{bot_id}", headers = headers, json = json) as res:
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
            
        return IBLAPIResponse(raw_res = res, success = success, data = json, message = message, status = res.status)

    
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

def get_user_sync(user_id: int, error_on_ratelimit: bool, debug: bool = False):
    headers = {"User-Agent": user_agent, "Content-Type": "application/json"}
    res = requests.get(f"{cfg.api}/user/{user_id}", headers = headers)
    # Workaround requests.json() sometimes giving string instead of dict due to IBL putting \\'s in API Responses and breaking Python JSON serialization
    try:
        json = json_lib.loads((res.json()))
    except:
        try:
            json = res.json()
        except:
            json = {"message": "IBLPy: Could not deserialize data. Potential server error or malformed request", "error": True}

    if res.status_code == 429 and error_on_ratelimit:
        raise IBLAPIRatelimit()
    if res.status_code == 429:
        return IBLAPIResponse(raw_res = res, success = False, data = json, message = json.get("message"), status = res.status_code)
    if debug:
        print(f"DEBUG: {json}")
    if json.get("error"):
        return None
    del json["error"] # Delete the error
    json["id"] = user_id
    return IBLUser(**json)

async def get_user_async(user_id: int, error_on_ratelimit: bool, debug: bool = False):
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


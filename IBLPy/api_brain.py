import IBLPy.config as cfg
from IBLPy.base_fn import async_api, sync_api, IBLAPIResponse, IBLAPIRatelimit, IBLBot, IBLUser
from IBLPy import requests, requests_async
from typing import Optional
try:
    import orjson as json_lib
except:
    print("WARNING: orjson is not found... falling back to json")
    import json as json_lib

user_agent = f"IBLPy/{cfg.version}"

def set_stats_sync(api_token: str, bot_id: int, guild_count: int, error_on_ratelimit: bool, shard_count: Optional[int] = None, debug: bool = False):
    json = {"servers": guild_count}
    if shard_count is not None:
        json["shards"] = shard_count
    else:
        json["shards"] = 0
    headers = {"authorization": api_token, "User-Agent": user_agent}
    res = requests.post(f"{cfg.api}/bot/{bot_id}", headers = headers, data = json)
    
    if res.status_code == 429 and error_on_ratelimit:
        raise IBLAPIRatelimit()

    # Workaround requests.json() sometimes giving string instead of dict due to IBL putting \\'s in API Responses and breaking Python JSON serialization
    try:
        json = json_lib.loads(res.json())
    except:
        json = res.json()

    if res.status_code == 200:
        success = True
        message = json.get("message")
    else:
        success = False
        message = json.get("message")
    if debug:
        print(f"DEBUG: {message}")
    return IBLAPIResponse(raw_res = res, success = success, data = json, message = message, status = res.status_code)

async def set_stats_async(api_token: str, bot_id: int, guild_count: int, error_on_ratelimit: bool, shard_count: Optional[int] = None, debug: bool = False):
    json = {"servers": guild_count}
    if shard_count is not None:
        json["shards"] = shard_count
    else:
        json["shards"] = 0
    headers = {"authorization": api_token, "User-Agent": user_agent}
    res = await requests_async.post(f"{cfg.api}/bot/{bot_id}", headers = headers, data = json)
    if res.status == 429 and error_on_ratelimit:
        raise IBLAPIRatelimit()

    # Workaround requests.json() sometimes giving string instead of dict due to IBL putting \\'s in API Responses and breaking Python JSON serialization
    try:
        json = json_lib.loads((await res.json()))
    except:
        try:
            json = await res.json()
        except:
            json = {"message": "IBLPy: Could not deserialize data. Potential server error or malformed request"}

    if res.status == 200:
        success = True
        message = json.get("message")
    else:
        success = False
        message = json.get("message")
    if debug:
        print(f"DEBUG: {message}")
    return IBLAPIResponse(raw_res = res, success = success, data = json, message = message, status = res.status)

def get_bot_sync(bot_id: int, error_on_ratelimit: bool, debug: bool = False):
    headers = {"User-Agent": user_agent, "Content-Type": "application/json"}
    res = requests.get(f"{cfg.api}/bot/{bot_id}", headers = headers)
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
    if json.get("error"):
        return None
    del json["error"] # Delete the error
    if debug:
        print(f"DEBUG: {json}")
    json["id"] = bot_id
    return IBLBot(**json)

async def get_bot_async(bot_id: int, error_on_ratelimit: bool, debug: bool = False):
    headers = {"User-Agent": user_agent, "Content-Type": "application/json"}
    res = await requests_async.get(f"{cfg.api}/bot/{bot_id}", headers = headers)
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


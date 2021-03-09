api_modes = []
try:
    import aiohttp
    from aiohttp_requests import requests as requests_async
    api_modes.append("async")
except:
    requests_async = None

try:
    import requests
    api_modes.append("sync")
except:
    requests = None

if api_modes == []:
    raise ibl_base.NoSuitableModesFound()

from IBLPy.base_fn import *
from IBLPy.main import IBLCli
from IBLPy.config import *
from IBLPy.api_brain import *

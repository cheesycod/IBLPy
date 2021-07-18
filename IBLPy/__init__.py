api_modes = []
try:
    import aiohttp
    api_modes.append("async")
except Exception:
    raise ImportError("You must have aiohttp installed to import this library!")
    
try:
    import uvicorn
    import fastapi
    api_modes.append("webhook")
except:
    uvicorn = None
    fastapi = None

import discord

from IBLPy.main import *
from IBLPy.config import *
from IBLPy.ws import *

__version__ = version

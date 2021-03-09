import IBLPy, asyncio

async def got_vote(vote, secret):
    print("Got vote:", vote, "with secret:", secret)

ibl = IBLPy.BotClient(bot_id = 733766762658529360, api_token = "mG4qsvkpF89g3vXdlipDK44DGAXFEcvPlA2iSpwGd9Azt2l2XDh3CmPIzKmeXcmHznMntMC3ghKmmKWQ5iQuhpyYPzSI2XSvm1kZ")
try:
    bot = asyncio.run(ibl.get_bot_async())
except:
    pass
a = IBLPy.Webhook(ibl, secret = "MY_SECRET")
#a.start_ws_normal("", func = got_vote)

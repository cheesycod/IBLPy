import IBLPy, asyncio, discord
from testcfg import TOKEN

async def got_vote(vote, secret):
    print("Got vote:", vote, "with secret:", secret)

async def test_poster(gc, sc, res):
    print(gc, sc, res)

ibl = IBLPy.BotClient(id = 733766762658529360, api_token = "mG4qsvkpF89g3vXdlipDK44DGAXFEcvPlA2iSpwGd9Azt2l2XDh3CmPIzKmeXcmHznMntMC3ghKmmKWQ5iQuhpyYPzSI2XSvm1kZ")
client = discord.AutoShardedClient()

@client.event
async def on_message(msg):
    print(msg)

@client.event
async def on_ready():
    print(f"Ready! {client.user}")
    #ibl.get_bot()
    a = IBLPy.Webhook(botcli = ibl, secret = "MY_SECRET", coro = got_vote)
    ap = IBLPy.AutoPoster(interval = 300, botcli = ibl, discli = client, on_post = test_poster, sharding = True)
    ap.start()
    a.start_ws_task(route = "/ibl", port = 8016)

client.run(TOKEN)

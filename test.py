import IBLPy, asyncio, discord

async def got_vote(vote, secret):
    print("Got vote:", vote, "with secret:", secret)

async def test_poster(gc, sc):
    print(gc, sc)

ibl = IBLPy.BotClient(id = 733766762658529360, api_token = "mG4qsvkpF89g3vXdlipDK44DGAXFEcvPlA2iSpwGd9Azt2l2XDh3CmPIzKmeXcmHznMntMC3ghKmmKWQ5iQuhpyYPzSI2XSvm1kZ")
client = discord.Client()

@client.event
async def on_message(msg):
    print(msg)

@client.event
async def on_ready():
    print(f"Ready! {client.user}")
    a = IBLPy.Webhook(ibl, secret = "MY_SECRET")
    ap = IBLPy.AutoPoster(5, ibl, client, on_post = test_poster)
    ap.start()
    a.start_ws_task("", func = got_vote)

client.run("NzMzNzY2NzYyNjU4NTI5MzYw.XxH7jA.y-6v7EXfequjeC0WjZKw3n2EeL8")

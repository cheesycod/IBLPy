import sys
sys.path.append(".")
import IBLPy, asyncio, discord
from testcfg import TOKEN

async def got_vote(vote, secret):
    print("Got vote:", vote, "with secret:", secret)

async def test_poster(gc, sc, res):
    print(gc, sc, res)

ibl = IBLPy.BotClient(
    bot_id = 733043768692965448,
    api_token="ySnVkMTSl4bjVJdHxy3nQnj2t2IQmKuuZUdojBCvkseyfQKuqjgS5x1idSKgUS3nLcgwtqHX8KEEe1VHuAbbw7U55VdQfrFs9hYy"
)
client = discord.AutoShardedClient()

@client.event
async def on_message(msg):
    print(msg)

@client.event
async def on_ready():
    print(f"Ready! {client.user}")
    print("Has Rootspring voted?")
    r = await ibl.has_user_voted(563808552288780322)
    print(r)
    print("Rootsprings user info")
    r = await IBLPy.UserClient(563808552288780322).get_user()
    print(r)
    r = await ibl.get_bot()
    print(r, r.servers, r.views, r.website, vars(r))
    a = IBLPy.Webhook(botcli = ibl, secret = "MY_SECRET", coro = got_vote)
    ap = IBLPy.AutoPoster(interval = 300, botcli = ibl, discli = client, on_post = test_poster, sharding = True)
    ap.start()
    a.start_ws_task(route = "/ibl", port = 8016)

client.run(TOKEN)

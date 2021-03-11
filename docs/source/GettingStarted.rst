Getting Started
===============

Using IBLPy is easy. Here, we will assume you are just using this to post stats using our autoposter and a webhook. The first thing you will need to do is create a Bot Client. A Bot Client is the base of all bot operations on IBLPy (there is also a User Client as the base of all user operations on IBLPy). 

You can create a Bot Client like this::

   ibl = IBLPy.BotClient(id = bot_id, api_token = api_token_here)

Replace bot_id and api_token_here with your bots ID and the api token (you don't have to give your api token and you can remove this parameter altogether if you just need to get the bot, but for autoposting and stat posting, you need to provide an API Token)

Next setup discord.py normally. You will get something like this (the exact discord.py Client you use may be different)::

   ibl = IBLPy.BotClient(id = bot_id, api_token = api_token_here
   client = discord.Client()

   @client.event
   async def on_ready():
        # This part is important, make sure you have this on_ready event.
        # Everything we do about autoposting and webhooks will be done here

   client.run(BOT_TOKEN)

The on_ready event is where we will do our autoposting and webhooks. If you are not using discord.py, please check the Documentation for which functions you have to use.)

**Autoposting**

Next, we need to create an AutoPoster inside our on_ready function. To do so, add something like the below code snippet to your on_ready function::

   ap = IBLPy.AutoPoster(interval = 300, botcli = ibl, discli = client, on_post = None, sharding = False)
   ap.start() # Starts the autoposter in the background

If you run this right now, you will see that it does post stats every 5 minutes and also logs it. Log configuration ia upcoming and will use logging. It is not currently possible to stop a started AutoPoster. Submit a PR on GitHub if you want to add this. The interval must be in seconds and if it is below the 5 minutes or 300 seconds above, it will automatically be set to 5 minutes. This is to prevent ratelimits, which are strict on IBL

**Webhooks**

Since webhooks are blocking, you must put it at the end of your on_ready function or nothing below it in on_ready will be executed. To setup webhooks, add something like the below code snippet to your on_ready function. The webhook secret is the one you configured in IBL, use None if you don't want to use one, not recommended to use None however as this allows anyone to use your webhook freely including non-IBL users. IBLPy will check the webhook and return 401 is the secret is invalid thus allowing only IBL to use your webhook. The route parameter below is what route to use for your webhook, func is the async coroutine to run when you get a vote and must be awaitable and must accept a vote parameter containing the vote, port is the port the webhook should listen at (the below webhook is running at http://0.0.0.0:8016/ibl/webhook). You can now tunnel/reverse proxy this and add your webhook to IBL::

   wh = IBLPy.Webhook(botcli = ibl, secret = "YOUR WEBHOOK SECRET")
   wh.start_ws_task(route = "/ibl/webhook", func = get_vote, port = 8016)

If you run this now, you will have discord.py, autoposting and webhooks working simultaneously! You're done!

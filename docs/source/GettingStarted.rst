Getting Started
===============

Using IBLPy is easy. Here, we will assume you are just using this to post stats using our autoposter and a webhook. The first thing you will need to do is create a Bot Client. A Bot Client is the base of all bot operations on IBLPy (there is also a User Client as the base of all user operations on IBLPy). 

You can create a Bot Client like this::

   ibl = BotClient(id = bot_id, api_token = api_token_here)

Replace bot_id and api_token_here with your bots ID and the api token (you don't have to give your api token and you can remove this parameter altogether if you just need to get the bot, but for autoposting and stat posting, you need to provide an API Token)

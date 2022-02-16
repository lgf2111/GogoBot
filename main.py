from discord.ext import commands
from discord_slash import SlashCommand
from keep_alive import keep_alive
import os
from dotenv import load_dotenv
import logging

format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(format)
ch.setLevel(logging.INFO)
logger.addHandler(ch)

fh = logging.FileHandler('output.log')
fh.setFormatter(format)
fh.setLevel(logging.INFO)
logger.addHandler(fh)

load_dotenv()
client = commands.Bot(command_prefix='gogo.')
slash = SlashCommand(client, sync_commands=True)
token = os.environ['TOKEN']


@client.command()
async def reload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
    finally:
        client.load_extension(f'cogs.{extension}')
        logger.info(f'cogs.{extension} has been reloaded')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# @client.event
# async def on_ready():
#   await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="anime"))
#   print(f"Logged in as {client.user}")


# @slash.slash(name="set", description="set new anime to track")
# async def ping(ctx):
#     await ctx.send("Pong!")


# anime = 'shingeki-no-kyojin-the-final-season-part-2'
# base_url = f'https://gogoanime.film/{anime}'
# counter = 1
# while True:
#     url = f'{base_url}-episode-{counter}'
#     data = str(requests.get(url).text.encode('utf-8'))
#     if '<h1 class="entry-title">404</h1>' not in data:
#         print(f"Episode {counter} had just came out!")
#         counter += 1
#     else:
#         print('404')
#         time.sleep(1)



keep_alive()
client.run(token)
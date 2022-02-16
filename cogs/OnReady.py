import discord
from discord.ext import commands
import logging

logger = logging.getLogger()


class OnReady(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'{self.client.user} is online')
        
    @commands.command()
    async def ping(self, ctx):
        logger.info(f'{ctx.message.author} has just pinged')
        await ctx.send(f'Pong! ({round(self.client.latency, 1)}ms)')

def setup(client):
    client.add_cog(OnReady(client))
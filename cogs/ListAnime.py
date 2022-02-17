from discord.ext import commands
from discord import Embed
import logging

logger = logging.getLogger()

class ListAnime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def list(self, ctx):
        """List all animes added to track"""
        msg = ctx.message
        usr = msg.author
        cmd = msg.content
        base_url = 'https://gogoanime.film/category/'
        with open('db.txt', 'r') as f:
            db = eval(f.read())
        if db.get(usr.id):
            await ctx.send(f'{usr.mention}\'s list ({len(db[usr.id])} anime(s))')
            for i in range(len(db[usr.id])):
                url = base_url+'-'.join(_.lower() for _ in db[usr.id][i][0].split())
                await ctx.send(url)
        else:
            await ctx.send('No anime added.')

def setup(client):
    client.add_cog(ListAnime(client))
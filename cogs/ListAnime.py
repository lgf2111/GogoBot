from discord.ext import commands
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
        with open('db.txt', 'r') as f:
            db = eval(f.read())
        await ctx.send('\n'.join([f'{i+1}. {db[i][0]}' for i in range(len(db))]) if db else 'No anime added yet')

def setup(client):
    client.add_cog(ListAnime(client))
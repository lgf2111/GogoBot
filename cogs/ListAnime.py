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
        gld = ctx.guild
        usr = msg.author
        cmd = msg.content
        base_url = 'https://gogoanime.gg/category/'
        with open('db.txt', 'r') as f:
            db = eval(f.read())
        gld_db = db[gld.id][1]
        if gld_db.get(usr.id):
            await ctx.send(f'{usr.mention}\'s list ({len(gld_db[usr.id])} anime(s))')
            for i in range(len(gld_db[usr.id])):
                url = base_url+'-'.join(_.lower() for _ in gld_db[usr.id][i][0].split())
                await ctx.send(url)
        else:
            await ctx.send('No anime added.')

def setup(client):
    client.add_cog(ListAnime(client))
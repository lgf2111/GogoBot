import discord
from discord.ext import commands
import logging

logger = logging.getLogger()

class Setup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def setup(self, ctx):
        """Setup for new server"""
        msg = ctx.message
        gld = ctx.guild
        cmd = msg.content
        # gld = int(cmd[cmd.find('/channels/')+10:cmd.rfind('/')])
        chn = int(cmd[cmd.rfind('/')+1:])
        # if gld.id != cmd gld
        with open('db.txt', 'r') as f:
            db = eval(f.read())
        db[gld.id] = [chn, {}]
        with open('db.txt', 'w') as f:
            f.write(str(db))
        chn = discord.utils.get(ctx.guild.channels, id=chn)
        await ctx.send(f'Notifications will be sent to {chn.name}.')

def setup(client):
    client.add_cog(Setup(client))
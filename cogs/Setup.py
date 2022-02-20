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
        usr = msg.author
        cmd = msg.content
        
        if len(cmd.split()) == 1:
            await ctx.send('Enter the channel link beside this command.\n'
                           'Example: gogo.setup https://discord.com/channels/123456789012345678/123456789012345678')

        elif len(cmd.split()) > 2:
            await ctx.send('Invalid channel link.\n'
                           'Enter the channel link beside this command.\n'
                           'Example: gogo.setup https://discord.com/channels/123456789012345678/123456789012345678')
                           
        else:
            gld_id = int(cmd[cmd.find('/channels/')+10:cmd.rfind('/')])
            chn = int(cmd[cmd.rfind('/')+1:])
            if gld.id == gld_id:
                with open('db.txt', 'r') as f:
                    db = eval(f.read())
                if db.get(gld.id):
                    db[gld.id][0] = chn
                else:
                    db[gld.id] = [chn, {}]
                with open('db.txt', 'w') as f:
                    f.write(str(db))
                chn = discord.utils.get(ctx.guild.channels, id=chn)
                logger.info(f'{usr} has setup guild {gld.name} to be notified at channel {chn.name}.')
                await ctx.send(f'Notifications will be sent at {chn.name}.')
            else:
                await ctx.send('Please copy channel link from this server.')

def setup(client):
    client.add_cog(Setup(client))
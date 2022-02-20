import discord
from discord.ext import commands, tasks
import logging
import requests

logger = logging.getLogger()


class OnReady(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="anime"))
        self.track.start()
        logger.info(f'{self.client.user} is online.')

    @tasks.loop(minutes=1)
    async def track(self):
        with open('db.txt', 'r') as f:
            db = eval(f.read())
        for gld in self.client.guilds:
            chn = self.client.get_channel(db[gld.id][0])
            gld_db = db[gld.id][1]
            base_url = f'https://gogoanime.film/'
            for usr in gld_db:
                for i in range(len(gld_db[usr])):
                    title, episode = gld_db[usr][i]
                    anime = '-'.join([_.lower() for _ in title.split()])
                    url = f'{base_url}{anime}'
                    link = f'{url}-episode-{episode}'
                    data = str(requests.get(link).text.encode('utf-8'))
                    logger.info(f'Pinged {link}.')
                    if '<h1 class="entry-title">404</h1>' not in data:
                        await chn.send(f'Good news <@{usr}>!\n'
                                       f'{title} episode {episode} has just came out!\n'+link)
                        gld_db[usr][i][1] += 1
                        db[gld.id][1] = gld_db
                        with open('db.txt', 'w') as f:
                            f.write(str(db))

    @commands.command()
    async def ping(self, ctx):
        """Ping the bot to get the latency"""
        msg = ctx.message
        usr = msg.author
        chn = msg.channel
        logger.info(f'{usr} from {chn} has just pinged.')
        await ctx.send(f'{usr.mention}\nPong! ({round(self.client.latency, 1)}ms)')

def setup(client):
    client.add_cog(OnReady(client))
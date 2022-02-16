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
        logger.info(f'{self.client.user} is online')

    @tasks.loop(seconds=1)
    async def track(self):
        chn = self.client.get_channel(943609240474517534)
        with open('db.txt', 'r') as f:
            db = eval(f.read())
        base_url = f'https://gogoanime.film/'
        for i in range(len(db)):
            title, episode = db[i]
            anime = '-'.join([_.lower() for _ in title.split()])
            url = f'{base_url}{anime}'
            link = f'{url}-episode-{episode}'
            data = str(requests.get(link).text.encode('utf-8'))
            if '<h1 class="entry-title">404</h1>' not in data:
                await chn.send(f'{title} episode {episode} has just came out!\n'+link)
                db[i][1] += 1
                with open('db.txt', 'w') as f:
                    f.write(str(db))

    @commands.command()
    async def ping(self, ctx):
        msg = ctx.message
        usr = msg.author
        chn = f'{msg.channel}({msg.channel.id})'
        """Ping the bot to get the latency"""
        logger.info(f'{usr} from {chn} has just pinged.')
        await ctx.send(f'Pong! ({round(self.client.latency, 1)}ms)')

def setup(client):
    client.add_cog(OnReady(client))
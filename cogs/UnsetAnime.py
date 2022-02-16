from discord.ext import commands
import logging

logger = logging.getLogger()

class UnsetAnime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def unset(self, ctx):
        msg = ctx.message
        usr = msg.author
        cmd = msg.content
        
        if len(cmd.split()) == 1:
            await ctx.send('Enter the anime link of any episode beside this command\n'
                            'Example: gogo.unset https://gogoanime.film/shingeki-no-kyojin-the-final-season-part-2-episode-1')
        elif len(cmd.split()) > 2:
            await ctx.send('Invalid anime link\n'
                            'Enter the anime link of any episode beside this command\n'
                            'Example: gogo.unset https://gogoanime.film/shingeki-no-kyojin-the-final-season-part-2-episode-1')
        else:
            link = cmd.split()[1]
            anime = link[link.find('https://gogoanime.film/')+23:link.rfind('-episode')]
            title = ' '.join([_.capitalize() for _ in anime.split('-')])
            with open('db.txt', 'r') as f:
                db = eval(f.read())
            if title in db:
                db.remove(title)
                with open('db.txt', 'w') as f:
                    f.write(str(db))
                logging.info(f'{usr} has set tracker for {title}')
                await ctx.send(f'{title} has been unset')
            else:
                await ctx.send(f'{title} has not been set')



def setup(client):
    client.add_cog(UnsetAnime(client))
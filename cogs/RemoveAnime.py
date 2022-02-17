from discord.ext import commands
import logging

logger = logging.getLogger()

class RemoveAnime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def remove(self, ctx):
        """Remove an anime to track"""
        msg = ctx.message
        usr = msg.author
        cmd = msg.content
        
        if len(cmd.split()) == 1:
            await ctx.send('Enter the anime link of any episode beside this command.\n'
                            'Example: gogo.remove https://gogoanime.film/shingeki-no-kyojin-the-final-season-part-2-episode-1')
        elif len(cmd.split()) > 2:
            await ctx.send('Invalid anime link\n'
                            'Enter the anime link of any episode beside this command.\n'
                            'Example: gogo.remove https://gogoanime.film/shingeki-no-kyojin-the-final-season-part-2-episode-1')
        else:
            link = cmd.split()[1]
            anime = link[link.find('https://gogoanime.film/')+23:link.rfind('-episode')]
            title = ' '.join([_.capitalize() for _ in anime.split('-')])
            with open('db.txt', 'r') as f:
                db = eval(f.read())
            for i in range(len(db)):
                if db[i][0] == title:
                    db.remove(db[i])
                    with open('db.txt', 'w') as f:
                        f.write(str(db))
                    logging.info(f'{usr} has removed tracker for {title}.')
                    await ctx.send(f'{title} has been removed.')
                    break
            else:
                await ctx.send(f'{title} has not been added.')



def setup(client):
    client.add_cog(RemoveAnime(client))
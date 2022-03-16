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
        gld = ctx.guild
        usr = msg.author
        cmd = msg.content
        
        if len(cmd.split()) == 1:
            await ctx.send('Enter the anime link of any episode beside this command.\n'
                            'Example: gogo.remove https://gogoanime.gg/shingeki-no-kyojin-the-final-season-part-2-episode-1')
        elif len(cmd.split()) > 2:
            await ctx.send('Invalid anime link\n'
                            'Enter the anime link of any episode beside this command.\n'
                            'Example: gogo.remove https://gogoanime.gg/shingeki-no-kyojin-the-final-season-part-2-episode-1')
        else:
            link = cmd.split()[1]
            if '/category/' in link:
                anime = link[link.find('https://gogoanime.gg/category/')+32:]
            else:
                anime = link[link.find('https://gogoanime.gg/')+21:link.rfind('-episode')]
            title = ' '.join([_.capitalize() for _ in anime.split('-')])
            with open('db.txt', 'r') as f:
                db = eval(f.read())
                gld_db = db[gld.id][1]
            for i in range(len(gld_db[usr.id])):
                if gld_db[usr.id][i][0] == title:
                    gld_db[usr.id].remove(gld_db[usr.id][i])
                    db[gld.id][1] = gld_db
                    with open('db.txt', 'w') as f:
                        f.write(str(db))
                    logging.info(f'{usr} has removed tracker for {title}.')
                    await ctx.send(f'{title} has been removed.')
                    break
            else:
                await ctx.send(f'{title} has not been added.')



def setup(client):
    client.add_cog(RemoveAnime(client))
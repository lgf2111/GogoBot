from discord.ext import commands
import logging

logger = logging.getLogger()
from requests_html import HTMLSession

class AddAnime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def add(self, ctx):
        """Add an anime to track"""
        msg = ctx.message
        gld = ctx.guild
        usr = msg.author
        cmd = msg.content
        
        if len(cmd.split()) == 1:
            await ctx.send('Enter the anime link of any episode beside this command.\n'
                            'Example: gogo.add https://gogoanime.film/shingeki-no-kyojin-the-final-season-part-2-episode-1')

        elif len(cmd.split()) > 2:
            await ctx.send('Invalid anime link.\n'
                            'Enter the anime link of any episode beside this command.\n'
                            'Example: gogo.add https://gogoanime.film/shingeki-no-kyojin-the-final-season-part-2-episode-1')

        else:
            link = cmd.split()[1]
            anime = link[link.find('https://gogoanime.film/')+23:link.rfind('-episode')]
            title = ' '.join([_.capitalize() for _ in anime.split('-')])
            with open('db.txt', 'r') as f:
                db = eval(f.read())
            gld_db = db[gld.id][1]
            if title in [_[0] for _ in gld_db[usr.id]]:
                await ctx.send(f'{title} is already in your list.')
            else:
                base_url = f'https://gogoanime.film/{anime}'
                counter = 0
                while True:
                    counter += 1
                    url = f'{base_url}-episode-{counter}'
                    session = HTMLSession()
                    data = session.get(url)
                    if data.html.find('.entry-title'):
                        if counter == 1:
                            await ctx.send(f'{title} does not exist.')
                        else:
                            if usr.id not in gld_db:
                                gld_db[usr.id] = []
                            gld_db[usr.id].append([title,counter])
                            db[gld.id][1] = gld_db
                            with open('db.txt', 'w') as f:
                                f.write(str(db))
                            logging.info(f'{usr} has added tracker for {title}.')
                            await ctx.send(f'{title} is currently on episode {counter-1}.\n'
                                            f'New episodes will be notified starting from episode {counter}.')
                        break


def setup(client):
    client.add_cog(AddAnime(client))
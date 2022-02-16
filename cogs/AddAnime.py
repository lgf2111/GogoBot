from discord.ext import commands
import logging

logger = logging.getLogger()
import requests

class AddAnime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def add(self, ctx):
        """Add an anime to track"""
        msg = ctx.message
        usr = msg.author
        cmd = msg.content
        
        if len(cmd.split()) == 1:
            await ctx.send('Enter the anime link of any episode beside this command\n'
                            'Example: gogo.add https://gogoanime.film/shingeki-no-kyojin-the-final-season-part-2-episode-1')
        elif len(cmd.split()) > 2:
            await ctx.send('Invalid anime link\n'
                            'Enter the anime link of any episode beside this command\n'
                            'Example: gogo.add https://gogoanime.film/shingeki-no-kyojin-the-final-season-part-2-episode-1')
        else:
            link = cmd.split()[1]
            anime = link[link.find('https://gogoanime.film/')+23:link.rfind('-episode')]
            title = ' '.join([_.capitalize() for _ in anime.split('-')])
            base_url = f'https://gogoanime.film/{anime}'
            counter = 0
            while True:
                counter += 1
                url = f'{base_url}-episode-{counter}'
                data = str(requests.get(url).text.encode('utf-8'))
                if '<h1 class="entry-title">404</h1>' in data:
                    if counter == 1:
                        await ctx.send(f'{title} does not exist')
                    else:
                        with open('db.txt', 'r') as f:
                            db = eval(f.read())
                        db.append([title,counter])
                        with open('db.txt', 'w') as f:
                            f.write(str(db))
                        logging.info(f'{usr} has added tracker for {title}')
                        await ctx.send(f'{title} is currently on episode {counter-1}\n'
                                        f'New episodes will be notified starting from episode {counter}')
                    break


def setup(client):
    client.add_cog(AddAnime(client))
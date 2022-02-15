import discord
from keep_alive import keep_alive
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
token = os.environ['TOKEN']


@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="anime"))
  print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    msg = message.content
    chn = message.channel

    if message.author == client.user:
        return
    
    if msg.startswith('gogo.'):
        cmd = msg[5:]
        if cmd.startswith('set'):
            if len(cmd.split()) == 1:
                await chn.send('Enter the anime link of any episode beside this command\n'
                               'Example: gogo.set https://gogoanime.film/shingeki-no-kyojin-the-final-season-part-2-episode-1')
            elif len(cmd.split()) > 2:
                await chn.send('Invalid anime link\n'
                               'Enter the anime link of any episode beside this command\n'
                               'Example: gogo.set https://gogoanime.film/shingeki-no-kyojin-the-final-season-part-2-episode-1')
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
                            await chn.send(f'{title} does not exist')
                        else:
                            await chn.send(f'{title} is currently on episode {counter-1}\n'
                                           f'New episodes will be notified starting from episode {counter}')
                        break


# anime = 'shingeki-no-kyojin-the-final-season-part-2'
# base_url = f'https://gogoanime.film/{anime}'
# counter = 1
# while True:
#     url = f'{base_url}-episode-{counter}'
#     data = str(requests.get(url).text.encode('utf-8'))
#     if '<h1 class="entry-title">404</h1>' not in data:
#         print(f"Episode {counter} had just came out!")
#         counter += 1
#     else:
#         print('404')
#         time.sleep(1)



keep_alive()
client.run(token)
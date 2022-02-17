from discord.ext import commands
from keep_alive import keep_alive
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import re

# Logger
format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(format)
ch.setLevel(logging.INFO)
logger.addHandler(ch)
fh = TimedRotatingFileHandler('logs/output.log', when='midnight', interval=1)
fh.setFormatter(format)
fh.setLevel(logging.INFO)
fh.suffix = '%Y%m%d'
fh.extMatch = re.compile(r'\d{8}$')
logger.addHandler(fh)

# Essential
client = commands.Bot(command_prefix='gogo.')
token = os.environ['TOKEN']

# Load all cogs
def reload_all():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            extension = filename[:-3]
            try:
                client.unload_extension(f'cogs.{extension}')
            except Exception as e:
                logger.info(f'cogs.{extension} failed to unload.')
            finally:
                client.load_extension(f'cogs.{extension}')
                logger.info(f'cogs.{extension} has been reloaded.')

# Reload Command
@client.command()
async def reload(ctx, extension):
    """Reloads a class"""
    if extension.lower() == 'all':
        reload_all()
    else:
        try:
            client.unload_extension(f'cogs.{extension}')
        except Exception as e:
            logger.info(f'cogs.{extension} failed to unload.')
        finally:
            client.load_extension(f'cogs.{extension}')
            logger.info(f'cogs.{extension} has been reloaded.')

reload_all()
keep_alive()
client.run(token)
from discord.ext import commands
from discord import Intents, LoginFailure
from glob import glob
from logging import getLogger
import traceback

LOG = getLogger(__name__)


class VocalizeCore(commands.Bot):
    def __init__(self, token: str, intents: Intents= Intents.default()):
        self.token = token
        super().__init__(command_prefix='+', intents=intents, enable_debug_events=True)

    async def setup_hook(self):
        extensions = glob('cogs/*.py')
        loaded_extension = []
        for _extension in extensions:
            extension = _extension.removeprefix('cogs/')
            if extension.startswith('_') or extension == '__init__.py':
                LOG.info(f'loading {extension} was skipped.')
            else:
                LOG.info(f'loading extension {extension}')
                print(_extension.replace('/', '.'))
                try:
                    await self.load_extension(_extension.replace('/', '.').replace('.py', ''))
                except Exception as e:
                    LOG.error(f'failed to load extension {extension}: {e}')
                finally:
                    LOG.info(f'loaded extension {extension}')
                    loaded_extension.append(extension)
        LOG.info(f'loaded {len(loaded_extension)} extensions')
        await self.tree.sync()

    async def run(self, is_reconnect: bool= True):
        try:
            await self.start(self.token, reconnect=is_reconnect)

        except KeyboardInterrupt:
            LOG.info('Shutdown...')

        except LoginFailure:
            LOG.error('TOKEN is invalid')

        else:
            LOG.error(traceback.format_exc())

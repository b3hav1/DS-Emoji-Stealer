from re import findall
from requests import get
from disnake import Intents
from disnake.ext.commands import Bot

token = 'PUT YOUR BOT TOKEN HERE'


bot = Bot(command_prefix = '/', intents = Intents.all())
@bot.event
async def on_ready(): print(f'Bot {bot.user} is running.')


def ternary(condition: bool, true_value: object, false_value: object = None) -> object:
    return true_value if condition else false_value


def is_animated(flag: str, url: bool) -> str:

    if url: return ternary(flag == 'a', 'gif', 'png')
    else: return ternary(flag == 'a', 'a')


@bot.command()
async def steal(ctx, *emojis: str):

    for emoji in emojis:
        matches = findall(r'<(a?):(.+):(\d+)>', emoji)

        for type, name, id in matches:
            url = f'https://cdn.discordapp.com/emojis/{id}.{is_animated(type, url = True)}'
            # message.append(f'<{is_animated(type, url = False)}:{name}:{id}>・{url}')
            await create(ctx, name, url)


@bot.command()
async def create(ctx, name: str, url: str):

    try: await ctx.message.delete()
    except: pass
    response = get(url)

    if response.status_code == 200:
        emoji = await ctx.guild.create_custom_emoji(name = name, image = response.content)
        await ctx.send(f'Emoji **{emoji.name.replace('_', '\\_')}** added to the server. {emoji}')
    else:
        await ctx.send('Failed to load image.')


bot.run(token)
from discord.ext import commands
from dotenv import load_dotenv
import emote_list

import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='$')
skynet_emotes = emote_list.EmoteList()


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user or message.content[0] == bot.command_prefix:
        await bot.process_commands(message)
        return None
    emote_ids = emote_list.parse_message(message.content)
    for emote_id in emote_ids:
        skynet_emotes.add(emote_id, message.author)
    print(emote_ids)
    return None


@bot.command(name='hello')
async def greeting(ctx):
    await ctx.send('Hello!')


@bot.command(name='getfreq')
async def get_frequency(ctx):
    totals = list(skynet_emotes.get_totals().items())
    print(totals)
    if len(totals) > 0:
        output = f"{totals[0][0]}\t:\t{totals[0][1]}"
        for i in range(1, len(totals)):
            output += f"\n{totals[i][0]}\t:\t{totals[i][1]}"
        await ctx.send(output)
    else:
        await ctx.send("No custom emotes have been used.")

# @bot.event
# async def on_error(event, *args, **kwargs):


bot.run(TOKEN)

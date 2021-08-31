from discord.ext import commands
from discord import Embed
from dotenv import load_dotenv
import os

import json
import jsonpickle

import emote_list

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='$')
bot.load_extension('cogs.queue')

emote_filename = 'emotes.json'
try:
    with open(emote_filename) as f:
        emoteList = jsonpickle.decode(f.read(), keys=True)
except FileNotFoundError:
    print("WARNING: No emote list found")
    emoteList = emote_list.EmoteList()

with open('pokemon.json', 'r') as f:
    pokemon_list = json.load(f)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("I can't do that for you.")
    elif isinstance(error, commands.errors.UserInputError):
        await ctx.send("You don't make any sense, check the command parameters.")


@bot.event
async def on_message(message):
    if message.author != bot.user and message.content[0] != bot.command_prefix:
        emote_ids = emote_list.parse_message(message.content)
        for emote_id in emote_ids:
            emoteList.add(emote_id, message.guild.id, message.author)
        print(emote_ids)
    else:
        await bot.process_commands(message)


@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')


@bot.command(name='getfreq', help="Returns amount each custom emote has been used in this server")
async def get_emote_frequency(ctx):
    totals = list(emoteList.get_totals()[ctx.guild.id].items())
    if len(totals) > 0:
        output = f"{totals[0][0]}\t:\t{totals[0][1]}"
        for i in range(1, len(totals)):
            output += f"\n{totals[i][0]}\t:\t{totals[i][1]}"
        msg = Embed(description=output)
        await ctx.send(embed=msg)
    else:
        await ctx.send("No custom emotes have been used.")


@bot.command(name="pokemon", help="Input a name or phrase to determine its related pokemon name")
async def get_pokemon_name(ctx, *, arg):
    total = 0
    for c in arg:
        if 97 <= ord(c) <= 122:  # if lowercase
            total += ord(c) - 96
        elif 65 <= ord(c) <= 90:  # if uppercase
            total += ord(c) - 64
    await ctx.send(pokemon_list[total] + " (id: "+str(total)+")")


@bot.command()
async def test(ctx, *, arg):
    await ctx.send(arg)


@bot.command(name='kill', help="Bot owner only; Kills bot functions")
@commands.is_owner()
async def leave(ctx):
    with open(emote_filename, 'w') as f_obj:
        f_obj.write(jsonpickle.encode(emoteList, keys=True))
    await ctx.send("See ya!")
    exit()


# @bot.event
# async def on_error(event, *args, **kwargs):

bot.run(TOKEN)

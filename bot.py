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

emote_filename = 'emotes.json'
try:
    with open(emote_filename) as f:
        emoteList = jsonpickle.decode(f.read(), keys=True)
except FileNotFoundError:
    print("WARNING: No emote list found")
    emoteList = emote_list.EmoteList()

with open('pokemon.json', 'r') as f:
    pokemon_list = json.load(f)

queueList = {}
voiceChannel = 737612005242044447


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
        emoteList.add(emote_id, message.guild.id, message.author)
    print(emote_ids)


@bot.event
async def on_reaction_add(reaction, r_user):
    if reaction.message.id in queueList:
        if reaction.count >= queueList[reaction.message.id]:
            invite = await reaction.message.guild.get_channel(voiceChannel).create_invite(max_age=300)
            async for user in reaction.users():
                if user != bot.user:
                    await user.send("Time to join! " + invite.url)
            await reaction.message.channel.send("Queue ended, join the voice channel.")
            await reaction.message.delete()
            del queueList[reaction.message.id]


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("God damn, you stupid.")


@bot.command(name='hello')
async def greeting(ctx):
    await ctx.send('Hello!')


@bot.command(name='getfreq')
async def get_frequency(ctx):
    totals = list(emoteList.get_totals()[ctx.guild.id].items())
    if len(totals) > 0:
        output = f"{totals[0][0]}\t:\t{totals[0][1]}"
        for i in range(1, len(totals)):
            output += f"\n{totals[i][0]}\t:\t{totals[i][1]}"
        msg = Embed(description=output)
        await ctx.send(embed=msg)
    else:
        await ctx.send("No custom emotes have been used.")


@bot.command(name='pokemon')
async def get_pokemon_name(ctx, *, arg):
    total = 0
    for c in arg:
        if 97 <= ord(c) <= 122:  # if lowercase
            total += ord(c) - 96
        elif 65 <= ord(c) <= 90:  # if uppercase
            total += ord(c) - 64
    await ctx.send(pokemon_list[total])


@bot.command(name='newqueue')
async def new_event_queue(ctx):
    msg = await ctx.send(embed=Embed(title="Queue started", description="Click the check mark to be notified when 2 "
                                                                        "people are ready!"))
    queueList[msg.id] = 2
    await msg.add_reaction("✅")


@bot.command(name='kill')
@commands.is_owner()
async def leave(ctx):
    with open(emote_filename, 'w') as f_obj:
        f_obj.write(jsonpickle.encode(emoteList, keys=True))
    await ctx.send("See ya!")
    exit()


# def exit_handler():
#     with open(emote_filename, 'w') as f_obj:
#         json.dump(skynet_emotes.get_totals(), f_obj)
#
#
# atexit.register(exit_handler)

# @bot.event
# async def on_error(event, *args, **kwargs):\

bot.run(TOKEN)

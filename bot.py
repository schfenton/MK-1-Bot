import asyncio

from discord.ext import commands
from discord import Embed
from discord import Color
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


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    try:
        if message.author != bot.user and message.content[0] != bot.command_prefix:
            emote_ids = emote_list.parse_message(message.content)
            for emote_id in emote_ids:
                emoteList.add(emote_id, message.guild.id, message.author)
            print(emote_ids)
        else:
            await bot.process_commands(message)
    except SystemExit:
        exit()


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


active_queues = set()


@bot.command(name='queue')
async def new_event_queue(ctx):
    msg = await ctx.send(embed=Embed(title="Queue started", description="Click the check mark to be notified when 2 "
                                                                        "people are ready!"))
    await msg.add_reaction("✅")
    msg = await ctx.fetch_message(msg.id)

    def reactionq_check(reaction, user):
        return reaction.message.channel == msg.channel and user != bot.user

    try:
        while msg.reactions[0].count < 2:
            await bot.wait_for('reaction_add', check=reactionq_check, timeout=900)  # use check to avoid constant timer
            msg = await ctx.fetch_message(msg.id)
        # Why can't I get the users after saving the reaction data? Who knows. Now we gotta flatten the damn thing.
        queued_users = await msg.reactions[0].users().flatten()
        await msg.delete()
        reply = await ctx.send("✅ Queue filled! Join the voice channel. ✅")
        for user in queued_users:
            if user != bot.user:
                await user.send(embed=Embed(title="Time to join "+ctx.guild.name+"!",
                                            description="[Click me to jump to the server]("+reply.jump_url+")",
                                            color=Color.green()))
    except asyncio.TimeoutError:
        await msg.delete()
        await ctx.send("❌ Queue timed out, not enough people. ❌")


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

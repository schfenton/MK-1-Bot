import asyncio
from discord.ext import commands
from discord import Embed
from discord import Color


class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def queue(self, ctx):
        msg = await ctx.send(
            embed=Embed(title="Queue started", description="Click the check mark to be notified when 2 "
                                                           "people are ready!"))
        await msg.add_reaction("✅")
        msg = await ctx.fetch_message(msg.id)

        def reaction_check(reaction, r_user):
            return reaction.message.channel == msg.channel and r_user != self.bot.user

        try:
            while msg.reactions[0].count < 2:
                await self.bot.wait_for('reaction_add', check=reaction_check,
                                        timeout=900)  # use check to avoid constant timer
                msg = await ctx.fetch_message(msg.id)
            # Why can't I get the users after saving the reaction data? Who knows. Now we gotta flatten the damn thing.
            queued_users = await msg.reactions[0].users().flatten()
            await msg.delete()
            reply = await ctx.send("✅ Queue filled! Join the voice channel. ✅")
            for user in queued_users:
                if user != self.bot.user:
                    await user.send(embed=Embed(title="Time to join " + ctx.guild.name + "!",
                                                description="[Click me to jump to the server](" + reply.jump_url + ")",
                                                color=Color.green()))
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send("❌ Queue timed out, not enough people. ❌")


def setup(bot):
    bot.add_cog(Queue(bot))

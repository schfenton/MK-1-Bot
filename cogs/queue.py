import asyncio
from discord.ext import commands
from discord import Embed
from discord import Color


class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='getqueue', aliases=['queue'], help="Retrieve channel queue, if active")
    async def get_queue(self, ctx):
        await ctx.send("...")  # add implementation

    @commands.command(name='newqueue', help="Create new queue, if one does not exist")
    async def new_queue(self, ctx, user_limit: int):
        if user_limit < 2:
            await ctx.send("Cannot create queue with a user limit less than two.")
        else:
            msg = await ctx.send(
                embed=Embed(title="Queue started",
                            description="Click the check mark to be notified when " + str(user_limit) + " users are " +
                                                                                                        "ready!"))
            await msg.add_reaction("✅")
            msg = await ctx.fetch_message(msg.id)

            def reaction_check(reaction, r_user):
                return reaction.message.id == msg.id and r_user != self.bot.user

            try:
                while msg.reactions[0].count < user_limit:
                    # use check to avoid timeout refresh on any reaction
                    await self.bot.wait_for('reaction_add', check=reaction_check, timeout=900)
                    msg = await ctx.fetch_message(msg.id)
                # Why can't I get the users after saving the reaction data? Who knows. Now we gotta flatten the mfer.
                queued_users = await msg.reactions[0].users().flatten()
                await msg.delete()
                reply = await ctx.send("✅ Queue filled! Join the voice channel. ✅")
                for user in queued_users:
                    if user != self.bot.user:
                        await user.send(embed=Embed(title="Time to join " + ctx.guild.name + "!",
                                                    description="[Click me to jump to the server]("+reply.jump_url+")",
                                                    color=Color.green()))
            except asyncio.TimeoutError:
                await msg.delete()
                await ctx.send("❌ Queue timed out, not enough people. ❌")


def setup(bot):
    bot.add_cog(Queue(bot))

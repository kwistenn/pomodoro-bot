from discord.ext import commands

print("Handler initialized.")


class Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        user = message.author
        msg = message.content

        print(f"{user} said {msg}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found.")

        raise error


def setup(bot):
    bot.add_cog(Handler(bot))

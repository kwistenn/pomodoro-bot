import asyncio
from discord.ext import commands
import json

print("Pom! initialized.")


class Pom(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.save_users())
        with open('users.json', 'r') as f:
            self.users = json.load(f)

    async def save_users(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open('users.json', 'w') as f:
                json.dump(self.users, f, indent=4)

            await asyncio.sleep(3)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        author_id = str(message.author.id)

        if author_id not in self.users:
            self.users[author_id] = {}
            self.users[author_id]["pom"] = 0

    @commands.command()
    async def pom(self, ctx, num: int):
        author_id = str(ctx.author.id)
        author = str(ctx.message.author.id)
        with open('users.json', 'r') as f:
            self.users = json.load(f)
        self.users[author_id]['pom'] += num
        await ctx.send(str(num) + " poms have been added! <@" + author +
                       "> now have " + str(self.users[author_id]['pom']) +
                       " poms! :tomato:")

    @pom.error
    async def pom_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Specify the amount of poms you want to add :tomato:")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Use a number!")

        raise error

    @commands.command()
    @commands.has_role('Admins')
    async def reset_all(self, ctx):
        with open('users.json', 'r') as f:
            self.users = json.load(f)
        for usr in self.users:
            self.users[usr]['pom'] = 0
        await ctx.send("All poms have been reset! :tomato:")

    @reset_all.error
    async def reset_all_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have the permission to do that!")

        raise error


def setup(bot):
    bot.add_cog(Pom(bot))

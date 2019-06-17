import discord
import json
from discord.ext import commands

print("Leaderboard initialized.")


class Leaderboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leaderboard(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.red()
        )
        with open('users.json', 'r+') as f:
            users = json.load(f)

        d = sorted(users, key=lambda x: users[x].get('pom', 0), reverse=True)
        message = ''
        for number, user in enumerate(d):
            message += '`{0}`. **<@{1}>** with {2} poms!\n'.format(number + 1, user, users[user].get('pom', 0))
        print(message)
        embed.set_author(name="Leaderboard")
        embed.add_field(name="Pom! Leaderboard :tomato:", value=message)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Leaderboard(bot))

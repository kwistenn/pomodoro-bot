import discord
from discord.ext import commands
import os
import json


def clear():
    with open('users.json', 'r+') as f:
        data = json.load(f)
        for author_id in data:
            data[author_id]["pom"] = 0
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

# Read Token


def read_token():
    with open("token.txt", "r") as a:
        text = a.readlines()
        return text[0].strip()


token = read_token()

# Bot Function

client = commands.Bot(command_prefix='!')
client.remove_command('help')

# Ready
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Studying hard!"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


# Cogs
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')  # Load cogs
    await ctx.send("Extension " + str(extension) + " has been loaded.")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')  # Unload cogs
    await ctx.send("Extension " + str(extension) + " has been unloaded.")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')  # Load all cogs


# Ping
@client.command()
async def ping(msg):
    latency = client.latency
    await msg.send("Pong!" + '`' + str(latency * 1000) + " ms`")

# Purge
@client.command()
async def purge(ctx, amount: int):
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"Deleted {len(deleted)} messages!")

# bada boom
@client.command()
async def boom(msg):
    await msg.send("big boom")

# Help
@client.command(pass_context=True)
async def help(msg):

    embed = discord.Embed(
        colour=discord.Colour.red()
    )

    embed.set_author(name="Pom! Help")
    embed.add_field(name="!help", value="Display this help menu :tomato:", inline=False)
    embed.add_field(name="!pom {amount of pomodoro}", value="Add completed pomodoro sessions :tomato:", inline=False)
    embed.add_field(
        name="s {number of session} {length} {break time}",
        value="Create a pomodoro session. 25 minutes = 1 pom :tomato:", inline=False)
    embed.add_field(name="!author", value="Display the creator of Pom! hint: it's! :tomato:", inline=False)

    await msg.author.send(embed=embed)
    await msg.send("Message sent to your DMs! :tomato:")


# Author
@client.command()
async def author(msg):
    embed = discord.Embed(
        colour=discord.Colour.green()
    )

    embed.set_author(name="Pom! Creator")
    embed.add_field(name="",
                    value="Polymath. I mostly do Art, Music, Writing, "
                          "Coding and many other interests.⁣ My Social Media:")
    embed.set_thumbnail(
        url="https://images.curiator.com/images/t_x/art/u14gmpwplrcfpkghekmo/kuvshinov-ilya-untitled.jpg")

    await msg.send("Pom! is created by ! :tomato:")
    await msg.send(embed=embed)


client.run(token)

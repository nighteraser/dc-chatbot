TOKEN = ''

import os, asyncio, discord
from discord.ext import commands

command_prefix = '$'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = command_prefix, intents = intents)

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f"login ID --> {bot.user}")
    print(f"load {len(slash)} slash commands")

# load commands
@bot.command()
async def load(ctx: commands.Context, extension: str):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")

# unload commands
@bot.command()
async def unload(ctx: commands.Context, extension: str):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")

# reload commands
@bot.command()
async def reload(ctx: commands.Context, extension: str):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")

# load all cogs
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
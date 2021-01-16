import discord   
import random
from discord.ext import commands

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Bot is ready.')


@client.command(aliases=['leet'])
async def _leet(ctx):
    responses = ["yoyo",
                 "bruh"]

    await ctx.send(f' Ans: {random.choice(responses)}')


client.run('ODAwMDY3MTg1Mjc1NTY4MTQ5.YAMuoQ.Lkq2Std3DvJDT0vjT00BMEuyklI')
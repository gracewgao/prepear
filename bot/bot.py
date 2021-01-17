import os
import discord
import asyncio
import configparser
import discord
from discord.ext import commands
import json
import random

from .database import *

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Logged in as: {0} - {1}'.format(client.user.name, client.user.id))
    print('-'*20)


@client.command(aliases=['leetcode'])
async def _leetcode(ctx, difficulty):
    message = get_question(difficulty)
    await ctx.send(message)

    channel2 = await member.guild.create_voice_channel(name,category=category)
    channelID = channel2.id
    await member.move_to(channel2)
    await channel2.set_permissions(self.bot.user, connect=True,read_messages=True)
    await channel2.edit(name= name, user_limit = limit)

# @client.event
# async def on_message(message):
#     """
#     members = []
#     if message.content.startswith('!member'):
#         for guild in client.guilds:
#             for member in guild.members:
#                 members.append(member)
#     print(members)
#     """
#     if message.content.startswith('!leet'):
#         userID = message.author
#         await message.author.send('Welcome!' + userID)


# sets up the bot
class DiscordBot(object):
    def __init__(self):
        self.token = None
        self.config = configparser.ConfigParser()

    def create_config(self):
        self.token = input('Bot Token:')
        self.config.add_section('DiscordBot')
        self.config.set('DiscordBot', 'token', self.token)
        with open('{0}\{1}'.format(os.getcwd(), 'config.ini'), 'w') as configfile:
            self.config.write(configfile)

    def get_token(self):
        self.config.read('{0}\{1}'.format(os.getcwd(), 'config.ini'))
        self.token = self.config.get('DiscordBot', 'token')

    def set_token(self, token):
        self.config.read('{0}\{1}'.format(os.getcwd(), 'config.ini'))
        self.config.set('DiscordBot', 'token', token)
        with open('{0}\{1}'.format(os.getcwd(), 'config.ini'), 'w') as configfile:
            self.config.write(configfile)

    def run(self):
        client.run(self.token)
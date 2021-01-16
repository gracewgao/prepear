import os
import discord
import asyncio
import configparser
import discord
from discord.ext import commands
import json
import random


client = commands.Bot(command_prefix = '!')


@client.event
async def on_ready():
    print('Logged in as: {0} - {1}'.format(client.user.name, client.user.id))
    print('-'*20)
"""
@client.command(aliases=['leet'])
async def _leet(ctx):
    responses = ["yoyo",
                 "bruh"]

    await ctx.send(f' Ans: {random.choice(responses)}')
"""
@client.command(aliases=['leetcode'])
async def _leetcode(ctx, difficulty):
    with open("bot/leetcode.json") as f:
        questions = json.load(f)
        rand = random.randint(0, len(questions[difficulty]) - 1)
        name = questions[difficulty][rand]
        leetcode_url = 'https://leetcode.com/problems/' + name + '/'

        count = 0
        code_url = 'https://codeshare.io/prepear-' + name + '-' + str(count)
        # todo: save count into database
        count += 1

    await ctx.send(f'Try this one!\n{leetcode_url}\nYou can get started here:\n{code_url}')

@client.event
async def on_message(message):
    """
    members = []
    if message.content.startswith('!member'):
        for guild in client.guilds:
            for member in guild.members:
                members.append(member)
    print(members)
    """
    if message.content.startswith('!leet'):
        await message.author.send('Welcome! {client.user.name}#{client.user.id}👋')


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

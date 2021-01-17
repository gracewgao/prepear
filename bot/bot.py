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

    
@client.command()
async def createvc(ctx, channelName):
    guild = ctx.guild
    mbed = discord.Embed(
        title = 'Success!',
        description = f'{channelName} has sucessfully been created!'
    )
    if ctx.author.guild_permissions.manage_channels:
        await guild.create_voice_channel(name=channelName)
        await ctx.send(embed=mbed)

        
@client.command()
async def deletevc(ctx,vc: discord.VoiceChannel):
    mbed = discord.Embed(
        title = 'Success!',
        description = f'{vc} has sucessfully been deleted!'
    )
    if ctx.author.guild_permissions.manage_channels:
        await ctx.send(embed=mbed)
        await vc.delete()

        
@client.event
async def on_raw_reaction_add(payload):

    add_user(payload.user_id)

    message_id = payload.message_id
    if message_id == 800124907920293939:
        guild_id = payload.guild_id
        guild = client.get_guild(payload.guild_id)

        add_language(payload.user_id, payload.emoji.name)

        if payload.emoji.name == 'cpp':
            role = discord.utils.get(guild.roles, name='C++')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = payload.member
            if member is not None:
                await member.add_roles(role)
                print("done")
            else:
                print("Member not found.")
        else:
            print("Role not found.")

    
@client.command(aliases=['leetcode'])
async def _leetcode(ctx, difficulty):
    message = check_pear(difficulty)
    await ctx.send(message)


@client.event
async def on_message(message):
    add_user(message.author)


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
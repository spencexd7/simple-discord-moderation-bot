# author : https://github.com/spencexd7


import discord

import os

from discord.ext import commands 

import datetime

import json

### config

token= os.environ["token"]

prefix = "."

bot_activity = "with spencexd7#0746"

non_prefix = [887973552958087168, 1111149745000423455]

t = "<:stolen_emoji:1117053998319534120>"#tick emoji 

c = "<:stolen_emoji:1117054122772942848>"#cross emoji

def get_prefix(client, message):

  if message.author.id in non_prefix:

     return ""

  else:

    return prefix

client = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all(), allowed_mentions=discord.AllowedMentions(

                                   everyone=False, replied_user=False), case_insensitive=True)

client.remove_command("help")

@client.event 

async def on_ready():

  print(client.user)

  await client.change_presence(activity=discord.Streaming(name=bot_activity, url="https://twitch.tv/spencexd7"))

@client.event

async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):

      return

    else:

      await ctx.reply(f"{c} Error : " + str(error))

      

@client.command()

async def ping(ctx):

    if ctx.author.bot:

        return

    await ctx.reply(f'{t} Pong! {client.latency*1000:.2f}ms.')

@client.command()

@commands.has_permissions(kick_members=True)

async def kick(ctx, member: discord.Member, *, reason=None):

    await member.kick(reason=reason)

    await ctx.reply(f'{t} {member} has been kicked from the server.')

@client.command()

@commands.has_permissions(ban_members=True)

async def ban(ctx, member: discord.Member, *, reason=None):

    await member.ban(reason=reason)

    await ctx.reply(f'{t} {member} has been banned from the server.')

@client.command()

@commands.has_permissions(manage_messages=True)

async def mute(ctx, member:discord.Member, minutes:int=60):

      duration = datetime.timedelta(minutes=minutes)

      await member.timeout(duration)

      await ctx.reply(f"{t} {member} has been muted for {minutes}mins.")

@client.command()

@commands.has_permissions(manage_messages=True)

async def unmute(ctx, member:discord.Member):

      duration = datetime.timedelta(minutes=0)

      await member.timeout(duration)

      await ctx.reply(f"{t} {member} has been unmuted.")

@client.command(aliases=["ar"])

@commands.has_permissions(manage_roles=True)

async def addrole(ctx, member: discord.Member, role: discord.Role):

    if member.id == ctx.author.id:

      await ctx.reply(f"{c} You can't add role to yourself.")

      return 

    await member.add_roles(role)

    await ctx.reply(f"{t} {role.name} role has been added to {member}.")

@client.command()

@commands.has_permissions(manage_roles=True)

async def removerole(ctx, member: discord.Member, role: discord.Role):

    await member.remove_roles(role)

    await ctx.reply(f"{t} {role.name} role has been removed from {member}.")

@client.command()

@commands.has_permissions(manage_channels=True)

async def lock(ctx):

    overwrites = ctx.channel.overwrites_for(ctx.guild.default_role)

    overwrites.send_messages=False

    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)

    await ctx.reply(f"{t} {ctx.channel.mention} has been locked.")

@client.command()

@commands.has_permissions(manage_channels=True)

async def unlock(ctx):

    overwrites = ctx.channel.overwrites_for(ctx.guild.default_role)

    overwrites.send_messages=None

    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)

    await ctx.reply(f"{t} {ctx.channel.mention} has been unlocked.")

with open('warnings.json', 'r') as f:

    warnings = json.load(f)

def save_warnings():

    with open('warnings.json', 'w') as f:

        json.dump(warnings, f)

@client.command()

@commands.has_permissions(manage_messages=True)

async def warn(ctx, member: discord.Member, *, reason:str="No reason provided."):

    if member.id not in warnings:

        warnings[str(member.id)] = []

    warnings[str(member.id)].append(reason)

    save_warnings()

    await ctx.reply(f"{t} {member} has been warned.")

@client.command()

@commands.has_permissions(manage_messages=True)

async def warns(ctx, member: discord.Member = None):

    if member is None:

        member = ctx.author

    if str(member.id) in warnings: 

        await ctx.reply(f"{t} {member} has {len(warnings[str(member.id)])} warnings.")

    else:

        await ctx.reply(f"{c} {member.display_name} has no warnings.")

  

@client.command(aliases=["h"])

async def help(ctx):

  em = discord.Embed(color=discord.Color.blurple())

  em.set_author(name=ctx.guild.name, icon_url=client.user.avatar)

  em.set_footer(text="Coded by spencexd7#0746", icon_url=client.user.avatar)

  em.add_field(name="Moderation Commands: ", value ="```mute, removerole, unlock, unmute, warns, lock, warn, addrole, kick, test, ban```", inline=False)

  em.add_field(name="General Commands: ", value ="```ping, help```", inline=False)

  await ctx.reply(embed=em)

client.run(token)

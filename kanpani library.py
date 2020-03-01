import discord
from discord.ext import commands
import json
import os

bot = commands.Bot(command_prefix = '!!')

with open('setting.json', mode = 'r', encoding = 'utf8') as setting_file:
    setting_data = json.load(setting_file)

@bot.event
async def on_ready(): ##online notification
    print ('お兄ちゃん、お帰り～.')
    channel = bot.get_channel(672402403806543882)
    await channel.send('お兄ちゃん、お帰り～.')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'``{extension}`` loaded.')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'``{extension}`` unloaded.')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'``{extension}`` reloaded.')

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 680826994325323802:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        print(payload.emoji.name)
        if payload.emoji.name == 'FISH':
            role = discord.utils.get(guild.roles, name = '功德社長')
        elif payload.emoji.name == 'ill':
            role = discord.utils.get(guild.roles, name = '技術專員')
        elif payload.emoji.name == 'aquawail':
            role = discord.utils.get(guild.roles, name = '和真')
        else:
            print('Role not found')
        if role != None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member != None:
                await member.add_roles(role)
                print(f'Add {member} to role {role} successful.')
            else:
                print('Member not found')
    else:
        print('Message not found')

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')


if __name__ == "__main__":
    bot.run(setting_data['token'])
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


for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')


if __name__ == "__main__":
    bot.run(setting_data['token'])
import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('setting.json', mode = 'r', encoding = 'utf8') as setting_file:
    setting_data = json.load(setting_file)


class Main(Cog_Extension):
    @commands.command() ##ping check
    async def ping(self, ctx): ##ctx = contex
        await ctx.send(f'{round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def mywife(self, ctx):
        pic = setting_data['pic']
        await ctx.send(pic)

def setup(bot):
    bot.add_cog(Main(bot))
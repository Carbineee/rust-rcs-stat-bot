import random
import discord
import urllib
import secrets
import asyncio
import aiohttp
import re
import requests
import random
import json

from io import BytesIO
from discord.ext import commands
from utils import lists, permissions, http, default, argparser


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.command()
    async def stats(self, ctx, steamId):
        """Displays rust stats based on the users steamID, if the profile is private nothing will be returned"""
        if(len(steamId) != 17):
            await ctx.send('SteamID seems to be invalid, please try again!')
            return

        stats = dict()
        file_name = random.randint(1000,9999)

        profile = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=A70902E029FC4EB4B0AD229444F30B22&steamids=" + steamId)
        player = requests.get("http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=252490&key=A70902E029FC4EB4B0AD229444F30B22&steamid=" + steamId)
        if(player.status_code == 500):
            await ctx.send("Steam Profile is private, please make it public and try again!")
            return
        profileJson = profile.json()
        playerData = player.json()

        for profile in profileJson.values():
            for player in profile.values():
                profile_name = player[0]['personaname']
                profile_avatar = player[0]['avatar']

        playerStats = playerData['playerstats']
        print(profile_avatar)

        #Convert the stats into a dictionary
        for stat in playerStats['stats']:
            stats[stat['name']] = stat['value']

        #Add custom statistics to the dictionary that don't exist by default
        stats['death_player'] = (stats['deaths'] - stats['death_suicide'] - stats['death_fall']- stats['death_bear'] - stats['death_entity'])
        stats['kd'] = round((stats['kill_player'] / stats['death_player']), 2)
        stats['headshot_percent'] = round((stats['headshot'] / stats['bullet_hit_player'] * 100), 2)

        embed=discord.Embed(title='Rust Stats For: ' + profile_name, color=0xFF5733)
        embed.add_field(name="Player Kills", value=stats['kill_player'])
        embed.add_field(name="Player Deaths", value=stats['death_player'])
        embed.add_field(name="KD Ratio", value=stats['kd'])
        embed.add_field(name="Player Hits", value=stats['bullet_hit_player'])
        embed.add_field(name="Headshots", value=stats['headshot'])
        embed.add_field(name="Headshot Percent", value=str(stats['headshot_percent']) + "%")
        embed.set_thumbnail(url=profile_avatar)

        embed.set_footer(text="Rust Stats are gathered using the Steam API, Bot By @Carbine#6969")


        print('Requesting Stats: http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=252490&key=A70902E029FC4EB4B0AD229444F30B22&steamid=' + steamId)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Stats(bot))

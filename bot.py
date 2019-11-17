# The Cave 2019 ^(C)
import discord
import json
import asyncio
import logging
import dbl

from discord.ext import commands

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
TOKEN = open("token.txt", "r").read()

client.remove_command('help')

@client.event
async def on_ready():
    client.loop.create_task(status_task())
    print('The Cave is online!')

@client.event
async def status_task():
    while True:
        await client.change_presence(status = discord.Status.online, activity=discord.Game('tc/help for commands.'))
        await asyncio.sleep(10)
        await client.change_presence(status= discord.Status.online, activity=discord.Game("Reinvite the bot if commands don't work."))
        await asyncio.sleep(10)

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server with The Cave in it.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server with The Cave in it.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Missing Requirement Error [TC10]", description="Pass in all required arguments.", colour=discord.Color.blue())

        await ctx.send(embed=embed)

    
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="Missing Permissions Error [TC11]", description="You are not able to use this command because you do not have the required permissions.", colour=discord.Color.blue())

        await ctx.send(embed=embed)

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = 'tc/'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms :ping_pong:')
    embed = discord.Embed(title="Pong!", description=":ping_pong:", colour=discord.Color.blue())

    embed.add_field(name="The latency for The Cave is...", value=f"{round(client.latency * 1000)} ms")
    

    await ctx.send(embed=embed)



@client.command(aliases=['p', 'c', 'purge'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Cleared {amount} messages.')

@client.command(aliases=['sp', 'sc', 'softpurge'])
@commands.has_permissions(manage_messages=True)
async def softclear(ctx,amount=2):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Cleared {amount} messages.')

@client.command(aliases=['k'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member}\nReason - {reason}')

@client.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member}\nReason - {reason}')

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
            return

@client.command()
async def bump(ctx):
    await ctx.send('Bump The Cave on:\nDiscordBots.org - <https://discordbots.org/bot/624829444963696660>\nDiscordBotList.com - <https://discordbotlist.com/bots/624829444963696660/upvote>')

@client.command(aliases=['developer', 'devteam'])
async def dev(ctx):
    await ctx.send('<@308000668181069824> developed me!')

@client.command(aliases=['prefix'])
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    embed = discord.Embed(title="Prefix Changed", description="The prefix has been changed by an Admin.", colour=discord.Color.blue())

    embed.add_field(name="The prefix for this server has been changed by an Admin to", value=f"{prefix}")

    await ctx.send(embed=embed)

@client.command()
async def invite(ctx):
    embed = discord.Embed(title="Invite", description="Invite The Cave to your server!", colour=discord.Color.blue(), url="https://discordapp.com/oauth2/authorize?client_id=624829444963696660&scope=bot&permissions=0")

    embed.add_field(name="Click here to invite The Cave to your Discord Server.", value="https://discordapp.com/oauth2/authorize?client_id=624829444963696660&scope=bot&permissions=0")

    await ctx.send(embed=embed)

@client.command(hidden=True)
async def baf(ctx):
    await ctx.send('https://i.gyazo.com/04d0cbc179d87db2234286dfb29c77b7.png')

@client.command(hidden=True)
async def L(ctx):
    await ctx.send('https://images-ext-1.discordapp.net/external/A3mHladESs0DR-qbDmStWES1E9nNUNVmnxX0RiLqiHE/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/184493854467162112/d90d39fe114c3ea0e5eb911f6c1bbc25.webp')

@client.command(aliases=['vc', 'screenshare', 'ss'])
async def vcshare(ctx):
    embed = discord.Embed(title="Screenshare", description="Cilck this link to screenshare", colour=discord.Color.blue(), url=f"https://discordapp.com/channels/{ctx.guild.id}/{ctx.author.voice.channel.id}")

    embed.add_field(name="Screenshare here", value=f"https://discordapp.com/channels/{ctx.guild.id}/{ctx.author.voice.channel.id}")

    await ctx.send(embed=embed)

@client.command()
async def support(ctx):
    embed = discord.Embed(title="Need Support?", description="The Discord Support Server and the dev's contact.", colour=discord.Color.blue(), url="https://discord.gg/8xMWb7W")

    embed.add_field(name="Contact the Dev", value="<@308000668181069824>")
    embed.add_field(name="Join the Discord", value="https://discord.gg/8xMWb7W")

    await ctx.send(embed=embed)

@client.command(hidden=True, aliases=['ce3', 'retard', 'poggers'])
async def clearesteagle3(ctx):
    await ctx.send('ClearestEagle3 be like, im retard')

@client.command(hidden=True, aliases=['boost'])
async def nitroboost(ctx):
    await ctx.send('Boosting gives you guys:\n- Special Pink Role\n- More emojis for the entire server\n- Higher bitrate for the entire server\n- Special access to higher level channels\n- Special access to a secret category with only the boosters [The Booster Club]\n- Choose any of the role colors\n- Embed Access :globe_with_meridians: \n- File Upload Access :file_folder: \n- Special Madge on the Member List\n - And More!!!\nSo you should join the Booster Club, by boosting our server. You help out the entire server and you get some awesome perks!\n https://tenor.com/view/discord-nitro-server-boost-boost-nitro-boost-gif-14289229')

@client.command(hidden=True, aliases=['hk', 'freehonkkong', 'freehk'])
async def hongkong(ctx):
    await ctx.send(':flag_hk: free hong kong https://www.reddit.com/r/HongKong/comments/dpn9oy/man_gets_pepper_sprayed_in_the_face_for_asking_a/')

@client.command()
async def embedtemplate(ctx):
    embed = discord.Embed(title="Title", description="Description", colour=discord.Color.blue(), url="https://mmatt.pw")

    embed.add_field(name="the title", value="the description")

    await ctx.send(embed=embed)




@client.command(hidden=True)
async def fortnite(ctx):
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')
    await ctx.send('fortnite')

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Command Help", description="All of The Cave's commands.", colour=discord.Color.blue())

    embed.add_field(name="Ban", value="Usage - tc/ban [@username] [reason]. Requires the Ban Member Permission. Bans the member specified, permanently. For more information, do tc/help ban.")
    embed.add_field(name="Join the Discord", value="https://discord.gg/8xMWb7W")

    await ctx.send(embed=embed)


#Role reaction for booster club
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 625430288658333729:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'yellow':
            role = discord.utils.get(guild.roles, name='yellow')
        elif payload.emoji.name == 'red':
            role = discord.utils.get(guild.roles, name='red')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print("Done")
            else:
                print('Member not found')
        else:
            print('Role not found')

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 625430288658333729:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'yellow':
            role = discord.utils.get(guild.roles, name='yellow')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print("Done")
            else:
                print('Member not found')
        else:
            print('Role not found')

#Role select for the general public
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 645399829039808514:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'twitchnotifications':
            role = discord.utils.get(guild.roles, name='twitchnotifications')
        elif payload.emoji.name == 'red':
            role = discord.utils.get(guild.roles, name='red')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print("Done")
            else:
                print('Member not found')
        else:
            print('Role not found')

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 645399829039808514:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'twitchnotifications':
            role = discord.utils.get(guild.roles, name='twitchnotifications')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print("Done")
            else:
                print('Member not found')
        else:
            print('Role not found')

#Top.gg vote sys
class DiscordBotsOrgAPI(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyNDgyOTQ0NDk2MzY5NjY2MCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTY5NDUwNzQzfQ.znNOAGSkl0dyExGwQpBXXle3bV7LO3w53-bNMoFnPZA' # set this to your DBL token
        self.dblpy = dbl.Client(self.bot, self.token)
        self.updating = self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""
        while not self.bot.is_closed():
            logger.info('Attempting to post server count')
            try:
                await self.dblpy.post_guild_count()
                logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))
            except Exception as e:
                logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)

def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(DiscordBotsOrgAPI(bot))

client.run('TOKEN')

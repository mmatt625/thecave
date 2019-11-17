# The Cave 2019 ^(C)
import discord
import json
import asyncio
import logging

from discord.ext import commands

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('tc/prefix - tc/help'))
    print('The Cave is online!')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server with The Cave in it.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server with The Cave in it.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing Requirement Error [TC10]\nPass in all required arguments.')\
    
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Missing Permissions Error [TC11]\nYou are not able to use this command because you do not have the required permissions.')

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

    await ctx.send(f'The prefix has changed to {prefix}')

@client.command()
async def invite(ctx):
    await ctx.send('You can invite The Cave to your server by going to\nhttps://discordapp.com/oauth2/authorize?client_id=624829444963696660&scope=bot&permissions=0')
    embed = discord.Embed(title="Invite", description="Invite The Cave to your server!", colour=discord.Color.blurple(), url="https://discordapp.com/oauth2/authorize?client_id=624829444963696660&scope=bot&permissions=0")

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
    embed = discord.Embed(title="Screenshare", description="Cilck this link to screenshare", colour=discord.Color.blurple(), url=f"https://discordapp.com/channels/{ctx.guild.id}/{ctx.author.voice.channel.id}")

    embed.add_field(name="Screenshare here", value=f"https://discordapp.com/channels/{ctx.guild.id}/{ctx.author.voice.channel.id}")

    await ctx.send(embed=embed)

@client.command()
async def support(ctx):
    embed = discord.Embed(title="Support", description="Discord Support Server", colour=discord.Color.blurple(), url="https://discord.gg/8xMWb7W")

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
    embed = discord.Embed(title="Title", description="Description", colour=discord.Color.blurple(), url="https://mmatt.pw")

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

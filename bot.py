# The Cave 2019 ^(C)
import discord
import json
import asyncio
import logging
import dbl

from discord.ext import commands


client = commands.Bot(command_prefix = 'tc/')

client.remove_command("help")


@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity=discord.Game('tc/help for commands.'))
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
    embed = discord.Embed(title="Pong!", description=":ping_pong:", colour=discord.Color.blue())

    embed.add_field(name="The latency for The Cave is...", value=f"{round(client.latency * 1000)} ms")
    

    await ctx.send(embed=embed)



@client.command(aliases=['p', 'c', 'purge'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    embed = discord.Embed(title="Cleared Messages", description="Purge has been executed.", colour=discord.Color.blue())

    embed.add_field(name="Cleared", value=f"{amount} messages")

    await ctx.channel.purge(limit=amount)

    await ctx.send(embed=embed)


@client.command(aliases=['sp', 'sc', 'softpurge'])
@commands.has_permissions(manage_messages=True)
async def softclear(ctx,amount=2):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title="Cleared Messages", description="Soft purge has been executed.", colour=discord.Color.blue())

    embed.add_field(name="Cleared", value=f"{amount} messages")

    await ctx.send(embed=embed)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, user : discord.Member, *, reason=None):
    await user.kick(reason=reason)
    embed = discord.Embed(title="User Kicked", description=f"{user.name} has been kicked from the server.", colour=discord.Color.blue())

    embed.add_field(name="User", value=f"@{user.name}#{user.discriminator}")
    embed.add_field(name="Reason", value=f"{reason}")

    await ctx.send(embed=embed)

@client.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, user : discord.Member, *, reason=None):
    await user.ban(reason=reason)
    embed = discord.Embed(title="User Banned", description=f"{user.name} has been banned from the server.", colour=discord.Color.blue())

    embed.add_field(name="User", value=f"@{user.name}#{user.discriminator}")
    embed.add_field(name="Reason", value=f"{reason}")

    await ctx.send(embed=embed)



@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed = discord.Embed(title="User Unbanned", description=f"{user.name} has been unbanned from the server.", colour=discord.Color.blue())

            embed.add_field(name="User", value=f"@{user.name}#{user.discriminator}")

            await ctx.send(embed=embed)


            return

@client.command()
async def vote(ctx):
    embed = discord.Embed(title="Vote", description="Vote on The Cave bot on...", colour=discord.Color.blue())

    embed.add_field(name="DiscordBots.org", value="https://discordbots.org/bot/624829444963696660")
    embed.add_field(name="DiscordBotList.com", value="https://discordbotlist.com/bots/624829444963696660/upvote")

    await ctx.send(embed=embed)


@client.command(aliases=['developer', 'devteam'])
async def dev(ctx):
    embed = discord.Embed(title="mmatt developed me!", colour=discord.Color.blue())

    embed.add_field(name="Dev's Discord", value="<@308000668181069824>")

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
    embed = discord.Embed(title="ClearestEagle3 be like", colour=discord.Color.blue())

    embed.add_field(name="Be like", value="retard")

    await ctx.send(embed=embed)

@client.command(hidden=True, aliases=['boost'])
async def nitroboost(ctx):
    embed = discord.Embed(title="Nitro Boosting", description="Using your Nitro Boost on a server gives the server...", colour=discord.Color.blue())

    embed.add_field(name="Pink Role", value="Special Pink Role only given to Nitro Boosters, that can be given special permissions.")
    embed.add_field(name="More Emojis", value="More emojis for the entire server to use. (up to a total of 250 emojis!)")
    embed.add_field(name="Higher Bitrate", value="Higher quality voice channels for the entire server.")
    embed.add_field(name="Special Badge", value="You get a special badge on your Discord profile as well as on the member list.")
    embed.add_field(name="The rest is up to the server.", value="The server can give you secret channels and more perks. For example, The Cave gives boosters more role colors, file upload access, file embed access, and more.")
    embed.set_thumbnail(url="https://tenor.com/view/discord-nitro-server-boost-boost-nitro-boost-gif-14289229")

    await ctx.send(embed=embed)


@client.command(hidden=True, aliases=['hk', 'freehonkkong', 'freehk'])
async def hongkong(ctx):
    await ctx.send(':flag_hk: free hong kong https://www.reddit.com/r/HongKong/comments/dpn9oy/man_gets_pepper_sprayed_in_the_face_for_asking_a/')

@client.command(hidden=True)
async def embedbuilder(ctx):
    embed = discord.Embed(title="Title", description="Description", colour=discord.Color.blue(), url="https://mmatt.pw")

    embed.add_field(name="the title", value="the description")

    await ctx.send(embed=embed)


@client.command(aliases=['helpme', 'help'])
async def commands(ctx):
    embed = discord.Embed(title="Command Help", description="All of The Cave's commands.", colour=discord.Color.blue())

    embed.add_field(name="Ban", value="Usage - tc/ban [or tc/b] [@username] [reason]. Bans the member specified, permanently. Requires the Ban Member Permission.")
    embed.add_field(name="ChangePrefix", value="[UNDER CONSTRUCTION] Usage - tc/prefix [or tc/changeprefix] [prefix]. Changes the prefix for this server. Requires the Administrator Permission.")
    embed.add_field(name="Clear", value="Usage - tc/clear [or tc/p,c, or purge] [amount]. Clears amount of messages specified. [Make sure you add 1 to your ammount.] [Default amount = 5] Requires the Manage Messages Permission.")
    embed.add_field(name="Dev", value="Usage - tc/dev [or tc/developer, or devteam]. Shows the development team of The Cave bot.")
    embed.add_field(name="Help", value="Usage - tc/help [or tc/commands]. Shows this message")
    embed.add_field(name="Invite", value="Usage - tc/invite Gives an invite link to the bot.")
    embed.add_field(name="Kick", value="Usage - tc/kick [or tc/k] [member] [reason]. Kicks the member specified. Requires the Kick Members Permission.")
    embed.add_field(name="Ping", value="Usage - tc/ping. Shows the bot's latency between the Discord servers.")
    embed.add_field(name="SoftClear", value="Usage - tc/softclear [or tc/sp, sc, or softpurge] Same thing as tc/clear, except the default value is 2.")
    embed.add_field(name="Support", value="Usage - tc/support. Gives support server + dev's username.")
    embed.add_field(name="Unban", value="Usage - tc/unban [Username]. Unbans a specific user. Requires Ban Members Permission")
    embed.add_field(name="VCShare", value="Usage - tc/vcshare. Gives link to screenshare in a voice channel. Must be in a voice channel to work. [FAN FAVORITE]")
    embed.add_field(name="Join the Support Discord", value="https://discord.gg/8xMWb7W")

    await ctx.send(embed=embed)


@client.command(hidden=True)
async def xander(ctx):
    embed = discord.Embed(title="xander be like", colour=discord.Color.green())

    embed.add_field(name="Xander", value="be like Fortnite")

    await ctx.send(embed=embed)

@client.command(hidden=True)
async def logan(ctx):
    embed = discord.Embed(title="Logan be like", colour=discord.Color.blue)

    embed.add_field(name="logan", value="be like retard")

    await ctx.send(embed=embed)


@client.command(hidden=True)
async def gracie(ctx):
    embed = discord.Embed(title='gracie be', description='like', colour=discord.Color.blue)

    embed.add_field(name='gracie', value='i dont know')

    await ctx.send(embed=embed)
zzz

#Role select for the general public [The Cave]
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

client.run("TOKEN")

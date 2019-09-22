# The Cave 2019 ^(C)
import discord
import json
from discord.ext import commands

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('tc/help | tc/invite'))
    print('The Cave is online.')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server with The Cave in it.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server with The Cave in it.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing Requirement Error [TC10]\nPass in all required arguments.')

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

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Missing Permissions Error [TC11]\nYou are not able to use this command because you do not have the required permissions.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms :ping_pong:')

#@client.command(aliases=['8ball', 'ahaha'])
#async def _8ball(ctx, *, question):
#    responses = ['It is certain.',   'It is decidedly so.', 'WIthout a doubt', 'Yes - definitely.', 'You may rely on it.', 'Yes sir!', 'Most likely.', 'Good', 'Yes.', 'North = Yes, and you are going north.', 'Try again...', 'Not telling you, yet', 'Can not say yes, can not say no.', 'Ask again', "Don't count on it", 'No', 'According to my sources, no', 'Nope', 'Never']
#    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Cleared {amount} messages.')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member}\nReason - {reason}')

@client.command()
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
    await ctx.send('Bump The Cave [Discord Server] on:\nDisboard: <https://disboard.org/server/560262402659057681> [go to bots then say "!d bump"]\nDiscordServers: <https://disc.gg/thecave>\nDiscord.me: <https://discord.me/thecavecord>\n\nBump The Cave [Discord Bot] on:\nDiscordBots.org - <https://discordbots.org/bot/624829444963696660>')

@client.command()
async def dev(ctx):
    await ctx.send('<@308000668181069824> developed me!')

@client.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'The prefix has changed to {prefix}')

@client.command()
async def invite(ctx):
    await ctx.send('You can invite The Cave to your server by going to\nhttps://discordapp.com/oauth2/authorize?client_id=624829444963696660&scope=bot&permissions=0')

client.run('process.env.discord_token')
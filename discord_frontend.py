import discord, asyncio, traceback
from discord.ext import commands
from credentials import discord_token
from controller import get_reply, get_general_error

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
previous_messages = []

@bot.event
async def on_ready():
    status = '!c help'
    await bot.change_presence(activity=discord.Game(name=status))

    # Debug
    print('Logged in as: {}'.format(bot.user.name))
    print("Currently active on servers:\n{}".format('\n'.join([guild.name for guild in bot.guilds])))
    print('-------------------')

@bot.command(aliases=['c'])
async def chat(ctx, *, name):
    conversation = ctx.message.content
    user = ctx.message.author.name + '#' + ctx.message.author.discriminator
    guild_id = ctx.message.guild.id
    thinking = discord.Embed().add_field(name="Thinking...", value="MeowBot is thinking...:thinking:")
    msg = await ctx.send(embed=thinking)

    try:
        reply = get_reply(conversation)
    except Exception as e:
        print ("Error when replying to message: {}".format(ctx.message.content), '\n', traceback.format_exc())
        reply = get_general_error()
    if not reply:
        print ("No reply generated.")
        reply = get_general_error()

    #print("Sending message:", reply)
    await msg.edit(embed=reply)


bot.run(discord_token)


#=============
#|| Imports ||
#=============
import config
import random
import nextcord
import logging
import jsonfs
from nextcord.ext import commands, application_checks# type: ignore
from nextcord import Interaction
from nextcord.utils import get
#===================
#|| Configuration ||
#===================
token=jsonfs.read("token.json")["token"]
intents=nextcord.Intents.default()
intents.members=True
intents.message_content=True
bot=commands.Bot(command_prefix='§',intents=intents)
handler=logging.FileHandler(filename='./discord.log',encoding='utf-8',mode='w')
logging.basicConfig(
    filename="./bot.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - [{levelname}]: {message}",
    style="{",
    datefmt="%Y/%m/%d - %H:%M"
)
#==========
#|| Boot ||
#==========
@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.CustomActivity(name=config.status))
    print(" ___            __   __        __   __  ___ ")
    print("|__   /\\  |    /  ` /  \\ |\\ | |__) /  \\  |")  
    print(f"|    /--\\ |___ \\__, \\__/ | \\| |__) \\__/  | {config.ver}") 
    print("────────────────────────────────────────────────────────────")
    print(random.choice(config.splash_text))
    print(f"Logged in as {bot.user}")
    print(f"Wrapper version: {nextcord.__version__}")
    print("---------------------------")
    print("Ctrl-C to exit bot program.")
    print("---------------------------")

#============
#|| Events ||
#============

#===============
#|| Commands ||
#===============

#===========================
#|| Application Commands ||
#===========================
#[] Help []
@bot.slash_command(description="Lists commands")
async def help(interaction:Interaction):
    print(f"Help command called by {interaction.user.name}")
    message=nextcord.Embed(title="App Commands", description="/verify - verifies a user\n/workhelp - calls for help with work\n/report - reports a user to admin")
    await interaction.send(embed=message, ephemeral=True)

#[] Verify []
@bot.slash_command(description="Verify a user")
@application_checks.has_role("Verified student")
async def verify(interaction: Interaction, username: nextcord.User):
    botlog=bot.get_channel(config.bot_log_id)
    print(f"Command invoked by {interaction.user.name}")
    role = get(interaction.guild.roles, name="Verified student")
    await username.add_roles(role)
    await botlog.send(f"{username.name} has been verified by {interaction.user.name}")
    await interaction.response.send_message(f"Verified {username.name}",ephemeral=True)

#[] Work Help []
@bot.slash_command(description="Request help with schoolwork!")
@application_checks.has_role("Verified student")
async def workhelp(interaction: Interaction, details:str):
    print(f"{interaction.user.name} Requested help with ticket {details}!")
    embedvar = nextcord.Embed(title="Work Help Request", description=f"<@&1282896327767756830> {interaction.user.name} needs help!\n{details}", color=0x00ff00)
    await interaction.response.send_message(embed=embedvar)

#[] Report []
@bot.slash_command(description="report a user for a server violation")
@application_checks.has_role("Verified student")
async def report(interaction:Interaction,user:nextcord.User,reason:str):
    adminonly= bot.get_channel(config.admin_only)
    print(f"{interaction.user.name} reported {user} for {reason}!")
    await adminonly.send(f"{interaction.user.name} reported {user} for {reason}")
    await interaction.send(f"Reported {user} for {reason}.",ephemeral=True)

#[] Memes []
@bot.slash_command(description="Sends a random meme")
async def meme(interaction: Interaction):
    await interaction.channel.typing()
    result = random.choice(list(config.meme_pick.items()))
    await interaction.send(str(result[1]))
    print(f'{interaction.user.name} used /meme and got {str(result[0])}!')

#[] Check []
@bot.slash_command(description="tests the bot and displays some info for the developers")
@application_checks.has_role("Admin")
async def check(interaction:Interaction):
    await interaction.send(f"{interaction}\n{interaction.user}\n{bot}\n{nextcord}\n{None}",ephemeral=True)

#[] Rando []
@bot.slash_command(name="rando",description="Displays some random sh*t")
async def rando(interaction:Interaction):
    await interaction.send(f"{random.choice(config.rando_list)}")

#====================
#|| Error handling ||
#====================
@bot.event
async def on_application_command_error(interaction:Interaction, error):
    if isinstance(error, application_checks.ApplicationBotMissingPermissions):
        await interaction.send("You don't have permission to run that!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await interaction.send("You forgot something...")
    else:
        await interaction.send(error)
#=========
#|| Run ||
#=========
bot.run(token)
# Created by Weird0cats - hosted on the deskPi server
from random import randint
import discord
import asyncio
from discord.ext import commands
import json

with open('config.json') as config_file:
    cfg = json.load(config_file)

bot = discord.Client()
#set command prefix
bot = commands.Bot(command_prefix='!', description="SpliMo Becko zu Ihren Diensten!")
#we want our own help command later
bot.remove_command('help')

#used for purge command
def is_me(m):
    return m.author == bot.user

####################################################################################################################################################################

@bot.command(name="help", description="alle Kommandos")
async def help(ctx):
    embed=discord.Embed()
    embed.add_field(name="!help", value="Diese Nachricht", inline=False)
    embed.add_field(name="!info", value="Gibt Infos über den Bot zurück", inline=False)
    embed.add_field(name="!roll normal+X", value="Standardwurf. X entspricht den Talentpunkten", inline=False)
    embed.add_field(name="!roll sicherheit+X", value="Sicherheitswurf. X entspricht den Talentpunkten", inline=False)
    embed.add_field(name="!roll risiko+X", value="Risikowurf. X entspricht den Talentpunkten", inline=False)
    embed.add_field(name="!roll initiative-X", value="Initiativewurf. X entspricht dem Wert INI", inline=False)
    embed.add_field(name="!roll coin", value="Wirf eine Münze", inline=False)
    embed.add_field(name="!roll XwY+Z oder XwY-Z oder XwY", value="Würfelwurf. X entspricht Anzahl, Y Entspricht Art (6, 10) Z entspricht Modifikator (Modifikator ist optional)", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="SpliMo Becko", description="Simpler Splittermond Bot", color=0xeee657)
    # give info about you here
    embed.add_field(name="Author", value=cfg['author'], inline=False)
    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}", inline=False)
    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value=cfg['invitelink'], inline=False)
    await ctx.send(embed=embed)

def roll_normal(talentpoints):
    y = randint(1, 10)
    x = randint(1, 10)
    z = y + x
    if z <= 3:
        return("Standardwurf: [{},{}] >>> **Patzer!**".format(str(y),str(x)))
    else:
        ergebnis = z + int(talentpoints)
        if z >= 19:
            return("Standardwurf: [{},{}] >>> ({}) + Talentpunkte({}) = **Krit!** **{}**".format(str(y),str(x),str(z),str(talentpoints),str(ergebnis)))
        return("Standardwurf: [{},{}] >>> ({}) + Talentpunkte({}) = **{}**".format(str(y),str(x),str(z),str(talentpoints),str(ergebnis)))

def roll_sicherheit(talentpoints):
    y = randint(1, 10)
    z = y + int(talentpoints)
    return("Sicherheitswurf: [{}] >>> ({}) + Talentpunkte({}) = **{}**".format(str(y),str(y),str(talentpoints),str(z)))

def roll_risiko(talentpoints):
    integers = [randint(1,10),randint(1,10),randint(1,10),randint(1,10)]
    sorted_integers = sorted(integers, reverse=True)
    largest_integer = sorted_integers[0]
    smallest_integer = sorted_integers[-1]
    second_largest_integer = sorted_integers[1]
    second_smallest_integer = sorted_integers[-2]
    if smallest_integer + second_smallest_integer <= 3:
        return("Risikowurf: {} >>> **Patzer!**".format(str(integers)))
    erg = largest_integer + second_largest_integer
    z = erg + int(talentpoints)
    if largest_integer + second_largest_integer >= 19:
        return("Risikowurf: {} >>> ({}) + Talentpunkte({}) = **Krit!** **{}**".format(str(integers),str(erg),str(talentpoints),str(z)))
    return("Risikowurf: {} >>> ({}) + Talentpunkte({}) = **{}**".format(str(integers),str(erg),str(talentpoints),str(z)))

def coin():
    z = randint(1,2)
    if z == 1:
        ergebnis = "Kopf"
    else:
        ergebnis = "Zahl"
    return("Münzwurf ergibt: {}".format(ergebnis))

def roll_initiative(initiative):
    w = randint(1,6)
    ergebnis = int(initiative) - w
    return("Initiativewurf: [{}] >>> ({}) + Initiative({}) = **{}**".format(str(w),str(w),str(initiative),str(ergebnis)))

def roll_schaden(dice_count,dice_type,mod,plumin):
    total = 0
    results = ''
    numbers=[]
    for x in range(0, int(dice_count)):
        y = randint(1, int(dice_type))
        numbers.append(y)
        total += y
    ergebeforemod = total
    if plumin == "plus":
        total += int(mod)
        return("{}W{}+{} Wurf: {} >>> ({}) + Modifikator({}) = **{}**".format(int(dice_count),int(dice_type),int(mod),numbers,ergebeforemod,int(mod),total))
    elif plumin == "minus":
        total -= int(mod)
        return("{}W{}-{} Wurf: {} >>> ({}) - Modifikator({}) = **{}**".format(int(dice_count),int(dice_type),int(mod),numbers,ergebeforemod,int(mod),total))
    else:
        return("{}W{} Wurf: {} >>> ({}) = **{}**".format(int(dice_count),int(dice_type),numbers,ergebeforemod,total))
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# Parse !roll verbiage
@bot.command(pass_context=True,description='')
async def roll(ctx, roll : str):
    author = ctx.message.author.mention
    try:
        if (roll.find('normal') != -1):
            roll, talentpunkte = roll.split('+')
            await ctx.send("{}: {}".format(author,roll_normal(talentpunkte)))
            return
        if (roll.find('sicherheit') != -1):
            roll, talentpunkte = roll.split('+')
            await ctx.send("{}: {}".format(author,roll_sicherheit(talentpunkte)))
            return
        if (roll.find('risiko') != -1):
            roll, talentpunkte = roll.split('+')
            await ctx.send("{}: {}".format(author,roll_risiko(talentpunkte)))
            return
        if (roll.find('initiative') != -1):
            roll, initiative = roll.split('-')
            await ctx.send("{}: {}".format(author,roll_initiative(initiative)))
            return
        if (roll.find('coin') != -1):
            await ctx.send("{}: {}".format(author,coin()))
            return
        if ((roll.find('w') != -1)):
            dice_count,roll = roll.split('w')
            if "+" in roll:
                dice_type, mod = roll.split('+')
                plumin = "plus"
            elif "-" in roll:
                dice_type, mod = roll.split('-')
                plumin = "minus"
            else:
                dice_type = roll
                mod = 0
                plumin = "nix"
            await ctx.send("{}: {}".format(author,roll_schaden(dice_count,dice_type,mod,plumin)))
            return
        else:
            await ctx.send("Befehl nicht gefunden, benutze !help um die verfügbaren Befehle anzuzeigen")
            return
    except Exception as e:
        await ctx.send("Da hat Becko wohl gepatzt... Fehler: ```{}```".format(e))
        return
@bot.command(pass_context=True,description='Deletes all messages the bot has made')
async def purge(ctx):
    channel = ctx.message.channel
    deleted = await channel.purge(limit=200, check=is_me)
    await ctx.send('Deleted {} message(s)'.format(len(deleted)))

@bot.command(pass_context=True,description='Deletes all messages')
async def purgeall(ctx):
    channel = ctx.message.channel
    deleted = await channel.purge(limit=200)
    await ctx.send('Deleted {} message(s)'.format(len(deleted)))

bot.run(cfg['apikey'])
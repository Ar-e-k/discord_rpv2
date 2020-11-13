import discord
from discord.ext import commands as coms
import pickle
import time
import datetime

help_info = {
    "all_countries": [
        "List of all the existing countries",
        "..."
    ],
    "country_info": [
        "Gives basic information about a target country",
        "This command gives you info about a given country.\nYou need to input your country name. The info you are getting is not exact!"
    ],
    "country_info_priv": [
        "Gives private information about your country",
        "This command gives you private info about your country and sends the info to your private country chat.\nYou do not need to input your country name!"
    ],
    "country_info_all": [
        "Gives all information about target country",
        "This command gives you info about a given country.\nYou need to input your country name.\nThis is admin only command"
    ],
    "fight": [
        "Simulate a battle",
        "This command takes no arguments when called.\nRather you input the specifics of each unit in the army later. The specifics are to be separated by spaces. They are number of units (unlimited number), unit level (a number between 1-100) and the position (number between 1 and 4, can not have two same positions in the same army)"
    ],
    "clear": [
        "Clears a given amount of messages in the channel",
        "It takes the number of messages you want to clear.\nExclude the clear message you sending!\nIf you give no argument, it will clear 10"
    ],
    "ping": [
        "Shows the bot ping",
        "The brief really tells the whole story"
    ],
    "change": [
        "Change the modifiers of the country",
        "Change the modifiers for the country.\nInput the value you want to change, and then the new values.\nYou can change the following values:\nTax_rate, Technology_spending, Building_spending, Benefits_spending, Economy_spending, Army"
    ],
    "add": [
        "Add some stuff to your numerical modifiers",
        "Same as change, only works for numerical modifiers. Adds or subtructs (use -) to  the modifier"
    ],
    "modify": [
        "Same as change just for different values",
        "Can be used by the hosts exclusively.\nUnlike change it needs a country argument\nIt has all the options that change has, also including the following:\nEconomy_tier, Stability_mod, Population, Area, Form, Culture\nIt can also be used to correct stability and libery"
    ],
    "mod_add": [
        "Same as add just more numbers",
        "Can be used by the hosts exclusively\nAlso include pick country argument later, just like the modify"
    ],
    "update": [
        "Update all countires values",
        "..."
    ],
    "change_name": [
        "Change the name of the country",
        "Input the new name of the coutnry"
    ],
}

client = coms.Bot(command_prefix="%")
channels = {}


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("Executing operation Barbarossaaa"))
    print("ready")

# Operators


async def runner(func, channel):
    alert = func
    if alert != None:
        await channel.send(alert)


def get_channels(client):
    for guild in client.guilds:
        for channel in guild.channels:
            chan = str(channel).lower()
            chan = chan.replace("-", " ")
            if chan in list(all_country.keys()):
                channels[chan] = channel
    if len(all_country.keys()) != len(channels.keys()):
        missing = ""
        for i in list(all_country.keys()):
            if i in list(channels.keys()):
                pass
            else:
                missing += str(i)
                missing += ", "
        return str("Invalid channal naming, missing "+missing)
    return channels


def check_country(ctx):
    roles = ctx.author.roles
    for role in roles:
        if str(role).lower() in channels.keys():
            return [True, str(role).lower()]
    else:
        return [False]
####

# Server actons


@client.command()
@coms.has_permissions(administrator=True)
async def init(ctx):
    import init_countries
    global all_country
    all_country = init_countries.read_stats()
    channels = get_channels(client)
    if type(channels) == str:
        await ctx.send(channels)
        del channels
        del all_country
    else:
        await ctx.send("Game loaded successfully")


@client.command()
@coms.has_permissions(administrator=True)
async def load(ctx, name):
    dbfile = open('saves/'+name, 'rb')
    global all_country
    all_country = pickle.load(dbfile)
    dbfile.close()
    channels = get_channels(client)
    if type(channels) == str:
        await ctx.send(channels)
        del channels
        del all_country
    else:
        await ctx.send("Game loaded successfully")


@client.command()
@coms.has_permissions(administrator=True)
async def save(ctx, name):
    dbfile = open('saves/'+name, 'ab')
    pickle.dump(all_country, dbfile)
    dbfile.close()
    await ctx.send("Game saved succesfully")
####

# Country info


@client.command(brief=help_info["all_countries"][0], description=help_info["all_countries"][1])
async def all_countries(ctx):
    await ctx.send(list(all_country.keys()))


@client.command(brief=help_info["country_info"][0], description=help_info["country_info"][1])
async def country_info(ctx, *, name):
    try:
        text = all_country[name].return_pub()
    except:
        await ctx.send("Invalid argument")
        return None
    await ctx.send(text)
####

# Country commands


@client.command(brief=help_info["country_info_priv"][0], description=help_info["country_info_priv"][1])
async def country_info_priv(ctx):
    checked = check_country(ctx)
    if checked[0]:
        pass
    else:
        await ctx.send("You have no country")
        return None
    all = all_country[checked[1]].return_priv()
    channel = channels[str(checked[1]).lower()]
    for cat in all.keys():
        try:
            text = cat+": "+str(all[cat])
            await channel.send(text)
        except TypeError:
            text = cat
            text2 = all[cat]
            await channel.send(text)
            await channel.send(text2)


@client.command(brief=help_info["change"][0], description=help_info["change"][1])
async def change(ctx, source, value=None):
    if value == None:
        await ctx.send("No value")
        return None
    else:
        pass
    checked = check_country(ctx)
    if checked[0]:
        pass
    else:
        await ctx.send("You have no country")
    await ctx.send(all_country[checked[1]].change(source, value))


@client.command(brief=help_info["change_name"][0], description=help_info["change_name"][1])
async def change_name(ctx,  *, value):
    if value == None:
        await ctx.send("No value")
        return None
    else:
        pass
    checked = check_country(ctx)
    if checked[0]:
        pass
    else:
        await ctx.send("You have no country")
    value = value.lower()
    if value == str(checked[1]).lower():
        await ctx.send("Thats already your country name")
        return None
    channel = channels[str(checked[1]).lower()]
    for guild in client.guilds:
        for role in guild.roles:
            if role.name == str(checked[1]).lower():
                break
    await role.edit(name=value)
    all_country[value] = all_country[checked[1]]
    channels[value] = channels[checked[1]]
    del all_country[checked[1]]
    del channels[checked[1]]
    alert = (all_country[value].change("name", value))
    await ctx.send(alert)


@client.command(brief=help_info["add"][0], description=help_info["add"][0])
async def add(ctx, source, value=None):
    if value == None:
        await ctx.send("No value")
        return None
    else:
        pass
    checked = check_country(ctx)
    if checked[0]:
        pass
    else:
        await ctx.send("You have no country")
    await ctx.send(all_country[checked[1]].add(source, value, add=True))


@client.command()
async def return_army(ctx, typ="whole", sub_type="none", *, name="none"):
    checked = check_country(ctx)
    if checked[0]:
        pass
    else:
        await ctx.send("You have no country")
        return None
    if typ.lower() == "whole":
        await ctx.send(all_country[checked[1]].return_army(sub_type))
    elif typ.lower() in ["division", "template"]:
        await ctx.send(all_country[checked[1]].return_division(typ, sub_type, name))


@client.command()
async def change_division(ctx, typ, name, *, kwarg="all"):
    checked = check_country(ctx)
    if checked[0]:
        pass
    else:
        await ctx.send("You have no country")
        return None
    if typ.lower() in ["add", "change_template", "delete"]:
        await ctx.send(all_country[checked[1]].change_division(typ, name, kwarg))
    elif typ.lower() in ["reinforce_all", "reinforce"]:
        await ctx.send(all_country[checked[1]].change_division_detail(typ, name, kwarg))
    else:
        await ctx.send("Invalid type")


@client.command()
async def change_template(ctx, typ, sub_type, name, *, kwarg):
    checked = check_country(ctx)
    if checked[0]:
        pass
    else:
        await ctx.send("You have no country")
        return None
    if typ.lower() in ["add", "update"]:
        await ctx.send(all_country[checked[1]].change_template(typ, name, kwarg, sub_type=sub_type))
####

# Mod control


@client.command(brief=help_info["country_info_all"][0], description=help_info["country_info_all"][0])
@coms.has_permissions(administrator=True)
async def country_info_all(ctx, *, name):
    try:
        all = all_country[name].return_all()
    except:
        await ctx.send("Invalid argument")
        return None
    for cat in all:
        mes = cat+": "+str(all[cat])
        await ctx.send(mes)


@client.command(brief=help_info["modify"][0], description=help_info["modify"][1])
@coms.has_permissions(administrator=True)
async def modify(ctx, source, value=None):
    await ctx.send("What country:")
    while True:
        country = await client.wait_for('message')
        if country.author == ctx.author:
            pass
        else:
            continue
        if country.clean_content.lower() in all_country.keys():
            country = country.clean_content
            break
        else:
            if country.clean_content.lower() == "stop":
                return None
            else:
                await ctx.send("Not a country")
    if value == None:
        await ctx.send("No value")
    else:
        pass
    await ctx.send(all_country[country].change(source, value, admin=True))


@client.command(brief=help_info["mod_add"][0], description=help_info["mod_add"][1])
@coms.has_permissions(administrator=True)
async def mod_add(ctx, source, value=None):
    await ctx.send("What country:")
    while True:
        country = await client.wait_for('message')
        if country.author == ctx.author:
            pass
        else:
            continue
        if country.clean_content.lower() in all_country.keys():
            country = country.clean_content.lower()
            break
        else:
            if country.clean_content() == "stop":
                return None
            else:
                await ctx.send("Not a country")
    if value == None:
        await ctx.send("No value")
    else:
        pass
    await ctx.send(all_country[country].change(source, value, admin=True, add=True))


@client.command(brief=help_info["update"][0], description=help_info["update"][1])
@coms.has_permissions(administrator=True)
async def update_all(ctx, *, country="None"):
    country = country.lower()
    if country == "none":
        for country in all_country.keys():
            func = all_country[country].update()
            await runner(func, channels[str(country).lower()])
    elif country in all_country.keys():
        await runner(all_country[country].update(), channels[country])
    else:
        await ctx.send("Invalid country")
        return None
    await ctx.send("Task successfull")
####

# Maintainance functions
'''


@client.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, coms.MissingRequiredArgument):
        await ctx.send("Invalid argument\nTry help command name, to see what arguments you require")
    elif isinstance(error, coms.MissingPermissions):
        await ctx.send("Dont try it\nIf you need the command please contact an admin")
    elif isinstance(error, coms.CommandNotFound):
        await ctx.send("There is no such command\nTry %help command to see the avaliable commands")
# '''


@client.command(brief=help_info["clear"][0], description=help_info["clear"][1])
@coms.has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    try:
        await ctx.channel.purge(limit=(amount+1))
    except:
        await ctx.send("Invalid argument")


@client.command(brief=help_info["ping"][0], description=help_info["ping"][1])
async def ping(ctx):
    await ctx.send(client.latency*1000)
####

client.run('NzE5ODAyNDM0MDA3OTkwMzU1.Xt8uQQ.Y8L6__FGGTQQghIhY_IWu1qlG7U')

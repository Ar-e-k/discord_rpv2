import csv
import discord
from discord.ext import commands as coms
import copy
import country as main
import time

help_info={
    "all_countries":[
        "List of all the existing countries",
        "..."
        ],
    "country_info":[
        "Gives basic information about a target country",
        "This command gives you info about a given country.\nYou need to input your country name. The info you are getting is not exact!"
        ],
    "country_info_priv":[
        "Gives private information about your country",
        "This command gives you private info about your country and sends the info to your private country chat.\nYou do not need to input your country name!"
        ],
    "country_info_all":[
        "Gives all information about target country",
        "This command gives you info about a given country.\nYou need to input your country name.\nThis is admin only command"
        ],
    "fight":[
        "Simulate a battle",
        "This command takes no arguments when called.\nRather you input the specifics of each unit in the army later. The specifics are to be separated by spaces. They are number of units (unlimited number), unit level (a number between 1-100) and the position (number between 1 and 4, can not have two same positions in the same army)"
        ],
    "clear":[
        "Clears a given amount of messages in the channel",
        "It takes the number of messages you want to clear.\nExclude the clear message you sending!\nIf you give no argument, it will clear 10"
        ],
    "ping":[
        "Shows the bot ping",
        "The brief really tells the whole story"
        ],
    "change":[
        "Change the modifiers of the country",
        "Change the modifiers for the country.\nInput the value you want to change, and then the new values.\nYou can change the following values:\nTax_rate, Technology_spending, Building_spending, Benefits_spending, Economy_spending, Army"
        ],
    "add":[
        "Add some stuff to your numerical modifiers",
        "Same as change, only works for numerical modifiers. Adds or subtructs (use -) to  the modifier"
        ],
    "modify":[
        "Same as change just for different values",
        "Can be used by the hosts exclusively.\nUnlike change it needs a country argument\nIt has all the options that change has, also including the following:\nEconomy_tier, Stability_mod, Population, Area, Form, Culture\nIt can also be used to correct stability and libery"
        ],
    "mod_add":[
        "Same as add just more numbers",
        "Can be used by the hosts exclusively\nAlso include pick country argument later, just like the modify"
        ],
    "update":[
        "Update all countires values",
        "..."
        ],
    "change_name":[
        "Change the name of the country",
        "Input the new name of the coutnry"
        ],
    }

client=coms.Bot(command_prefix="%")
#global channels
channels={}

world=[]
with open("info/World_priv(backup)(copy).csv") as world_map:
    reader=csv.reader(world_map)
    for line in reader:
        world.append(line)
world.pop(0)
all_country={}
#print(world)
for country in world:
    all_country[country[0].upper()]=main.country_init(country[0].upper())
del world

async def runner(func, channel):
    alert=func
    if alert!=None:
        await channel.send(alert)

@client.event
async def on_ready():
    channels=get_channels(client)
    await client.change_presence(activity=discord.Game("Executing operation Barbarossaaa"))
    print("ready")

def get_channels(client):
    for guild in client.guilds:
        for channel in guild.channels:
            chan=str(channel).upper()
            chan=chan.replace("-", " ")
            if chan in list(all_country.keys()):
                channels[chan]=channel
    return channels

def check_country(ctx):
    roles=ctx.author.roles
    #print(channels.keys())
    for role in roles:
        #print("role", str(role))
        if str(role).upper() in channels.keys():
            return [True, str(role).upper()]
    else:
        return [False]

@client.command(brief=help_info["country_info_priv"][0], description=help_info["country_info_priv"][1])
async def country_info_priv(ctx):
    checked=check_country(ctx)
    if checked[0]:
        all=all_country[checked[1]].return_priv()
        channel=channels[str(checked[1]).upper()]
        #print(all)
        for cat in all.keys():
            try:
                text=cat+": "+str(all[cat])
                await channel.send(text)
            except TypeError:
                text=cat
                text2=all[cat]
                await channel.send(text)
                await channel.send(text2)
    else:
        await ctx.send("You have no country")

@client.command(brief=help_info["country_info"][0], description=help_info["country_info"][1])
async def country_info(ctx, *, name):
    try:
        text=all_country[name.upper()].return_pub()
    except:
        await ctx.send("Invalid argument")
        return None
    await ctx.send(text)

@client.command(brief=help_info["country_info_all"][0], description=help_info["country_info_all"][0])
@coms.has_permissions(administrator=True)
async def country_info_all(ctx, *, name):
    try:
        all=all_country[name.upper()].return_all()
    except:
        await ctx.send("Invalid argument")
        return None
    for cat in all:
        print(cat)
        await ctx.send(cat)

@client.command(brief=help_info["all_countries"][0], description=help_info["all_countries"][1])
async def all_countries(ctx):
    await ctx.send(list(all_country.keys()))

#@client.command()
async def random_input(ctx, mes, stats, amount, check=False):
    await ctx.send(mes)
    while True:
        res=await client.wait_for('message')
        if res.author==ctx.author:
            pass
        else:
            continue
        if res.clean_content=="stop":
            amount+=2
            return None, amount
        res=res.clean_content.split(" ")
        if len(res)==check or check==False:
            break
        else:
            amount+=2
            await ctx.send("Invalid number of arguments")
    for r in res:
        stats.append(r)
    amount+=2
    return stats, amount

@client.command(brief=help_info["fight"][0], description=help_info["fight"][1])
async def fight(ctx):
    await ctx.send("Currently not avaliable")
    return None
    stats=[]
    amount=1
    try:
        info=["Attacking soldiers: ", "Attacking archers: ", "Attacking cavalery: ", "Attacking artilery: ", "Defending soldiers: ", "Defending archers: ", "Defending cavalery: ",  "Defending artilery: "]
        for name in info:
            stats, amount=await random_input(ctx, name, stats, amount, 3)
            list(stats)
    except TypeError:
        await ctx.channel.purge(limit=(amount))
        return None
    for stat in stats:
        try:
            stats[stats.index(stat)]=float(stat)
        except ValueError:
            await ctx.send("Invalid argument")
            break
    else:
        if len(stats)==24:
            lis=["attacker survived:", "defender survived:"]
            result=battle.analize_stats(stats[0:12], stats[12:24])
            #print(type(result))
            #print(result)
            if len(result)!=1:
                result.insert(1, lis[0])
                result.insert(3, lis[1])
            await ctx.channel.purge(limit=(amount))
            for i in range(len(result)):
                mes=result[i]
                #print(amount)
                await ctx.send(mes)
        else:
            #await ctx.channel.purge(amount)
            await ctx.send("Invalid argument")

async def input_army(ctx, info):
    try:
        amount=0
        value=[]
        for name in info:
            value, amount=await random_input(ctx, name, value, amount, False)
            list(value)
            int(value-1)
        return value, amount
    except TypeError or ValueError:
        return None, amount

@client.command(brief=help_info["change"][0], description=help_info["change"][1])
async def change(ctx, source, value=None):
    if value==None:
        await ctx.send("No value")
    else:
        pass
    checked=check_country(ctx)
    if checked[0]:
        if value==None:
                await ctx.send("No value")
        else:
            pass
        await ctx.send(all_country[checked[1]].change(source, value))
    else:
        await ctx.send("You have no country")

@client.command(brief=help_info["change_name"][0], description=help_info["change_name"][1])
async def change_name(ctx,  *, value):
    #print("\n\n\n")
    checked=check_country(ctx)
    if checked[0]:
        if value.upper()==str(checked[1]).upper():
            await ctx.send("Thats already your country name")
            return None
        channel=channels[str(checked[1]).upper()]
        for guild in client.guilds:
            for role in guild.roles:
                #print(role.name)
                if role.name.upper()==str(checked[1]).upper():
                    break
        alert=(all_country[checked[1]].change_name(value))
        if "Task successfull" in alert:
            print("here")
            #print(list(all_country.keys()))
            #print(channel.name)
            value=value.upper()
            all_country[value]=all_country[checked[1]]
            channels[value]=channels[checked[1]]
            print("here1.5")
            print(await role.edit(name=value))
            print(channel.id)
            t=time.time()
            print(await channel.edit(name=value))
            print(time.time()-t)
            del t
            print("here2")
            del all_country[checked[1]]
            del channels[checked[1]]
            #print(list(all_country.keys()))
            print("here3")
        await ctx.send(alert)
    else:
        await ctx.send("You have no country")

@client.command(brief=help_info["add"][0], description=help_info["add"][0])
async def add(ctx, source, value=None):
    if value==None:
        await ctx.send("No value")
    else:
        pass
    checked=check_country(ctx)
    if checked[0]:
        await ctx.send(all_country[checked[1]].add(source, value, False))
    else:
        await ctx.send("You have no country")

@client.command(brief=help_info["modify"][0], description=help_info["modify"][1])
async def modify(ctx, source, value=None):
    await ctx.send("What country:")
    while True:
        country=await client.wait_for('message')
        if country.author==ctx.author:
            pass
        else:
            continue
        if country.clean_content.upper() in all_country.keys():
            country=country.clean_content
            break
        else:
            if country.clean_content.upper()=="STOP":
                return None
            else:
                await ctx.send("Not a country")
    if source.upper()=="ARMY" or source.upper()=="NAVY":
        await ctx.send("What unit:")
        while True:
            unit=await client.wait_for('message')
            if unit.author==ctx.author:
                break
            else:
                continue
        units=["SOL", "ARCH", "CAV", "ART", "LIGH", "CON", "HEAV", "BORD"]
        if unit.clean_content.upper() in units[0:4]:
            unit=unit.clean_content.upper()
            await ctx.send(all_country[country.upper()].change_army(value, unit, "Army"))
        elif unit.clean_content.upper() in units[4:7]:
            unit=unit.clean_content
            await ctx.send(all_country[country.upper()].change_army(value, unit, "Navy"))
        else:
            await ctx.send("Not a country")
            return None
        return None
    else:
        if value==None:
            await ctx.send("No value")
        else:
            pass
    await ctx.send(all_country[country.upper()].change(source, value, True))

@client.command(brief=help_info["mod_add"][0], description=help_info["mod_add"][0])
@coms.has_permissions(administrator=True)
async def mod_add(ctx, source, value=None):
    await ctx.send("What country:")
    while True:
        country=await client.wait_for('message')
        if country.author==ctx.author:
            pass
        else:
            continue
        if country.clean_content.upper() in all_country.keys():
            country=country.clean_content
            break
        else:
            if country.clean_content.upper()=="STOP":
                return None
            else:
                await ctx.send("Not a country")
    if value==None:
        await ctx.send("No value")
    else:
        pass
    if source.upper()=="ARMY" or source.upper()=="NAVY":
        await ctx.send("What unit:")
        while True:
            unit=await client.wait_for('message')
            if unit.author==ctx.author:
                break
            else:
                continue
        units=["SOL", "ARCH", "CAV", "ART", "LIGH", "CON", "HEAV", "BORD"]
        if unit.clean_content.upper() in units[0:4]:
            unit=unit.clean_content.upper()
            await ctx.send(all_country[country.upper()].add_army(value, unit, "Army"))
        elif unit.clean_content.upper() in units[4:7]:
            unit=unit.clean_content
            await ctx.send(all_country[country.upper()].add_army(value, unit, "Navy"))
        else:
            await ctx.send("Not a country")
            return None
        return None
    await ctx.send(all_country[country.upper()].add(source, value, True))

@client.command(brief=help_info["update"][0], description=help_info["update"][1])
@coms.has_permissions(administrator=True)
async def update_all(ctx, *, country="None"):
    country=country.upper()
    if country=="NONE":
        #print("keys", channels.keys())
        for country in all_country.keys():
            #print("country", country)
            #print(country in all_country.keys())
            func=all_country[country].update_save()
            await runner(func, channels[str(country).upper()])
    elif country in all_country.keys():
        await runner(all_country[country].update_save(), channels[str(country).upper()])
    else:
        await ctx.send("Invalid country")
        return None
    await ctx.send("Task successfull")

######################################################################################################################################
######################################################################################################################################
#function commands
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
#'''

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

@client.command()
@coms.has_permissions(administrator=True)
async def debug_foo(ctx, var=None):
    if var==None:
        print(globals())
        print()
        return None
    try:
        print(var)
        print(globals()[var])
        print()
    except KeyError:
        print(var)
        print("Dosent exist")
        print()

client.run('NzE5ODAyNDM0MDA3OTkwMzU1.Xt8uQQ.cWmLhzzsLnC7woQnMMGEzlGZflU')

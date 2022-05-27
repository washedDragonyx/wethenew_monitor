import requests
import time
import json
import os
from dhooks import Webhook, Embed
from threading import Thread
from colorama import Fore, Back, Style
from discord.ext import commands
os.system('cls')


client = commands.Bot(command_prefix = '+')
@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def sbx(ctx):
    await ctx.send(ctx.command)

@client.event
async def on_message(message):
    if message.content.startswith("+add"):
        msg = message.content[5:]
        msg = str(msg).split(',')
        pid = msg[0]
        name = msg[1]
        thread = Thread(target = wethenew, args = (pid, name))
        thread.start()



def wethenew(pid,name):
    
    params = {
        'skip': '0',
        'take': '100',
        'keywordSearch': str(name),
        'onlyWanted': 'true',
    }
    oldSizes = ""
    while True:
        r = requests.get('https://sell.wethenew.com/api/products', params=params)
        if r.status_code == 200:
            try:
                data = json.loads(r.text)
                name = data["results"][0]["name"]
                id = data["results"][0]["id"]
                image = data["results"][0]["image"]
                wantedSizes = data["results"][0]["wantedSizes"]

                if str(id) == str(pid):

                    if oldSizes == "":
                        print(' [ '+ time.strftime('%H:%M:%S') + ' ] '+ Fore.CYAN+"Found : "+str(name)+" with pid "+str(pid))

                    if wantedSizes != oldSizes:
                        oldSizes = wantedSizes
                        print(' [ '+ time.strftime('%H:%M:%S') + ' ] '+ Fore.GREEN+"Found changes in : "+str(name)+" with pid "+str(pid))
                        hook = Webhook('INSERT WEBHOOK HERE')
                        embed = Embed(
                                        color = 0xfe7812,
                                        description = str(id),
                                        timestamp= 'now'
                                    )
                        embed.set_title(title= 'Wethenew', url= 'https://sell.wethenew.com/listing/product/'+str(id)) 
                        embed.add_field(name = 'Item', value = str(name),inline = False)
                        embed.add_field(name = 'Wantedsizes', value = str(wantedSizes))
                        embed.set_footer(text= 'Wethenew Monitor | Dragonyx', icon_url='https://pbs.twimg.com/profile_images/1387046154186084355/9B34r5d2_400x400.jpg')
                        embed.set_thumbnail(image)
                        hook.send(embed=embed)
                    else:
                        print(' [ '+ time.strftime('%H:%M:%S') + ' ] '+ Fore.YELLOW+"No changes found : "+str(name)+" with pid "+str(pid))
                else:
                    print(' [ '+ time.strftime('%H:%M:%S') + ' ] '+ Fore.MAGENTA+"No product found with pid "+str(pid))        
            except:
                print("Error")
            
            time.sleep(2)

        else:
            print(' [ '+ time.strftime('%H:%M:%S') + ' ] '+ Fore.RED+"Request error: "+str(r.status_code))
            time.sleep(200)



client.run('INSERT DISCORD TOKEN HERE')

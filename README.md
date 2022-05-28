<p float="left">
  <img src="https://github.com/NaeCqde/Verify_Bot/blob/images/d0g3h4ck3r-Verification.gif" width="600" />
  <img src="https://github.com/NaeCqde/Verify_Bot/blob/images/verify.png" width="400" />
</p>

# Discord 認証BOT

![stars](https://img.shields.io/github/stars/NaeCqde/Verify_Bot) ![fork](	https://img.shields.io/github/forks/NaeCqde/Verify_Bot) ![issues](https://img.shields.io/github/issues/NaeCqde/Verify_Bot) ![license](https://img.shields.io/github/license/NaeCqde/Verify_Bot) [![Coverage Status](https://coveralls.io/repos/github/NaeCqde/Verify_Bot/badge.svg?branch=main)](https://coveralls.io/github/NaeCqde/Verify_Bot?branch=main) [🎈HomePage](http://ezz.gg/)

#### これはDiscord上にいるPython#6084別名core#3328が作ったものです 僕自身はEmbedと設定項目しかやっていません

#### このコード使ってるのが確認できてお前が自作発言してたらつぶします By なえこーど

#### [こ↑こ↓](http://ezz.gg/verify_bot)でも紹介してます！笑

## kwsk

### サーバーのロール付与+バックアップサーバーなどに入れさせる機能が内臓してます
#### 作者(Pythonさん)が3時間で作れたくらいの難しさらしいです
#### すごいよなーって思いますよね？？僕も尊敬します！！
#### 認証はDiscordのRedirectsを使ってユーザーを識別してロール付与、サーバーJoinをさせています
#### 実はあのボタンはURLを踏ませてるだけです笑

![](https://github.com/NaeCqde/Verify_Bot/blob/images/verify_sample-beta.gif)


## セットアップ

### 1. ライブラリのインストール

##### Linux

```python3 -m pip install -U flask requests py-cord --pre```

##### Windows

```py -3 -m pip install -U flask requests py-cord --pre```


### 2. [```server.py```](https://github.com/NaeCqde/Verify_Bot/blob/main/server.py)の中身をいじる(.env作ってませんスマソ...)

#### [```server.py```](https://github.com/NaeCqde/Verify_Bot/blob/main/server.py)みて察してください()

### 察してもわからない内容

##### ロールを付与したいサーバーにだけ権限付きにしてください

##### 認証後入れさせたいサーバーには権限の無い(あってもいい)BOTを入れてください

#### 1つのサーバーじゃなくて2つ以上のサーバーに入れたくなったら

##### 12,35,60行目のコメント化を解除してください

##### 12行目の```join_guild_2 = ```は```= serverid```としてください

#### もし3つ以上増やしたくなったら12.35.60を増やしてください やり方は察してください

##### ↓ ```server.py```の設定 ↓

<details>
<summary>クリック又はタップで展開</summary>
<pre>
<code>
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
bot_prefix = "p!"
</code>
</pre>
</details>


### 3. 起動

```Python3 server.py```

##### data.jsonの初期状態

```{"last_update":0, "data":{}}```

## Setup Images

<details>
<summary>クリック又はタップで展開</summary>
<pre>
<p float="left">
  <img src="https://github.com/NaeCqde/Verify_Bot/blob/images/Verify_BOT_SETUP_1.png" width="300" />
  <img src="https://github.com/NaeCqde/Verify_Bot/blob/images/Verify_BOT_SETUP_2.png" width="300" />
  <img src="https://github.com/NaeCqde/Verify_Bot/blob/images/Verify_BOT_SETUP_3.png" width="600" />
  <img src="https://github.com/NaeCqde/Verify_Bot/blob/images/Verify_BOT_SETUP_4.png" width="400" />
  <img src="https://github.com/NaeCqde/Verify_Bot/blob/images/Verify_BOT_SETUP_5.png" width="400" />
  <img src="https://github.com/NaeCqde/Verify_Bot/blob/images/Verify_BOT_SETUP_6.png" width="700" />
  <img src="https://github.com/NaeCqde/Verify_Bot/blob/images/Verify_BOT_SETUP_7.png" width="700" />
  <img src="https://github.com/NaeCqde/Verify_Bot/blob/images/Verify_BOT_SETUP_8.png" width="500" />
</p>
</pre>
</details>

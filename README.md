# DiscordOTP-SelfBot  
Q.これは何ですか？  
A.これはDiscord上でセルフボットを用いてOTPコードを取得するコードです！   
## 使い方  
1.リポジトリをクローンする  

    $ git clone https://github.com/yuffycord/DiscordOTP-SelfBot
    $ cd DiscordOTP-SelfBot  
2.必要ライブラリのインストール
```sh
                 $ pip install git+https://github.com/voidpro-dev/discord.py-self.git
    $ pip install pyotp
        $ pip install python-dotenv  
```
もし、あなたがこのマークダウンにストレスを感じる場合 requirements.txtを使用可能です。  
```sh
$                                                 pip install -r requirements.txt
```

3 .envファイルにOTPシークレットの追加

4.実行
```sh
$ python main.py
```  
もしくは  
```sh
$ pythonw main.py
```
### Q.PythonとPythonwの違いはなんですか？  
A.Pythonwはバックグラウンドでpythonプロセスを実行するためのツールです。  
Windows上でホストする際におすすめです。  
ただし、BOTを止めるにはタスクキル、Jishaku-Selfによるシャットダウンなどの方法のみとなります

import json
import discord
import random

from lib.numberCount import *
from lib.guessNumber import *
from lib.rank import *
from lib.Minesweeper import *

intents = discord.Intents.default()#練切權限
intents.message_content = True
client = discord.Client(intents=intents)
commendMember = ["siatelin","阿嶳Dylan","SDxBacon"]

#load config
with open("./config.json","r") as f:
    configs = json.load(f)
with open("./servers.json","r") as f:
    servers = json.load(f)

#------------------------------------------------------------------
#起動
@client.event
async def on_ready():
    print('目前登入身份：', client.user)

#啟動抹些東西
numberCounter = numberCount()
GuessNumber = guessNumber()
minesweeper = Minesweeper()
rank = Rank()

#傳送訊息
@client.event
async def on_message(message):
    user = message.author
    userName = message.author.global_name
    content = message.content
    server = message.channel
    serverId = message.channel.id

    if message.author == client.user or message.author.bot:#排除機器人
        return
    
    if serverId == servers["sayYousayServerId"]:#回你訊息
        await message.channel.send(message.author.global_name + " : " + message.content)

    if serverId == servers["firendMainChat"]:                    # 阿嶳457
        emoji = "🫨😭🕛🕚🔲👁️‍🗨️◼️🟤🤣🙂🫥😑😑😑😛🫤🙃🙁☹️😲😔😝😝😝😝😝😝😝😜😜😜😜😛😛😛😣😣😣😥😥😥😑😑😑😑😑😑😑😑😑😐😐😐😫😫😝😜😛🫤🙃🫠☹️🙁"
        await message.add_reaction(emoji[random.randint(0,len(emoji )-1)])

        if "嗨" in message.content or "hi" in message.content or "hello" in message.content:
            a = ["hi","嗨嗨",'hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii',"hihihihihihihihihihi","c9 c9 c9 ","嗨嗨嗨嗨嗨","hello"]       
            await message.channel.send(a[random.randint(0,len(a)-1)])

    if serverId == servers["numberCountServerId"]:#數字接龍
        test = numberCounter.test(message.content)
        if test == 1:
            await message.add_reaction("✅")
        if test == 2:
            await message.channel.send("# 啊?你竟然錯了，這麼簡單的事你也不會?**                                **好吧，只能重來了")
            await message.add_reaction("❌")
            await message.add_reaction("🚫")

            userName = message.author.global_name
            userData = numberCounter.data[message.author.global_name]
            numberCounter.X(userName)
            x = "數錯"+ str(userData[1])+"次"
            v = "數對"+ str(userData[0])+"次"
            a = "正確率" + str(userData[0]/(userData[0]+ userData[1] )*100) +"%"
            await message.channel.send("# "+ userName + x + ","+ v+"," + a)

    if serverId == servers["guessNumber"] : # 猜數字
        if content[0] == "/":
            try:
                text = content.split(",")
                if text[0] == "/start" or text[0] == "/restart": GuessNumber.restart()
                if text[0] == "/save" : GuessNumber.save()
                if text[0] == "/setMaxNumber" : GuessNumber.maxNumber = int(text[1])
                if text[0] == "/setMixNumber" : GuessNumber.mixNumber = int(text[1])
                if text[0] == "/reloadData" : GuessNumber.load()
            except:await server.send("## 指令錯誤!")

        try : 
            number = int(content)
            type = GuessNumber.EnterNumber(number,userName)

            if type == 1: 
                await server.send("# " + str(userName) + "獲勝!")
                await server.send("## 共猜了" + str(GuessNumber.guessCount) + "次")
                GuessNumber.restart()

            if type == 2: await server.send("太大了")
            if type == 3: await server.send("太小了")
            await server.send("## 請猜數字" + str(GuessNumber.guessmix) + "~" + str(GuessNumber.guessmax))

        except : pass

    if serverId == servers["Minesweeper"]:
        AnsType = minesweeper.Enter(userName,content)
        win = minesweeper.testWin()

        if AnsType == "error" :
            await server.send("### 格式出錯")
        if AnsType == "digged":
            await server.send("### 已挖掘")
        if AnsType == "fine": 
            pass
        if win:
            await server.send("# " + userName + "挖除了最後一個方塊，獲勝")
        if AnsType == "lose":
            await server.send("# " + userName + "挖到了地雷，輸了")

        if AnsType == "lose" or win:#詳細數據
            NowData = minesweeper.nowData
            dig = NowData["userDigCounts"]
            flag = NowData["userFlagCounts"]
            unflag = NowData["userUnflagCounts"]

            for i in dig:
                await server.send(i + "已挖掘 : " + str(dig[i]) + " 個方塊")
            for i in flag:
                await server.send(i + "已放置 : " + str(flag[i]) + " 個旗子")
            for i in unflag:
                await server.send(i + "已拆除 : " + str(unflag[i]) + " 個旗子")

            if win: minesweeper.Win(userName)# 重來
            if AnsType == "lose" : minesweeper.lose(userName)

        if AnsType != "talk" :
            minesweeper.saveAll() 
            await server.send( minesweeper.ChangeMapToTextAddEmoji() )
    
    print(message)

#正在輸入訊息
@client.event
async def on_typing(channel, user, when):
    if channel.id == servers["sayYousayServerId"]:#超煩機器人
        await channel.send(user.global_name+ "你到底要說啥拉，塊說~")

client.run(configs["token"])
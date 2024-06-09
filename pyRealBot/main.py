import json
import discord
import random

from lib.numberCount import *
from lib.guessNumber import *
from lib.rank import *
from lib.Minesweeper import *
from lib.ItemAndTrad.item import *

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
Item = item()
rank = Rank(Item.itemdata)


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

    if serverId == servers["EnterCommend"]: #指令輸入
        if content[0] == "/" and userName in commendMember:
            #try:
                text = content.split(",")
                #數字接龍
                if text[0] == "/numberCountAlldata" : await server.send(str( numberCounter.data ))
                if text[0] == "/reloadNumberCountData" : numberCounter.reload()
                #猜數字
                if text[0] == "/startGuessNumber" or text[0] == "/GuessNumberRestart    ": GuessNumber.restart()
                if text[0] == "/saveGuessNumberData" : GuessNumber.save()
                if text[0] == "/setGuessNumberMaxNumber" : GuessNumber.maxNumber = int(text[1])
                if text[0] == "/setGuessNumberMixNumber" : GuessNumber.mixNumber = int(text[1])
                if text[0] == "/reloadGuessNumberData" : GuessNumber.load()
                #踩地雷
                if text[0] == "/reloadMinesweeper": minesweeper.reload()
                if text[0] == "/MinesweeperShowMines": await server.send(minesweeper.ChangeMapToTextAddEmojiShowMines())
            #except:await server.send("## 指令錯誤!")
    
    if serverId == servers["sayYousayServerId"]:#回你訊息
        await message.channel.send(message.author.global_name + " : " + message.content)

    if serverId == servers["firendMainChat"]:                    # 阿嶳457
        emoji = "🫨😭🕛🕚🔲👁️‍🗨️◼️🟤🤣🙂🫥😑😑😑😛🫤🙃🙁☹️😲😔😝😝😝😝😝😝😝😜😜😜😜😛😛😛😣😣😣😥😥😥😑😑😑😑😑😑😑😑😑😐😐😐😫😫😝😜😛🫤🙃🫠☹️🙁"
        await message.add_reaction(emoji[random.randint(0,len(emoji )-1)])

        if "嗨" in message.content or "hi" in message.content or "hello" in message.content:
            a = ["hi","嗨嗨",'hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii',"hihihihihihihihihihi","c9 c9 c9 ","嗨嗨嗨嗨嗨","hello"]       
            await message.channel.send(a[random.randint(0,len(a)-1)])

    if serverId == servers["numberCountServerId"]:#數字接龍
        test = numberCounter.test(userName,message.content)
        if test == 1:
            rankget = rank.numberCountTrue(userName,numberCounter.data[userName])
            await message.add_reaction("✅")
            await server.send(userName + "獲得" + str(rankget[0]) +" rank , " +str(rankget[1]) +" money")
        if test == 2:
            rankget = rank.numberCountFalse(userName,numberCounter.data[userName])
            await message.channel.send("# 啊?你竟然錯了，這麼簡單的事你也不會?**                                **好吧，只能重來了")
            await server.send(userName + "獲得" + str(rankget[0]) +" rank , " +str(rankget[1]) +" money")
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
        try : 
            number = int(content)
            type = GuessNumber.EnterNumber(number,userName)

            if type == 1:
                rankget = rank.GuessNumberTrue(userName,GuessNumber.maxNumber,GuessNumber.guessCount) 
                await server.send("# " + str(userName) + "獲勝!")
                await server.send(userName + "獲得" + str(rankget[0]) +" rank , " +str(rankget[1]) +" money")
                await server.send("## 共猜了" + str(GuessNumber.guessCount) + "次")
                GuessNumber.restart()

            if type == 2: 
                await server.send("太大了")
                rankget = rank.GuessNumberFalse(userName,GuessNumber.nowNumber,GuessNumber.maxNumber,GuessNumber.guessNumber)
                await server.send(userName + "獲得" + str(rankget[0]) +" rank , " +str(rankget[1]) +" money")
            if type == 3: 
                await server.send("太小了")
                rankget = rank.GuessNumberFalse(userName,GuessNumber.nowNumber,GuessNumber.maxNumber,GuessNumber.guessNumber) 
                await server.send(userName + "獲得" + str(rankget[0]) +" rank , " +str(rankget[1]) +" money")
            await server.send("## 請猜數字" + str(GuessNumber.guessmix) + "~" + str(GuessNumber.guessmax))

            GuessNumber.save()
        except : pass

    if serverId == servers["Minesweeper"]:#踩地雷
        try: 
            text = content.split(",")

        except :await server.send("指令錯誤") ; return
        AnsType = minesweeper.Enter(userName,content)
        win = minesweeper.testWin()

        if AnsType == "error" :
            await server.send("### 格式出錯");return
        if AnsType == "digged":
            await server.send("### 已挖掘");return
        if AnsType == "fine": 
            rankget = rank.addScore( minesweeper.rankadd )
            await server.send(userName + "獲得" + str(rankget[0]) +" rank , " +str(rankget[1]) +" money")            
        if win:
            await server.send("# " + userName + "挖除了最後一個方塊，獲勝")
            rankget = rank.addScore( minesweeper.rankadd )
            await server.send(userName + "獲得" + str(rankget[0]) +" rank , " +str(rankget[1]) +" money")
        if AnsType == "lose":
            await server.send("# " + userName + "挖到了地雷，輸了")
            rankget = rank.addScore( minesweeper.rankadd )
            await server.send(userName + "獲得" + str(rankget[0]) +" rank , " +str(rankget[1]) +" money")            

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
    
    if serverId == servers["openBox"] :#商店
        try:
            content = content.split(",")
            if len(content) == 2:
                out = False
                if content[0] == "buy money bonus box":     #開箱
                    out = Item.openBox(userName,"money bonus box", int(content[1]) )
                    rank.addMoneyBonus(userName,Item.itemdata[userName])
                if content[0] == "buy":
                    out = Item.openBox(userName,"box1", int(content[1]) )

                if out:
                    if out[0] == "not find his money":
                        await server.send("你沒錢，去玩遊戲賺錢再來")
                        return 
                    if out[0] == "not find box":
                        await server.send("沒這箱子")
                        return
                    if out[0] == "not enough money":
                        await server.send("你錢不夠")
                    else:
                        #顯示結果
                        await server.send("## " + userName + "獲得:")
                        outItem = out[0]
                        for i in outItem:
                            count = outItem[i]
                            await server.send(i + " : " + str(count) + "個")
                        await server.send("剩下 : " + str(out[2]) + "元")
                else:
                    await server.send("你有地方輸入錯了")

            else:
                await server.send("?");return

        except: await server.send("?");return

    print(message)

#正在輸入訊息
@client.event
async def on_typing(channel, user, when):
    if channel.id == servers["sayYousayServerId"]:#超煩機器人
        await channel.send(user.global_name+ "你到底要說啥拉，塊說~")

client.run(configs["token"])
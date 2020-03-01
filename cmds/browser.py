import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import string

bot = commands.Bot(command_prefix = '!!')

with open('setting.json', mode = 'r', encoding = 'utf8') as setting_file:
    setting_data = json.load(setting_file)


class Browser(Cog_Extension):
    @commands.command()
    async def h(self, ctx, key = ''):
        x = ['**指令列表**', '!!chr `<角色別稱>`  搜尋單一角色（限中文別稱）',
            '!!chr -`<類別><關鍵字>` 列出符合條件的角色清單',
            '> N`<名稱>`  E`<屬性>` R`<範圍>` A`<技能效果>`', '> L1`<作戰>` L2`<異界作戰>` C`<職業>`',
            '> 日文名請用用 -N`<名前>`  進行搜尋',
            '!!h `<類別>`  列出指定類別的所有關鍵字',
            '!!pic `<角色稱號>` `<N/S/H>`  角色 一般圖/大破圖/大頭照']
        if key == 'N':
            await ctx.send('```此類別沒有關鍵字```')
        elif key == 'E':
            await ctx.send('```水 火 風 地 光 暗 對 無```')
        elif key == 'R':
            await ctx.send('```單體 2體 3體 4體 全體 彈性 橫列 縱列 2X2```')
        elif key == 'A':
            y = ['回復 先制 後制 必中 吸血 冰凍 無',
                '暈眩 麻痺 中毒 致盲 燒傷 代價 詛咒',
                '遠程 必中 睡眠 魅惑 蘇生 閃避 絕命',
                '治療效果 時間旅行 時間停止 劍聖霸體',
                '攻擊上升 物攻上升 魔攻上升 物理上升', '攻擊下降 物攻下降 魔攻下降',
                '防禦上升 物防上升 魔防上升 魔法上升', '防禦下降 物防下降 魔防下降',
                '多重增益1 多重增益2 被爆擊傷害減輕']
            y = '\n'.join(y)
            await ctx.send(f'```{y}```')
        elif key == 'L1':
            await ctx.send('```隊長 強敵 雜魚 範圍 回復 遠攻 弱小 元氣 魔法```')
        elif key == 'L2':
            await ctx.send('```攻高 攻低 防高 防低 HP高 HP低 魔法 範圍 回復 素早 遠攻 本體 部位```')
        elif key == 'P':
            z = ['常駐 EX 泳裝1 溫泉1 萬聖1 聖誕1 新春1 學院1 情人1 花嫁1 睡衣1 泳裝2 萬聖2 聖誕2 新春2',
                '大紀行 魔伊 遊戲人生 美好世界 RE:0 工作細胞 煉金工坊']
            z = '\n'.join(z)
            await ctx.send(f'```{z}```')
        elif key == 'C':
            await ctx.send('```劍 侍 弓 槍 戰 補 刺 法```')
        else:
            await ctx.send ('\n'.join(x))

    @commands.command()
    async def chr(self, ctx, name = '', v1 = '', v2 = '', v3 = '', v4 = '', v5 = ''):
        cindex, v = [], []
        file = open('index.txt', mode = 'r', encoding = 'utf8')
        for lines in file.readlines():
            cindex.append(lines.replace('\n', '').split('\\ '))
        file.close()
        anser, display = find_chr(name, cindex, v, v1, v2, v3, v4, v5)

        if anser == []:
            await ctx.send('Character not found.')
            print(v)

        elif len(anser) == 1 or len(anser) == 2 and anser[0][0] == anser[1][0]:
            result = [anser[0][-1][0], anser[0][0].split('.')[0]]  #result[0] = class, result[1] = name
            file_path = './character\\' + str(result[0]) + '\\' + str(result[1]) + '.json'

            with open(file_path, mode = 'r', encoding = 'utf8') as character_file:
                chrdata = json.load(character_file)
            with open('img.json', mode = 'r', encoding = 'utf8') as imglink_file:
                imglink = json.load(imglink_file)
            with open('character link.json', mode = 'r', encoding = 'utf8') as chrlink_file:
                chrlink = json.load(chrlink_file)
            
            embed=discord.Embed(title = chrdata["日文名"], url = chrlink[str(result[1])], description =  chrdata["中文名"])
            embed.set_thumbnail(url = imglink[str(result[1])])
            embed.add_field(name = "作戰", value = chrdata["作戰"], inline = True)
            embed.add_field(name = "卡池", value = chrdata["卡池"], inline = True)
            embed.add_field(name = "特效", value = chrdata["特效"], inline = True)
            embed.add_field(name = "EX特性", value = chrdata["EX特性"], inline = True)
            embed.add_field(name = "插畫", value = chrdata["插畫"], inline = True)
            embed.add_field(name = "聲優", value = chrdata["聲優"], inline = True)
            embed.add_field(name = "ep1", value = chrdata["ep1"], inline = False)
            embed.add_field(name = "ep3", value = chrdata["ep3"], inline = False)
            await ctx.send(embed = embed)

        else:               #   0       1       2       3       4       5       6       7       8
            chr_list = []   #[[名稱], [專武], [屬性], [範圍], [效果], [作戰], [異界], [卡池], [職業]]
            print(anser)
            for characters in anser:    
                temp = [characters[0].split('.')[0], characters[8], characters[1], characters[3]] # 名稱 職業 專武 範圍
                if display[0] == True:
                    temp.append(characters[2])  # 屬性 Optional
                if display[1] == True:
                    temp.append(characters[4])  # 效果 Optional
                if display[2] == True:
                    temp.append(characters[5])  # 作戰 Optional
                if display[3] == True:
                    temp.append(characters[6])  # 異界 Optional
                if display[4] == True:
                    temp.append(characters[7])  # 卡池 Optional
                chr_list.append('  '.join(temp))
            x = '\n'.join(chr_list)
            await ctx.send(f'```{x}```')
            print(v)

    @commands.command()
    async def pic(self, ctx, name, dress = 'n'):
        cindex = []
        file = open('index.txt', mode = 'r', encoding = 'utf8')
        for lines in file.readlines():
            cindex.append(lines.replace('\n', '').split('\\ '))
        file.close()
        
        anser, display = find_chr(name, cindex)
        if anser == []:
            await ctx.send('Character not found.')
        elif len(anser) == 1 or len(anser) == 2 and anser[0][0] == anser[1][0]:
            result = [anser[0][-1][0], anser[0][0].split('.')[0]] #result[0] = class, result[1] = name
            if dress.lower() == 'n':
                await ctx.send(f'Normal {str(result[1])}')
                imgpath = './character\\img\\normal\\' + str(result[1]) + '.png'
                character_img = discord.File(imgpath)
                await ctx.send(file = character_img)
            elif dress.lower() == 's':
                await ctx.send(f'Special {str(result[1])}')
                imgpath = './character\\img\\special\\H' + str(result[1]) + '.png'
                character_img = discord.File(imgpath)
                await ctx.send(file = character_img)
            elif dress.lower() == 'i':
                await ctx.send(f'ID photo {str(result[1])}')
                imgpath = './character\\img\\head\\' + str(result[1]) + '.png'
                character_img = discord.File(imgpath)
                await ctx.send(file = character_img)
            else:
                await ctx.send('```Add n for normal, s for special, and i for ID photo.```')


def setup(bot):
    bot.add_cog(Browser(bot))

def find_chr(name, cindex, v = [], v1 = '', v2 = '', v3 = '', v4 = '', v5 = ''):
    name = str(name)
    result, display = [], [False, False, False, False, False]
    if name.startswith('-'):
        v_list = [name, v1, v2, v3, v4, v5]
        for vs in v_list:
            if vs.startswith('-N'):
                v.append( ['n', vs[2:]] )
            if vs.startswith('-E'):
                v.append( ['e', vs[2:]] )
                display[0] = True
            if vs.startswith('-R'):
                v.append( ['r', vs[2:]] )
            if vs.startswith('-A'):
                v.append( ['a', vs[2:]] )
                display[1] = True
            if vs.startswith('-L1'):
                v.append( ['l1', vs[3:]] )
                display[2] = True
            if vs.startswith('-L2'):
                v.append( ['l2', vs[3:]] )
                display[3] = True
            if vs.startswith('-P'):
                v.append( ['p', vs[2:]] )
                display[4] = True
            if vs.startswith('-C'):
                v.append( ['c', vs[2:]] )
        for keys in v: # v = [[類別, 關鍵字], [類別, 關鍵字]...]
            cindex = list_chr(keys, cindex)
        result = cindex
    else:
        for character in cindex:
            for nickname in character[0].split('.'):
                    if nickname == name:
                        result.append(character)
    return result, display

def list_chr(key, cindex):
    temp = []                   #   n0       1       e2     r3      a4     l1 5    l2 6    p7      c8
    for character in cindex:    #[[名稱], [專武], [屬性], [範圍], [效果], [作戰], [異界], [卡池], [職業]]
        if key[0] == 'n':
            if character[0].find(key[1]) != -1:
                temp.append(character)
        elif key[0] == 'e':  #屬性2
            if character[2].find(key[1]) != -1:
                temp.append(character)
        elif key[0] == 'r':  #範圍3
            if character[3].find(key[1]) != -1:
                temp.append(character)
        elif key[0] == 'a':  #技能效果4
            if character[4].find(key[1]) != -1:
                temp.append(character)
        elif key[0] == 'l1': #作戰5
            if character[5].find(key[1]) != -1:
                temp.append(character)
        elif key[0] == 'l2': #異界6
            if character[6].find(key[1]) != -1:
                temp.append(character)
        elif key[0] == 'p':  #卡池7
            if character[7].find(key[1]) != -1:
                temp.append(character)
        elif key[0] == 'c':  #職業8
            if character[8].find(key[1]) != -1:
                temp.append(character)
    return temp


#大破圖搜尋     V
#關鍵字列表搜尋 V
#使用說明       V
#圖文回覆、添加 X
#外部資料連結   V
#日文名         V
#關鍵字異名導引 X
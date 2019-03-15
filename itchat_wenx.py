# -*- coding:utf-8 -*-

import itchat
import os
import math
import PIL.Image as Image
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud
import jieba
import re


#获取头像
def headImg():
    itchat.login()
    friends = itchat.get_friends(update=True)
    #itchat.get_friends獲取頭像二進制,并写入文件，保存头像
    for count, f in enumerate(friends):
        #根据useerName获取头像
        img = itchat.get_head_img(userName=f["UserName"])
        imgFile = open("img/" + str(count) + ".jpg", "wb+")
        imgFile.write(img)
        imgFile.close()


#头像拼图
def createImg():
    x = 0
    y = 0
    imgs = os.listdir("img")
    random.shuffle(imgs)
    #创建拼图的图片大小
    newImg = Image.new('RGBA', (720, 720))
    #以720*720来拼图。 math.sqrt()来开平方计算小图的宽和高
    width = int(math.sqrt(720 * 720 /len(imgs)))
    #每行图片数
    numLine = int(720/ width)

    for i in imgs:
        try:
            img = Image.open("img/" + i)
            #缩小图片
            img = img.resize((width, width), Image.ANTIALIAS)
            #拼接图片
            newImg.paste(img, (x * width, y* width))
            x +=1
            if x >= numLine:
                x = 0 
                y += 1
        except IOError:
            print("img/ %s can not open"%(i))

    newImg.save("all.png")



#性别统计
def getSex():
    itchat.login()
    friends = itchat.get_friends(update=True)
    sex = dict()
    for f in friends:
        if f["Sex"] == 1: #男
            sex["man"] = sex.get("man", 0) + 1
            # try:
                
            # except KeyError:
            #     import ipdb; ipdb.set_trace()
            #     pass
        elif f["Sex"] == 2: #女
            sex["women"] = sex.get("women", 0) + 1
        else: #未知
            sex["unknown"] = sex.get("unknown", 0) + 1

        #柱状图展示
        for i, key in enumerate(sex):
            plt.bar(key, sex[key])
        plt.savefig("getSex.png") #保存图片
        plt.ion()
        plt.pause(5)
        plt.close() #图片显示5s, 之后关闭
        #plt.show() #不建议用show， show是堵塞式
        

#获取个性签名
def getSignature():
    itchat.login()
    friends = itchat.get_friends(update=True)
    file = open('sign.txt', 'a', encoding = 'utf-8')
    for f in friends:
        signature = f["Signature"].strip().replace("emoji", "").replace("span", "").replace("class", "")
        print(signature, type(signature))
        rec = re.compile("1f\d+w*|[<>/=]")
        signature = rec.sub("", signature)
        file.write(signature + "\n")


#生成词云
def create_word_cloud(filename):
    #读取文件内容
    text = open("{}.txt".format(filename), encoding='utf-8').read()

    # 注释部分采用结巴分词
    wordlist = jieba.cut(text, cut_all=True)
    wl = " ".join(wordlist)
    

    #设置词云
    wc = WordCloud(
        #设置背景颜色
        background_color = "white",
        #设置最大显示的词云数
        max_words = 2000,
        #设置字体
        font_path='C:\\Windows\\Fonts\\simfang.ttf',
        height = 500,
        width = 500,
        #设置字体最大值
        max_font_size = 60,
        #设置随机生成状态，既有多少种配色
        random_state =30,

        )
    
    myword = wc.generate(wl) #生成词云，如果用结巴分词的话，使用wl 取代 text， 生成词云图
    # 展示词云图
    plt.imshow(myword)
    plt.axis("off")
    plt.show()
    wc.to_file('signature.png')  # 把词云保存下


# if __name__ == '__main__':
# 微信好友头像拼接
headImg()
createImg()
# 性别统计
getSex()

# 个性签名统计

getSignature()
create_word_cloud("sign")
import requests
from wxpy import *
from threading import Timer

#用于登录和操作微信
bot = Bot(cache_path=True)


#获取语句
def get_msg():
    #给出api地址
    url = 'http://open.iciba.com/dsapi/'
    html = requests.get(url)
    #获取每一日英文语句
    content = html.json()['content']
    #获取每一日英文的翻译
    note = html.json()['note']
    return content , note

#发送语句
def send_msg():
    try:
        msgs = get_msg()
        content = msgs[0]
        note = msgs[1]
        #设置要发送信息人的昵称
        my_friend = bot.friends().search(u'对方昵称')[0]
        #向他发送英文语句
        my_friend.send(content)
        #向他发送翻译的语句
        my_friend.send(note)
        #设置发送的时间间隔
        t = Timer(10, send_msg())
        t.start()

    except BaseException:
        #如果发送不成功就把消息发给自己，
        my_friend = bot.friends().search(u'自己的昵称')[0]
        my_friend.send(u'消息发送失败')


if __name__ == '__main__':
    send_msg()
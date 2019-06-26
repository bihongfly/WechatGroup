# coding:utf8
import os
import sys
import ConfigParser
reload(sys)
sys.setdefaultencoding( "utf8" ) 
import itchat
from itchat.content import *


cf = ConfigParser.ConfigParser()
cf.read('wechat.ini')
src_room=cf.get('rooms','src_room')
dest_room=cf.get('rooms','dest_room')

def get_group(room):
    rooms = itchat.get_chatrooms(update=True,contactOnly=True)
    for i in rooms:
        if i["NickName"] == room:
            return i["UserName"]    


@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def forward_text(msg):
    now_roomid = msg['FromUserName']    
    if now_roomid == get_group(src_room):
        user_name = msg['ActualNickName']
        if msg['Type'] == TEXT:
            content = msg['Content']
            itchat.send('%s（%s）:\n\n%s' % (user_name,src_room,content),get_group(dest_room) )
        elif msg['Type'] == SHARING:
            content = msg['Text']
            url = msg["Url"]
            itchat.send('%s（%s）:\n%s\n%s' % (user_name,src_room,content, url), get_group(dest_room))
         
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def forward_media(msg):
    now_roomid = msg['FromUserName']
    if now_roomid == get_group(src_room):
        user_name = msg['ActualNickName']
        media_name = msg['FileName']
        if media_name[-4:] == '.gif':
            return
        else:
            msg['Text'](media_name)
            typeSymbol = {PICTURE: 'img',VIDEO: 'vid', }.get(msg['Type'], 'fil')
            itchat.send('@%s@%s' % (typeSymbol, media_name),get_group(dest_room))
            # itchat.send('@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'fil', msg['FileName']),get_group(dest_room))
            os.remove(media_name)

itchat.auto_login(hotReload=True,enableCmdQR=2)
itchat.run()

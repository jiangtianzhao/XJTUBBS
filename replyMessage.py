#-*-coding:utf-8-*-
#Filename:replyMessage.py
#--------------------
#Function description:
#自动将文件中内容回复到西交BBS指定模块主题
#--------------------
#Autnor:Jiang Tianzhao
#QQ:1435207832
#--------------------
#Date:2016-9-25
#--------------------
#导入必要模块
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re

#获取文件信息
def getMessage(pathName):
    f=open(pathName,'r')
    messages=f.readlines()
    data=[]
    for i in range(len(messages)):
        data.append(messages[i][3:len(messages[i])-1])
    return data  
#发帖
class replyMsg:
    #获取初始数据
    def __init__(self,baseurl,account,password,module):
        self.baseurl=baseurl
        self.account=account
        self.password=password
        self.module=module
    #自动登录系统,获取URL地址
    def login(self):
        payload = {'id':self.account, 'pw':self.password}
        urlLogin=self.baseurl+'BMY/bbslogin'
        reponseLogin=requests.post(urlLogin,data=payload)
        reponse=reponseLogin.text
        startLogin=reponse.find("url")
        endLogin=reponse.find("/'>")
        urlResult=reponse[startLogin+4:endLogin+1]
        if not urlResult.strip():
            print("账号或密码错误")
            return None
        else:
            return urlResult
    #查找回帖地址
    def getReplyUrl(self,postData):
        urlPost=self.baseurl+self.login()+'bbsbfind?type=1'
        reponsePost=requests.post(urlPost,postData)
        a=reponsePost.text
        start_num1=a.find("F=M.")
        end_num1=a.find("A&N=")
        end_num2=a.find("&T=")
        num1=a[start_num1+4:end_num1-1]
        num2=a[end_num1+4:end_num2]
        url='http://bbs.xjtu.edu.cn/BMYAAFDCRUVHIDLPTUKKGNHSHLPJEBNKTYBM_B/bbssnd?board=XJTUnews&th='+num1+'&ref=M.'+num1+'.A&rid='+num2
        return url
    #上传回复内容
    def reply(self,body,replyData):
        reponseReply=requests.post(self.getReplyUrl(body),replyData)
        
#获取文件信息
pathText='Reply.txt'
message=getMessage(pathText)    
baseurl='http://bbs.xjtu.edu.cn/'
#获取发帖类
replyMessage=replyMsg(baseurl,message[0],message[1],message[2])
#回帖内容
body={"board":message[2],"title":message[3],"userid":message[4],"dt":message[5]}
#回帖
Reply_data={"title":"Re: "+message[3],"text":message[6].encode('gbk')}
replyMessage.reply(body,Reply_data)











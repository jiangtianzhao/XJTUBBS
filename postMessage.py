#-*-coding:utf-8-*-
#Filename:postMessage.py
#--------------------
#Function description:
#自动将文件中内容发送到西交BBS指定模块
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
class postMsg:
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
    #自动发帖
    def postAuto(self,postData):
        urlPost=self.baseurl+self.login()+'bbssnd?board='+self.module+'&th=-1'
        reponsePost=requests.post(urlPost,postData)
#获取文件信息
pathText='Post.txt'
message=getMessage(pathText)    
baseurl='http://bbs.xjtu.edu.cn/'
#获取发帖类
postMessage=postMsg(baseurl,message[0],message[1],message[2])
#发帖内容
body={"title":message[3].encode('gbk'),"text":message[4].encode('gbk')}
#发帖
postMessage.postAuto(body)










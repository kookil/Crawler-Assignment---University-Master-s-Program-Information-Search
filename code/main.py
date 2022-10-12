# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 11:37:26 2020

@author: kookil
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import urllib3
urllib3.disable_warnings()

def getHTMLText(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
        h=requests.get(url,headers=headers,verify=False)
        h.raise_for_status()
        h.encoding="gbk"
        return h.text 
    
    except:
        return ""


def save_info(dic):
    with open("ECNU.txt","w",encoding="gbk") as f :
        f.write(json.dumps(dic))
        
def get_info():
    url="https://yjszs.ecnu.edu.cn/system/sszszyml_list.asp"
    s=getHTMLText(url)
    soup=BeautifulSoup(s,'lxml')
    x=soup.find_all('a')
    dic={}
    for c in x:
        tit=c.text
        tittle=re.sub(u"\\(.*?\\)", "", tit)
        web="https://yjszs.ecnu.edu.cn/system/"+c["href"]   
        web_s=getHTMLText(web)
    #print(web_s)
        dic.setdefault(tittle,[]).append(c["href"])
    #print(dic)
        if tittle[-1]=='系':
            dic.setdefault(tittle,[]).append('详细请点击网络链接')

        else:
            soup2=BeautifulSoup(web_s,'lxml')
            x2=soup2.find_all('tr', align='left', valign='middle')
            for c2 in x2:
                tit2=c2.find_all('td')[4].text.strip()
                dic.setdefault(tittle,[]).append(tit2)
    save_info(dic)
    return dic



def main():
    while True:
        n=input('请输入你想查找的系/专业：')
        info=get_info()
        print("你所查询的"+n+"网址为https://yjszs.ecnu.edu.cn/system/"+info[n][0]+"。"+"录取情况为"+info[n][1])            
        
    
main()
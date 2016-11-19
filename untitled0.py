# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 14:12:37 2016

@author: yangz
"""
#!/usr/bin/python
#-*- coding:utf-8 -*-
import re
import requests
import sys
import urllib
import time
import socket
import os
os.chdir('C:\Users\yangz\Desktop\pacong')
reload(sys)
sys.setdefaultencoding("utf-8")
def html_page(url):
    r = requests.get(url)
    data = r.text
    link_list =re.findall(r"(?<=href=\"bencandy.asp).+?(?=\")|(?<=href=\'bencandy.asp).+?(?=\')",data)
    return link_list
#link_list_title=[]
#link_list_title =re.findall(r'title=(.*)',data)
def html_re(url,i,sleep_download_time,timeout):
    U=[]
    try:
        time.sleep(sleep_download_time)
        socket.setdefaulttimeout(timeout)
        user_agent = 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0'
        headers = {'User-Agent' : user_agent,'Referer':url+'/'}
        r = requests.get(url,headers=headers)
        data = r.text
        r.close()
        link_name =re.findall(r'<title>(.*?)</title>',data)
        if len(link_name)==0:
            d=url[-4:]
        else:
            d=link_name[0]
        pic_url_modify=[]
        pic_floder=[]
        pic_url=re.findall('src="(.*?)"',data,re.S)
        for pic in pic_url:
            if pic.find('http://')==-1:
                if pic.find('images/')==-1:
                    if pic.find('/admin/up_img/image/')>-1:
                        i=i+1
                        pic_url_modify.append('http://www.hzmb.org/'+pic)
                        pic_floder.append('admin/up_img/image/'+str(i)+pic[-4:])
                        data=data.replace(pic,pic_floder[-1])                    
                        f=file(pic_floder[-1],'w')
                        urllib.urlretrieve(pic_url_modify[-1],pic_floder[-1])
                        f.close()
                else:
                    pic_url_modify.append('http://www.hzmb.org/cn/'+pic)
                    f=file(pic,'w')
                    urllib.urlretrieve(pic_url_modify[-1],pic)
                    f.close() 
        f=file(d+'.html','w')
        for line in data:
            f.write(line)
        f.close()
    except requests.RequestException as e:
        print(e)
        U=url
    except requests.exceptions.ConnectionError as e:
        print(e)
        U=url
    except UnicodeDecodeError as e:
        print('-----UnicodeDecodeErrorurl:',url)
        U=url
    except socket.timeout as e:
        print("-----socket timout:",url)
        U=url
    except IOError as e:
        print("download ",url,"\nerror:",e)
        U=url
    return i,U
def main_support(i,j,link_list,sleep_download_time,timeout):
    link_defeat_list=[]
    n=j
    for url in link_list[n:]:
        [i,U]=html_re(url,i,sleep_download_time,timeout)
        j=j+1
        if len(U)>0:
            link_defeat_list.append(U)
            f=open('link_defeat_list.txt','a')
            f.write(U+'\n')
            f.close()
        print '第'+str(j)+'个网页'
    return i,j,link_defeat_list
url_all=[]
link_list=[]
link=[]      
for i in range(1,34):
    if i==1:
        url_all.append('http://www.hzmb.org/cn/list.asp?id=13')
    else:
        url_all.append('http://www.hzmb.org/cn/list.asp?id=13'+'&page='+str(i))
for url_a in url_all:
    link_list.extend(html_page(url_a))
for url in link_list:
    if len(url)==8:
        url='http://www.hzmb.org/cn/bencandy.asp'+url
        link.append(url)
i=1000
timeout = 20
sleep_download_time=2
link_defeat_list=[]
j=0
[i,j,link_defeat_list]=main_support(i,j,link_defeat_list,sleep_download_time,timeout)
            

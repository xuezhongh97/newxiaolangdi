import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import calendar
import time
import xlrd
import math
import cv2 as cv
import matplotlib.image as mpimg # mpimg 用于读取图片
import random as rd
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, time






def read_excel(excel_path, sheet_no = 0):
    book = xlrd.open_workbook(excel_path)
    sheet = book.sheet_by_index(sheet_no)
    return np.array([list(map(lambda x : x.value, sheet.row(i))) for i in range(sheet.nrows)])

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def remove_by_indices(iter, idxs):
    return [e for i, e in enumerate(iter) if i not in idxs]

fast_normal_timetable1=[]
for i in range(5*60,24*60,6):
    fast_normal_timetable1.append(i)
for i in range(7*60+3,9*60,6):
    fast_normal_timetable1.append(i)
for i in range(17*60+3,20*60,6):
    fast_normal_timetable1.append(i)
for i in range(0*60,5*60,30):
    fast_normal_timetable1.append(i)
fast_normal_timetable = []
for i in fast_normal_timetable1:
    fast_normal_timetable.append(i)
    fast_normal_timetable.append(i+1440)
fast_normal_timetable.sort()


main_normal_timetable1=[]
for i in range(5*60,24*60,12):
    main_normal_timetable1.append(i)
for i in range(7*60+6,9*60,12):
    main_normal_timetable1.append(i)
for i in range(17*60+6,20*60,12):
    main_normal_timetable1.append(i)
main_normal_timetable = []
for i in main_normal_timetable1:
    main_normal_timetable.append(i)
    main_normal_timetable.append(i+1440)
main_normal_timetable.sort()



slow_normal_timetable1=[]
for i in range(5*60,24*60,24):
    slow_normal_timetable1.append(i)
for i in range(7*60+12,9*60,24):
    slow_normal_timetable1.append(i)
for i in range(17*60+12,20*60,24):
    slow_normal_timetable1.append(i)
slow_normal_timetable = []
for i in slow_normal_timetable1:
    slow_normal_timetable.append(i)
    slow_normal_timetable.append(i+1440)
slow_normal_timetable.sort()


list_station=[]
list_line=[]

class busline:
    def __init__(self,numero,starttime=5,endtime=22,proprity=1,time=1,price=1,timetable1=slow_normal_timetable,timetable2=slow_normal_timetable):
        self.__numero=numero
        self.__starttime=starttime
        self.__endtime=endtime
        self.__proprity=proprity
        self.__station=[]
        self.__price=price
        self.__time=time
        self.__timetable1=timetable1
        self.__timetable2=timetable2
        self.__interval=[]
        
        
    def get_numero(self):
        return self.__numero
    
    def get_station(self):
        return self.__station
    
    def get_proprity(self):
        return self.__proprity
    
    def get_price(self):
        return self.__price
    
    def get_linecolor(self):
        return self.__linecolor

    def get_stationcolor(self):
        return self.__stationcolor

    def get_time(self):
        return self.__time

    def get_linecolor(self):
        return self.__linecolor

    def add_linecolor(self,linecolor):
        self.__linecolor=linecolor
    
    def add_station(self,station):
        self.__station=station
        for i in station:
            flag=0
            for j in list_station:
                if j.get_name()==i:
                    j.add_line(self.get_numero())
                    flag=1
            if flag==0: list_station.append(Station(i,self.get_numero()))
            
    def add_interval(self,interval):
        self.__interval=interval

    def get_interval(self):
        return self.__interval
            
    def get_info(self):
        if self.__station[0]=="外环" or self.__station[0]=="内环":
            print(color.RED + self.get_numero() + color.END ," ",color.YELLOW+self.__station[1]+color.END," 环线")
        else:
            print(color.RED+str(self.get_numero())+color.END," ",color.YELLOW+self.__station[0]+color.END,color.YELLOW+"<--->"+color.END,color.YELLOW+self.__station[-1]+color.END,"\n")
        if self.__proprity==0:
            print("小浪底大众运输公司运营")
            print("监督电话030-41224100")
        elif self.__proprity==1:
            print("小浪底白鹿原通勤公司运营") 
            print("监督电话030-41224200")
           
        elif self.__proprity==2:
            print("小浪底北郊大众运输专门组织运营")
            print("监督电话030-41224105")
        else:
            print("小浪底南郊大众运输专门组织运营")
            print("监督电话030-45882155")           
        print("首班车",self.__starttime,"点")
        print("末班车",self.__endtime,"点","\n")
        print(color.BOLD+"站点\n"+color.END)
        connectiontemp2=0
        for m in self.__station:
            for n in list_station:
                if m==n.get_name():
                    if connectiontemp2==1:
                        pass#print("|")                        
                    print(zonebar[n.get_zone()],"\t",int(self.get_interval()[self.__station.index(m)]),"\t","+",m)
                    connectiontemp2=1
        self.affichage_timetable()
    
    def get_starttime(self):
        return self.__starttime
    
    def get_endtime(self):
        return self.__endtime
    
    def affichage_timetable(self):
        print(color.BOLD+"\n上行发车时刻表"+color.END)
        hourtemp=-1
        issunday = 0
        if issunday==1:
            for i in self.__timetable2:
                if i//60!=hourtemp:
                    print("\n","%02d"%(i//60),"\t",end="")
                print("%02d"%(i%60),end=" ")
                hourtemp=i//60
        else:
            for i in self.__timetable1:
                if i//60!=hourtemp:
                    print("\n","%02d"%(i//60),"\t",end="")
                print("%02d"%(i%60),end=" ")
                hourtemp=i//60
    
    def get_timetable(self):
        if issunday==1:
            return self.__timetable2
        else:
            return self.__timetable1

class Station:
    def __init__(self,name,line,zone=1):
        self.__name=name
        self.__line=[]
        self.__line.append(line)
        self.__neighborhood=[]
        self.__timetable=[]
        self.__position=[1,1,1,1]
        self.__zone=zone
        self.__shortname=[]
    def get_name(self):
        return self.__name
        
    def add_line(self,line):
        self.__line.append(line)
    
    def get_line(self):
        return self.__line

    def get_zone(self):
        return self.__zone


    def get_position(self):
        return self.__position

    def add_position(self,position,zone):
        self.__position=position
        self.__zone=zone
        
    def get_shortname(self):
        return self.__shortname
    
    def add_shortname(self,shortname):
        self.__shortname=shortname
    
    def get_info(self):
        print(self.get_name())
        #print(self.get_zone(),"区车站")
        print("停靠巴士")
        print(self.get_line())
        self.get_timetable()
        
    def initialiser(self):
        for i in self.__line:
            for j in list_line:
                if i==j.get_numero():
                    liste_de_line=j.get_station()
                    for k in liste_de_line:
                        if k!=self.get_name():
                            self.__neighborhood.append((k,abs(j.get_interval()[liste_de_line.index(k)]-j.get_interval()[liste_de_line.index(self.get_name())]),j.get_numero()))
        self.__neighborhoodsorted=sorted(self.__neighborhood, key=lambda s: s[-1])
        for i in self.__line:
            for j in list_line:
                if i==j.get_numero():
                    direction=j.get_station()[0]
                    delay=j.get_interval()[-1]-j.get_interval()[j.get_station().index(self.get_name())]
                    timetableexact=[]
                    for i in j.get_timetable():
                        timetableexact.append(i+delay)
                    self.__timetable.append((j.get_numero(),direction,timetableexact))
                    direction=j.get_station()[-1]
                    delay=j.get_interval()[j.get_station().index(self.get_name())]
                    timetableexact=[]
                    for i in j.get_timetable():
                        timetableexact.append(i+delay)
                    self.__timetable.append((j.get_numero(),direction,timetableexact))
  
    def get_neighbor(self):
        return self.__neighborhoodsorted
    def get_timetable(self):
        for i in self.__timetable:
            waiting_time = []
            for j in i[2]:      
                time_rest=j-timenow  
                if j>timenow:
                    waiting_time.append(time_rest)
                    if len(waiting_time)>2:
                        break
            if time_rest<0:
                print(i[0]," ",i[1]," ","停止运营")
            else:
                print(i[0]," ",i[1]," \t +",end= " ")
                for k in waiting_time:
                    print(int(k),end=" ") 
                print("")
    def give_timetable(self):
        return self.__timetable



#now = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))

# 判断今天是否为周末
def is_week_lastday():
    # 假如今天是周日
    sunday = now.weekday()
    # 如果今天是周日，则返回True
    if sunday == 6:
        return True
    else:
        pass


    
def searchline():
    try:
        line=int(input("线路号\n"))
    except ValueError:
        print("")
    os.system("clear")    
    for i in list_line:
        if line==i.get_numero():
            i.get_info()
                
        
def searchstation():
    station=input("站点名\n输入汉语全称或者拼音首字母\n")
    os.system("clear")
    for i in list_station:
        if station==i.get_name():
            i.get_info()

def drawline(station1,station2,line):
    global linemap
    for i in list_station:
        if station1==i.get_name():
            Station1=i
    for i in list_station:
        if station2==i.get_name():
            Station2=i
    n1,y1,x1,z1=Station1.get_position()
    n2,y2,x2,z1=Station2.get_position()
    mainline=[1,3,4,6,8,11,12]
    if line.get_numero() in mainline:
        width=5
    else:
        width=3
    cv.line(linemap, (y1, x1), (y2, x2), (line.get_linecolor()[2],line.get_linecolor()[1],line.get_linecolor()[0]), width) #9
    

def drawpoint(station,line,isblackened):
    global linemap
    if isblackened==1:
        sizefont=20
        radius=6
        thickness=3
    else:
        sizefont=10
        radius=4
        thickness=2
    for i in list_station:
        if station==i.get_name():
            Station=i
    n1,y1,x1,z1=Station.get_position()
    cv.circle(linemap, (y1,x1), radius, colorbar[Station.get_zone()-1], thickness) #33
    img_PIL = Image.fromarray(cv.cvtColor(linemap, cv.COLOR_BGR2RGB))
    font = ImageFont.truetype('wqy-microhei.ttc', sizefont)
    position = (y1+10,x1-5)
    str = Station.get_name()
    draw = ImageDraw.Draw(img_PIL)
    draw.text(position, str, font=font,  fill=(255,255,255))
    linemap = cv.cvtColor(np.asarray(img_PIL),cv.COLOR_RGB2BGR)

def drawnumber(station,line):
    global linemap
    for i in list_station:
        if station==i.get_name():
            Station=i
    n1,y1,x1,z1=Station.get_position()
    img_PIL = Image.fromarray(cv.cvtColor(linemap, cv.COLOR_BGR2RGB))
    sizefont=30
    font = ImageFont.truetype('wqy-microhei.ttc', sizefont)
    fillColor = line.get_linecolor()
    position = (y1-40,x1-20)
    str1 = str(line.get_numero())
    draw = ImageDraw.Draw(img_PIL)
    draw.text(position, str1, font=font,  fill=fillColor)
    linemap = cv.cvtColor(np.asarray(img_PIL),cv.COLOR_RGB2BGR)
   
    
def searchroute(startstation,endstation,line,timenow1,ticketflag):
    stations=[]
    for i in list_station:
        if startstation==i.get_name():
            stationstarted=i
        if endstation==i.get_name():
            stationended=i
    mintime=3000
    for j in list_line:
        if line==j.get_numero():
            linetemp=j
            found=0
            circle=0
            if linetemp.get_station()[1]==linetemp.get_station()[-1]:
                circle=1
            for k in linetemp.get_station():
                if k==stationstarted.get_name():
                    stationnum1=linetemp.get_station().index(k)
                if k==stationended.get_name():
                    stationnum2=linetemp.get_station().index(k)
                    found=1                
            if found==1:
                if stationnum1<=stationnum2:
                    direction=linetemp.get_station()[-1]
                else:
                    direction=linetemp.get_station()[0]
                if circle:
                    if stationnum1==1:
                        if abs(stationnum2-1)>abs(len(linetemp.get_station())-stationnum2):
                            direction=linetemp.get_station()[-1]
                            stationnum1=len(linetemp.get_station())-1
                        else:
                            direction=linetemp.get_station()[0]
                    if stationnum2==1:
                        if abs(stationnum1-1)>abs(len(linetemp.get_station())-stationnum1):
                            direction=linetemp.get_station()[-1]
                            stationnum2=len(linetemp.get_station())-1
                        else:
                            direction=linetemp.get_station()[0]

                timetable=stationstarted.give_timetable() 
                for i in timetable:
                    if i[0]==linetemp.get_numero() and i[1]==direction:
                        for m in i[-1]:
                            time_rest=m-timenow1
                            if time_rest>=0:
                                break
                if time_rest>=0 and time_rest<=600:
                    if stationnum1<=stationnum2:
                        for j in range(stationnum1,stationnum2+1):
                            for l in list_station:
                                if linetemp.get_station()[j]==l.get_name():
                                    stations.append(l.get_name())
                                    ticketflag.append(l.get_zone())
                    else:
                        for j in range(stationnum1,stationnum2-1,-1):
                            for l in list_station:
                                if linetemp.get_station()[j]==l.get_name():
                                    stations.append(l.get_name())                                   
                                    ticketflag.append(l.get_zone())
                    mintime=min(mintime,abs(stationnum1-stationnum2)*linetemp.get_time()+time_rest+timenow1)
                else:
                    print("车辆停止运营")
                    return 0
                return (startstation,endstation,timenow1,time_rest,timenow1+time_rest,stations,abs(linetemp.get_interval()[stationnum1]-linetemp.get_interval()[stationnum2])+time_rest+timenow1,line,direction,ticketflag)
    return 0
            
def search1(stationstarted,stationended,route):
    goal=stationended.get_name()
    for i in stationstarted.get_neighbor():
        if i[0]==goal:
            poids=i[1]
            route.append((1,i[2],poids))
    return route
                

def search2(stationstarted,stationended,route):
    goal=stationended.get_name()
    for i in stationstarted.get_neighbor():
        for j in list_station:
            if i[0]==j.get_name():
                for k in j.get_neighbor():
                    if k[0]==goal:
                        poids=i[1]+k[1]+15
                        route.append((2,i[2],i[0],k[2],poids))
                        
    return route

def search3(stationstarted,stationended,route):
    goal=stationended.get_name()
    for i in stationstarted.get_neighbor():
        for j in list_station:
            if i[0]==j.get_name():
                for k in j.get_neighbor():
                    for l in list_station:
                        if k[0]==l.get_name():
                            for m in l.get_neighbor():
                                if m[0]==goal:
                                    poids=i[1]+k[1]+m[1]+30
                                    route.append((3,i[2],i[0],k[2],k[0],m[2],poids))
                        
    return route

def search4(stationstarted,stationended,route):
    goal=stationended.get_name()
    for i in stationstarted.get_neighbor():
        for j in list_station:
            if i[0]==j.get_name():
                for k in j.get_neighbor():
                    for l in list_station:
                        if k[0]==l.get_name():
                            for m in l.get_neighbor():
                                for n in list_station:
                                    if m[0]==n.get_name():
                                        for p in n.get_neighbor():
                                            if p[0]==goal:
                                                poids=i[1]+k[1]+m[1]+p[1]+45
                                                route.append((4,i[2],i[0],k[2],k[0],m[2],m[0],p[2],poids))
                                        
    return route
  

def achat():
    global charge
    try:
        zonenumber=int(input("请输入乘坐区号\n"))
    except ValueError:
        print("")    
    os.system("clear")    
    for i in prince_list:
        if i[0]==zonenumber:
            try:
                print("优惠类型？\n")
                print(color.UNDERLINE+"1 市民"+color.END,end="\t")
                print(color.UNDERLINE+"2 学生"+color.END,end="\t")
                print(color.UNDERLINE+"3 老人"+color.END,end="\t")
                print(color.UNDERLINE+"4 游客"+color.END,end="\t")
                print(color.UNDERLINE+"5 无优惠"+color.END,end="\n")
                reducedtype=int(input(""))
            except ValueError:
                print("")                
            reduced=1
            if reducedtype==1:
                reduced=0.8
            if reducedtype==2:
                reduced=0.3
            if reducedtype==3:
                reduced=0.5
            if reducedtype==4:
                reduced=0.9
            newprice=i[1]*reduced
            print("票价为",round(newprice,1),"元")
            try:
                print("是否支付\n")
                print(color.UNDERLINE+"0 取消"+color.END,end="\t")
                print(color.UNDERLINE+"1 确认"+color.END,end="\n")
                ispayed=int(input(""))
            except ValueError:
                print("")
            os.system("clear")
            if ispayed and charge>=round(newprice,1):
                charge-=round(newprice,1)
                print("支付成功，以下为确认码")
                identi=rd.randint(1000000000000,10000000000000)                
                print(identi)
                identity.append(identi)
                return
            else:
                print("支付失败")
                return
    print("信息输入错误")
    return

def acount():
    global charge
    os.system("clear")
    print("账户信息")
    print("余额:",round(charge,1),"元")
    if len(identity)>0:
        print("已购买车票验证码")
        for i in identity:
            print(i)
    else:
        print("无车票验证码")
    return



    

def UIdisplay(results):
    global linemap
    for i in list_station:
        if results[0]==i.get_name():
            stationstarted=i
        if results[1]==i.get_name():
            stationended=i
    for k in list_line:
        if k.get_numero()==results[7]:
            linetemp=k
    print(color.RED+str(results[7])+color.END,"\t",color.YELLOW+results[-2]+color.END)
    print(color.BLUE+stationstarted.get_name()+color.END,color.BLUE+"---->"+color.END,color.BLUE+stationended.get_name()+color.END)
    print("%02d"%int(results[4]//60),":","%02d"%int(results[4]%60),"---->","%02d"%int(results[6]//60),":","%02d"%int(results[6]%60))
    print("+",int(results[3]))
    print("")
    isconnected=0
    drawnumber(results[5][0],linetemp)
    for j in results[5]:
        for m in list_station:
            if j==m.get_name():

                delaytemp=abs(linetemp.get_interval()[linetemp.get_station().index(m.get_name())]-linetemp.get_interval()[linetemp.get_station().index(stationstarted.get_name())])
                print(zonebar[m.get_zone()],"\t","%02d"%int((results[4]+delaytemp)//60),":","%02d"%int((results[4]+delaytemp)%60),"\t ",j)
    for j in range(len(results[5])-1):
        drawline(results[5][j],results[5][j+1],linetemp)
                
    for j in range(len(results[5])-1):
        if j==len(results[5])-2:
            drawpoint(results[5][j+1],linetemp,1)
        else:
            drawpoint(results[5][j+1],linetemp,0)            
            
    print("")

def UIdisplay_streamlit(results, output_str):
    for i in list_station:
        if results[0]==i.get_name():
            stationstarted=i
        if results[1]==i.get_name():
            stationended=i
    for k in list_line:
        if k.get_numero()==results[7]:
            linetemp=k   
    #output_str += f'<span style="font-size:24px; font-weight:bold;">{str(results[7])}</span>'
    output_str += '<span style="font-size:24px; font-weight:bold;">'+str(results[7])+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+results[-2]+"</span>  \n"
    if results[4] > 1440:
        results4 = results[4] - 1440
    else:
        results4 = results[4]
    if results[6] > 1440:
        results6 = results[6] - 1440
    else:
        results6 = results[6]
    output_str += '<span style="font-size:18px; font-weight:bold;">'+stationstarted.get_name()+"%02d"%int(results4//60)+":"+"%02d"%int(results4%60)+'&nbsp;→&nbsp;'+stationended.get_name()+"%02d"%int(results6//60)+":"+"%02d"%int(results6%60)+"</span>  \n"
#    output_str += '<span style="font-size:16px; font-weight:bold;">'+"%02d"%int(results[4]//60)+":"+"%02d"%int(results[4]%60)+"&nbsp;→&nbsp;"+"%02d"%int(results[6]//60)+":"+"%02d"%int(results[6]%60)+"</span>  \n"
    output_str += '<span style="font-size:12px; font-weight:bold;">'+"等待约"+str(int(results[3]))+"分钟</span>  \n"
    for j in results[5]:
        for m in list_station:
            if j==m.get_name():
                delaytemp=abs(linetemp.get_interval()[linetemp.get_station().index(m.get_name())]-linetemp.get_interval()[linetemp.get_station().index(stationstarted.get_name())])
                #print(zonebar[m.get_zone()],"\t","%02d"%int((results[4]+delaytemp)//60),":","%02d"%int((results[4]+delaytemp)%60),"\t ",j)
                if results4+delaytemp > 1440:
                    results4 -= 1440
                output_str += "%02d"%int((results4+delaytemp)//60)+":"+"%02d"%int((results4+delaytemp)%60)+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+j+"  \n"
    output_str += "  \n"
    return output_str

    
def displayresults(route,startstation,endstation,ticketflag):
    global linemap
    print(color.BOLD+startstation+color.END,color.BOLD+"---->"+color.END,color.BOLD+endstation+color.END,"\n")
    if route[0]==1:
        for i in list_line:
            if route[1]==i.get_numero():
                drawpoint(startstation,i,1)
        results=searchroute(startstation,endstation,route[1],timenow,ticketflag)
        if results:
            UIdisplay(results)
        else:
            return 0
    if route[0]==2:
        for i in list_line:
            if route[1]==i.get_numero():
                drawpoint(startstation,i,1)
        results=searchroute(startstation,route[2],route[1],timenow,ticketflag)
        if results: UIdisplay(results)
        else:
            return 0
        results=searchroute(route[2],endstation,route[3],results[-4],results[-1])
        if results: UIdisplay(results)
        else:
            return 0        
    if route[0]==3:
        for i in list_line:
            if route[1]==i.get_numero():
                drawpoint(startstation,i,1)
        results=searchroute(startstation,route[2],route[1],timenow,ticketflag)
        if results: UIdisplay(results)
        else:
            return 0
        results=searchroute(route[2],route[4],route[3],results[-4],results[-1])
        if results: UIdisplay(results)
        else:
            return 0
        results=searchroute(route[4],endstation,route[5],results[-4],results[-1])
        if results:
            UIdisplay(results)
        else:
            return 0
    if route[0]==4:
        for i in list_line:
            if route[1]==i.get_numero():
                drawpoint(startstation,i,1)
        results=searchroute(startstation,route[2],route[1],timenow,ticketflag)
        if results: UIdisplay(results)
        else: return 0
        results=searchroute(route[2],route[4],route[3],results[-4],results[-1])
        if results: UIdisplay(results)
        else: return 0
        results=searchroute(route[4],route[6],route[5],results[-4],results[-1])
        if results: UIdisplay(results)
        else: return 0                      
        results=searchroute(route[6],endstation,route[7],results[-4],results[-1])
        if results: UIdisplay(results)
        else: return 0
    print("")
    ticketflag2 = list(set(results[-1]))
#    print("经过区间")
#    for i in ticketflag2:
#        print(i,end="")
#    print("\n")
    print("到达时间"," ","%02d"%int(results[6]//60),":","%02d"%int(results[6]%60))
    print("")
    cv.imwrite('final.png', linemap)   
    
def displayresults_short(route,startstation,endstation,ticketflag):
    global linemap
    if route[0]==1:
        for i in list_line:
            if route[1]==i.get_numero():
                drawpoint(startstation,i,1)
        results=searchroute(startstation,endstation,route[1],timenow,ticketflag)
        if results:
            print(results[7], " ", end="")
        else:
            return 0
    if route[0]==2:
        for i in list_line:
            if route[1]==i.get_numero():
                drawpoint(startstation,i,1)
        results=searchroute(startstation,route[2],route[1],timenow,ticketflag)
        if results:
            print(results[7], ">", end=" ")
        else:
            return 0
        results=searchroute(route[2],endstation,route[3],results[-4],results[-1])
        if results:
            print(results[7], " ", end="")
        else:
            return 0      
    if route[0]==3:
        for i in list_line:
            if route[1]==i.get_numero():
                drawpoint(startstation,i,1)
        results=searchroute(startstation,route[2],route[1],timenow,ticketflag)
        if results:
            print(results[7], ">", end=" ")
        else:
            return 0
        results=searchroute(route[2],route[4],route[3],results[-4],results[-1])
        if results:
            print(results[7], ">", end=" ")
        else:
            return 0
        results=searchroute(route[4],endstation,route[5],results[-4],results[-1])
        if results:
            print(results[7], " ", end="")
        else:
            return 0
    if route[0]==4:
        for i in list_line:
            if route[1]==i.get_numero():
                drawpoint(startstation,i,1)
        results=searchroute(startstation,route[2],route[1],timenow,ticketflag)
        if results:
            print(results[7], ">", end=" ")
        else:
            return 0
        results=searchroute(route[2],route[4],route[3],results[-4],results[-1])
        if results:
            print(results[7], ">", end=" ")
        else:
            return 0
        results=searchroute(route[4],route[6],route[5],results[-4],results[-1])
        if results:
            print(results[7], ">", end=" ")
        else:
            return 0                     
        results=searchroute(route[6],endstation,route[7],results[-4],results[-1])
        if results:
            print(results[7], " ", end="")
        else:
            return 0
    
    
    print(" ", "%02d"%int(results[6]//60),":","%02d"%int(results[6]%60))
    


def displayresults_short_streamlit (route,startstation,endstation,ticketflag):
    global linemap
    output_content = " "
    output_details = " "
    if route[0]==1:
        results=searchroute(startstation,endstation,route[1],timenow,ticketflag)
        if results:
            output_content = output_content + str(results[7])
            output_details = UIdisplay_streamlit(results, output_details)
            # st.write(results[7])
        else:
            return 0
    if route[0]==2:
        results=searchroute(startstation,route[2],route[1],timenow,ticketflag)
        if results:
            output_content = output_content + str(results[7])
            output_content = output_content + " → "
            output_details = UIdisplay_streamlit(results, output_details)

        else:
            return 0
        results=searchroute(route[2],endstation,route[3],results[-4],results[-1])
        if results:
            output_content = output_content + str(results[7])
            output_details = UIdisplay_streamlit(results, output_details)

        else:
            return 0      
    if route[0]==3:
        results=searchroute(startstation,route[2],route[1],timenow,ticketflag)
        if results:
            output_content = output_content + str(results[7])
            output_content = output_content + " → "
            output_details = UIdisplay_streamlit(results, output_details)

        else:
            return 0
        results=searchroute(route[2],route[4],route[3],results[-4],results[-1])
        if results:
            output_content = output_content + str(results[7])
            output_content = output_content + " → "
            output_details = UIdisplay_streamlit(results, output_details)

        else:
            return 0
        results=searchroute(route[4],endstation,route[5],results[-4],results[-1])
        if results:
            output_content = output_content + str(results[7])
            output_details = UIdisplay_streamlit(results, output_details)

        else:
            return 0
    if route[0]==4:
        results=searchroute(startstation,route[2],route[1],timenow,ticketflag)
        if results:
            output_content = output_content + str(results[7])
            output_content = output_content + " → "
            output_details = UIdisplay_streamlit(results, output_details)

        else:
            return 0
        results=searchroute(route[2],route[4],route[3],results[-4],results[-1])
        if results:
            output_content = output_content + str(results[7])
            output_content = output_content + " → "
            output_details = UIdisplay_streamlit(results, output_details)

        else:
            return 0
        results=searchroute(route[4],route[6],route[5],results[-4],results[-1])
        if results:
            output_content = output_content + str(results[7])
            output_content = output_content + " → "
            output_details = UIdisplay_streamlit(results, output_details)

        else:
            return 0                     
        results=searchroute(route[6],endstation,route[7],results[-4],results[-1])
        if results:
            output_content = output_content + str(results[7])
            output_details = UIdisplay_streamlit(results, output_details)

        else:
            return 0
    
    
    if results[6] > 1440:
        results6 = results[6] - 1440
    else:
        results6 = results[6]
    
    output_content += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;到达时间&nbsp;&nbsp;" + "%02d"%int(results6//60) + ":" + "%02d"%int(results6%60)
    with st.expander(output_content):
        st.markdown(output_details,unsafe_allow_html=True)
    #st.write(" ", "%02d"%int(results[6]//60),":","%02d"%int(results[6]%60),"</p>")

    
        
def main():
    os.system("clear")
    print("小浪底公交服务系统v1.3")  
    global linemap
    isended=0
    global timenow
    global issunday
    issunday = 1
    global charge
    try:
        print("系统时间？\n ")
        print(color.UNDERLINE+"0 否"+color.END,end="\t")
        print(color.UNDERLINE+"1 是"+color.END,end="\n")
        systemtime=int(input(""))
    except ValueError:
        print("")
    if systemtime:
        hour=time.localtime().tm_hour
        minute=time.localtime().tm_min
        issunday=0
    else:
        os.system("clear")
        try: hour=int(input("小时\n"))
        except ValueError:
            print("")
        os.system("clear")
        try: minute=int(input("分钟\n"))
        except ValueError:
            print("")
        os.system("clear")
    timenow=60*hour+minute
    for i in list_station:
        i.initialiser()
    charge=round(rd.randint(5,2000)/10,1)
    while(isended==0):
        linemap=cv.imread("real.png")
        os.system("clear")
        if systemtime:
            hour=time.localtime().tm_hour
            minute=time.localtime().tm_min
            issunday=is_week_lastday()
            timenow=60*hour+minute
        print("%02d"%int(hour),":","%02d"%int(minute),end=" ")
        if issunday:
            print("星期天",end=" ")
        else:
            print("工作日",end=" ")
        print("余额 ",round(charge,1),"元")
        print(color.UNDERLINE+"0 退出系统"+color.END,end="\n")
        print(color.UNDERLINE+"1 路线查询"+color.END,end="\t")
        print(color.UNDERLINE+"2 购票系统"+color.END,end="\t")        
        print(color.UNDERLINE+"3 线路查询"+color.END,end="\t")
        print(color.UNDERLINE+"4 候车查询"+color.END,end="\t")
        print(color.UNDERLINE+"5 账户查询"+color.END)
        option=-1
        while(option>10 or option<0):
            try:
                option=int(input(""))
            except ValueError:
                print("")
            os.system("clear")
        if option==3:
            searchline()
        if option==4:
            searchstation()
        if option==5:
            acount()
        if option==2:
            achat()
        if option==1:
            get_station=0
            while(get_station==0):
                startstation=input("出发地\n输入汉语全称或者拼音首字母\n")
                os.system("clear")                
                endstation=input("目的地\n输入汉语全称或者拼音首字母\n")
                os.system("clear")
                if startstation=="s" and endstation=="s":
                    startstation=list_station[rd.randint(0,len(list_station))].get_name()
                    endstation=list_station[rd.randint(0,len(list_station))].get_name()
                for i in list_station:
                    if startstation==i.get_name():
                        stationstarted=i
                        get_station=1
                    if endstation==i.get_name():
                        stationended=i
                        get_station=1
            route=[]
            route=search1(stationstarted,stationended,route)
            route=search2(stationstarted,stationended,route)
            if len(route) < 10:
               route=search3(stationstarted,stationended,route)
            if len(route) < 2:
               route=search4(stationstarted,stationended,route)
            route_sorted=sorted(route, key=lambda s: s[-1])
            number_route = len(route_sorted)
            route_sorted_to_delete_index = []
            for j in range(number_route):
               if route_sorted[j][0] == 2 and route_sorted[j][1] == route_sorted[j][3]:
                  route_sorted_to_delete_index.append(j)
               if route_sorted[j][0] == 3 and (route_sorted[j][1] == route_sorted[j][3] or route_sorted[j][1] == route_sorted[j][5] or route_sorted[j][3] == route_sorted[j][5]):
                  route_sorted_to_delete_index.append(j)
               if route_sorted[j][0] == 5 and (
                     route_sorted[j][1] == route_sorted[j][3] or
                     route_sorted[j][1] == route_sorted[j][5] or
                     route_sorted[j][1] == route_sorted[j][7] or
                     route_sorted[j][3] == route_sorted[j][5] or
                     route_sorted[j][3] == route_sorted[j][7] or
                     route_sorted[j][5] == route_sorted[j][7]   
               ):
                  route_sorted_to_delete_index.append(j)
            for j in range(number_route-1):
               for k in range(number_route-1):
                  if k+1 > j:
                     if route_sorted[j][0] == route_sorted[k+1][0]:
                        if route_sorted[j][0] == 2:
                           if route_sorted[j][1] == route_sorted[k+1][1] and route_sorted[j][3] == route_sorted[k+1][3]:
                              if k+1 not in route_sorted_to_delete_index:
                                 route_sorted_to_delete_index.append(k+1)
                              break
                        if route_sorted[j][0] == 3:
                           if route_sorted[j][1] == route_sorted[k+1][1] and route_sorted[j][3] == route_sorted[k+1][3] and route_sorted[j][5] == route_sorted[k+1][5]:
                              if k+1 not in route_sorted_to_delete_index:
                                 route_sorted_to_delete_index.append(k+1)
                              break
                        if route_sorted[j][0] == 4:
                           if route_sorted[j][1] == route_sorted[k+1][1] and route_sorted[j][3] == route_sorted[k+1][3] and route_sorted[j][5] == route_sorted[k+1][5] and route_sorted[j][7] == route_sorted[k+1][7]:
                              if k+1 not in route_sorted_to_delete_index:
                                 route_sorted_to_delete_index.append(k+1)
                              break
#            print(route_sorted_to_delete_index)
            remove_by_indices(route_sorted, route_sorted_to_delete_index)
            route_sorted2 = [element for index, element in enumerate(route_sorted) if index not in route_sorted_to_delete_index]

            
            isshortend=0
            while isshortend==0:
               os.system("clear")
               print(color.BOLD+startstation+color.END,color.BOLD+"---->"+color.END,color.BOLD+endstation+color.END,"\n")
               for i in range(min(len(route_sorted2),10)):
                  ticketflag_short=[]
                  print("路线",i+1," ",end="")
                  displayresults_short(route_sorted2[i],startstation,endstation,ticketflag_short)
               signal2 = 0
               try:
                  print(color.UNDERLINE+"0 退出\t"+color.END,color.UNDERLINE+"输入其他数字查看详情\n"+color.END)
                  signal2=int(input(""))
               except ValueError:
                  print("")
               if signal2 == 0:
                  isshortend = 1
               if signal2 > 0:                  
                  isendeded=0
                  if len(route_sorted2)<1:
                     isendeded=1
                  order=signal2 - 1
                  while isendeded==0:
                     ticketflag=[]
                     os.system("clear")                
                     displayresults(route_sorted2[order],startstation,endstation,ticketflag)
                     print(order+1,"/",len(route_sorted2))
                     try:
                        print(color.UNDERLINE+"0 退出\t"+color.END,color.UNDERLINE+"1 下一结果\t"+color.END,color.UNDERLINE+"2 上一结果\n"+color.END)
                        signal=int(input(""))
                     except ValueError:
                        print("")
                        os.system("clear")                
                     if signal==0:
                        isendeded=1
                     else:
                        linemap=cv.imread("real.png")
                        if signal==1:
                           order+=1
                        if signal==2:
                           order-=1
                        if order>=len(route_sorted2):
                           order=len(route_sorted2)-1
                        if order<0:
                           order=0

                
                    
        if option==0:
            isended=1
        if isended==0:
            try:
                print(color.UNDERLINE+"\n\n 0 返回\n"+color.END)
                isended=int(input(""))
            except ValueError:
                print("")

line_extra_info = read_excel("line-stations-data/line-extra-info.xls", 0)

line_number = []
line_company = []
line_timetable_type = []
line_vehicule = []
line_color_r = []
line_color_g = []
line_color_b = []

for i in line_extra_info:
   line_number.append(int(float(i[0])))
   line_company.append(int(float(i[1])))
   line_timetable_type.append(int(float(i[2])))
   line_vehicule.append(i[3])
   line_color_r.append(int(float(i[4])))
   line_color_g.append(int(float(i[5])))
   line_color_b.append(int(float(i[6])))


for i in range(len(line_number)):
   line_station_data = read_excel("line-stations-data/line1.xls", i)
   line_object = busline(1,0,0,0,0,0,fast_normal_timetable,fast_normal_timetable)
   if line_timetable_type[i] == 0:
      line_object = busline(line_number[i], 0, 24, line_company[i], 1,1, fast_normal_timetable, fast_normal_timetable)
   if line_timetable_type[i] == 1:
      line_object = busline(line_number[i], 5, 24, line_company[i], 1,1, main_normal_timetable, main_normal_timetable)
   if line_timetable_type[i] == 2:
      line_object = busline(line_number[i], 5, 24, line_company[i], 1,1, slow_normal_timetable, slow_normal_timetable)

   station_list_tmp = []
   interval_list_tmp = []
   
   for j in line_station_data:
      station_list_tmp.append(j[0])
      interval_list_tmp.append(float(j[2]))
      
   line_object.add_station(station_list_tmp)
   line_object.add_interval(interval_list_tmp)
   line_object.add_linecolor((line_color_r[i],line_color_g[i],line_color_b[i]))

   list_line.append(line_object)


colorbar=[[105, 140, 255],[180,229,255],[208,253,255],[250,230,230],[214,122,218]]
zonebar=["*","*","**","***","****","*****"]
prince_list=[
    [1,1],
    [2,1],
    [3,2],
    [4,3],
    [5,4],
    [12,1.5],
    [23,2.5],
    [34,4.5],
    [45,6.5],
    [123,3],
    [234,5],
    [345,8],
    [1234,5.5],
    [2345,8.5],
    [12345,9]
]

list_station_name = []

for i in list_station:
   i.add_position([1,1,1,1],1)
   i.add_shortname("xxx")
   list_station_name.append(i.get_name())




st.set_page_config(
    page_title="小浪底公共出行企划书｜小浪底大众运输查询系统",
    page_icon="🚌",
)
st.title("路线规划")

if 'selected_time' not in st.session_state:
    st.session_state.selected_time = datetime.now().time()


col1, col2 ,col3= st.columns(3)
with col1:
    start_station = st.selectbox("从哪一站出发？",list_station_name,index = 30)
with col2:
    end_station = st.selectbox("想去哪里？",list_station_name,index = 10)
with col3:
    selected_time = st.time_input("出发时间", value=st.session_state.selected_time)
is_button_applied = st.button("开始规划")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

#hour=time.localtime().tm_hour
#minute=time.localtime().tm_min
hour = selected_time.hour
minute = selected_time.minute
issunday=0
timenow=60*hour+minute
for i in list_station:
    i.initialiser()


if is_button_applied:
    for i in list_station:
        if start_station==i.get_name():
            stationstarted=i
        if end_station==i.get_name():
            stationended=i
    route=[]
    route=search1(stationstarted,stationended,route)
    route=search2(stationstarted,stationended,route)
    if len(route) < 10:
       route=search3(stationstarted,stationended,route)
    if len(route) < 2:
       route=search4(stationstarted,stationended,route)
    route_sorted=sorted(route, key=lambda s: s[-1])
    number_route = len(route_sorted)
    route_sorted_to_delete_index = []
    for j in range(number_route):
       if route_sorted[j][0] == 2 and route_sorted[j][1] == route_sorted[j][3]:
          route_sorted_to_delete_index.append(j)
       if route_sorted[j][0] == 3 and (route_sorted[j][1] == route_sorted[j][3] or route_sorted[j][1] == route_sorted[j][5] or route_sorted[j][3] == route_sorted[j][5]):
          route_sorted_to_delete_index.append(j)
       if route_sorted[j][0] == 5 and (
             route_sorted[j][1] == route_sorted[j][3] or
             route_sorted[j][1] == route_sorted[j][5] or
             route_sorted[j][1] == route_sorted[j][7] or
             route_sorted[j][3] == route_sorted[j][5] or
             route_sorted[j][3] == route_sorted[j][7] or
             route_sorted[j][5] == route_sorted[j][7]   
       ):
          route_sorted_to_delete_index.append(j)
    for j in range(number_route-1):
       for k in range(number_route-1):
          if k+1 > j:
             if route_sorted[j][0] == route_sorted[k+1][0]:
                if route_sorted[j][0] == 2:
                   if route_sorted[j][1] == route_sorted[k+1][1] and route_sorted[j][3] == route_sorted[k+1][3]:
                      if k+1 not in route_sorted_to_delete_index:
                         route_sorted_to_delete_index.append(k+1)
                      break
                if route_sorted[j][0] == 3:
                   if route_sorted[j][1] == route_sorted[k+1][1] and route_sorted[j][3] == route_sorted[k+1][3] and route_sorted[j][5] == route_sorted[k+1][5]:
                      if k+1 not in route_sorted_to_delete_index:
                         route_sorted_to_delete_index.append(k+1)
                      break
                if route_sorted[j][0] == 4:
                   if route_sorted[j][1] == route_sorted[k+1][1] and route_sorted[j][3] == route_sorted[k+1][3] and route_sorted[j][5] == route_sorted[k+1][5] and route_sorted[j][7] == route_sorted[k+1][7]:
                      if k+1 not in route_sorted_to_delete_index:
                         route_sorted_to_delete_index.append(k+1)
                      break
#            print(route_sorted_to_delete_index)
    remove_by_indices(route_sorted, route_sorted_to_delete_index)
    route_sorted2 = [element for index, element in enumerate(route_sorted) if index not in route_sorted_to_delete_index]
    for i in range(min(len(route_sorted2),10)):
        ticketflag_short=[]
        # st.write("路线",i+1)
        displayresults_short_streamlit(route_sorted2[i],start_station,end_station,ticketflag_short)

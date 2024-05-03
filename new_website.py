import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import calendar
import time
import xlrd
import math
import matplotlib.image as mpimg # mpimg 用于读取图片
import random as rd
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, time
import csv
from streamlit_folium import folium_static
import folium






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
    def __init__(self,numero,starttime=5,endtime=22,proprity=1,time=1,price=1,timetable1=slow_normal_timetable,timetable2=slow_normal_timetable,level=0):
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
        self.__level=level
        
        
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
    
    def add_level(self,level):
        self.__level = level
        
    def get_level(self):
        return self.__level
            
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
    
    def get_info_streamlit(self):
        
        output_str = str(self.get_numero())+"路"
        if self.__level == 0:
            output_str += "  核心线路"
        if self.__level == 1:
            output_str += "  主干线路"
        if self.__level == 2:
            output_str += "  支线"
        st.subheader(output_str)
        if self.__proprity==0:
            st.write("小浪底大众运输公司运营", "监督电话030-41224100")
        elif self.__proprity==1:
            st.write("小浪底白鹿原通勤公司运营", "监督电话030-41224200") 
        elif self.__proprity==2:
            st.write("小浪底北郊大众运输专门组织运营","监督电话030-41224105")
        else:
            st.write("小浪底南郊大众运输专门组织运营","监督电话030-45882155")
        st.write("首班车",self.__starttime,"点", "，末班车",self.__endtime,"点","\n")
        st.write()
        st.markdown('<span style="font-weight:bold;font-size:18px;">站点</span>',unsafe_allow_html=True)
        connectiontemp2=0
        for m in self.__station:
            for n in list_station:
                if m==n.get_name():
                    if connectiontemp2==1:
                        pass#print("|")                        
                    st.write(str(int(self.get_interval()[self.__station.index(m)])),"分 ",m)
                    connectiontemp2=1
        self.affichage_timetable_streamlit()

    
    
    def get_starttime(self):
        return self.__starttime
    
    def get_endtime(self):
        return self.__endtime
    
    def affichage_timetable(self):
        print(color.BOLD+"\n发车时刻表"+color.END)
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
    def affichage_timetable_streamlit(self):
        st.markdown('<span style="font-weight:bold;font-size:18px;">双向对发时刻表</span>',unsafe_allow_html=True)
        hourtemp=-1
        issunday = 0
        timetable_output_str = ""
        for i in self.__timetable1:
            if i <1440:
                if i//60!=hourtemp:
                    timetable_output_str += "  \n" + '<span style="font-weight:bold;">' +"%02d"%(i//60)+"</span>&nbsp;&nbsp;&nbsp;&nbsp;"
                timetable_output_str += "%02d"%(i%60) + "&nbsp;&nbsp;"
                hourtemp=i//60
        st.markdown(timetable_output_str,unsafe_allow_html=True)
    
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
        self.__openposition=[112.3864124,34.93619181]
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
    
    def add_openposition(self, position):
        self.__openposition=position
        
    def get_openposition(self):
        return self.__openposition
        
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
    def get_info_streamlit(self):
        st.subheader(self.get_name())
        st.markdown('<span style="font-size:18px; font-weight:bold;">停靠线路', unsafe_allow_html=True)
        output_line_list = ""
        for i in self.get_line():
            output_line_list += str(i) + "&nbsp;&nbsp;"
        st.markdown(output_line_list, unsafe_allow_html=True)
        self.get_timetable_streamlit()
        
    def get_info_streamlit_popup(self):
        output_line_list = '<p>停靠线路</p> <p>'
        for i in self.get_line():
            output_line_list += str(i) + " "
        output_line_list += '</p>'
        return output_line_list


        
    def initialiser(self):
        for i in self.__line:
            for j in list_line:
                if i==j.get_numero():
                    liste_de_line=j.get_station()
                    for k in liste_de_line:
                        if k!=self.get_name():
                            if j.get_level() == 0:
                                prefactor = 0.1
                            elif j.get_level() == 1:
                                prefactor = 0.5
                            else:
                                prefactor = 1
                            self.__neighborhood.append((k,prefactor * abs(j.get_interval()[liste_de_line.index(k)]-j.get_interval()[liste_de_line.index(self.get_name())]),j.get_numero()))
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

    def get_timetable_streamlit(self):
        for i in self.__timetable:
            waiting_time = []
            for j in i[2]:      
                time_rest=j-timenow  
                if j>timenow:
                    waiting_time.append(time_rest)
                    if len(waiting_time)>2:
                        break
            output_str = ""
            if time_rest<0:
                output_str += '<span style="font-weight:bold;">' + str(i[0]) + '路</span> &nbsp;&nbsp;' + '<span style="font-weight:bold;">' + i[1] + "</span>停止营运"
            else:
                output_str += '<span style="font-weight:bold;">' + str(i[0]) + '路</span> &nbsp;&nbsp;开往' + '<span style="font-weight:bold;">' + i[1] + "方向</span>等待"
                for k in waiting_time:
                    output_str += "&nbsp;" + str(int(k)) + "&nbsp;"
                output_str += "分钟    \n"
            st.markdown(output_str, unsafe_allow_html=True)
            
    def get_timetable_streamlit_popup(self):
        output_str = ""
        for i in self.__timetable:
            output_str += "<p>"
            waiting_time = []
            for j in i[2]:      
                time_rest=j-timenow  
                if j>timenow:
                    waiting_time.append(time_rest)
                    if len(waiting_time)>2:
                        break

            if time_rest<0:
                output_str += str(i[0]) + '&nbsp;&nbsp;' + i[1] + "停止营运"
            else:
                output_str += str(i[0]) + '路开往' + i[1] + "方向 等待"
                for k in waiting_time:
                    output_str += " " + str(int(k)) + " "
                output_str += "分钟</p>"
        return output_str

    def give_timetable(self):
        return self.__timetable



#now = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))

# 判断今天是否为周末
    
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
    if results[4] > 1440:
        results4 = results[4] - 1440
    else:
        results4 = results[4]
    if results[6] > 1440:
        results6 = results[6] - 1440
    else:
        results6 = results[6]
    spendtime = results[6] - results[4]
    output_str += '<span style="font-size:20px;">'+stationstarted.get_name()+'&nbsp;'+"%02d"%int(results4//60)+":"+"%02d"%int(results4%60)+'&nbsp;→&nbsp;'+stationended.get_name()+'&nbsp;'+"%02d"%int(results6//60)+":"+"%02d"%int(results6%60)+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用时" + str(int(spendtime)) + "分钟</span>  \n"
    output_str += '<span style="font-size:18px; font-weight:bold;">'+str(results[7])+"路&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;开往"+results[-2]+"方向</span>  \n"
#    output_str += '<span style="font-size:16px; font-weight:bold;">'+"%02d"%int(results[4]//60)+":"+"%02d"%int(results[4]%60)+"&nbsp;→&nbsp;"+"%02d"%int(results[6]//60)+":"+"%02d"%int(results[6]%60)+"</span>  \n"
    output_str += '<span style="font-size:14px; font-weight:bold;">'+"等待约"+str(int(results[3]))+"分钟</span>  \n"
    for j in results[5]:
        for m in list_station:
            if j==m.get_name():
                delaytemp=abs(linetemp.get_interval()[linetemp.get_station().index(m.get_name())]-linetemp.get_interval()[linetemp.get_station().index(stationstarted.get_name())])
                #print(zonebar[m.get_zone()],"\t","%02d"%int((results[4]+delaytemp)//60),":","%02d"%int((results[4]+delaytemp)%60),"\t ",j)
                if results4+delaytemp > 1440:
                    results4 -= 1440
                output_str += '<span style="font-size:12px;">'+ "%02d"%int((results4+delaytemp)//60)+":"+"%02d"%int((results4+delaytemp)%60)+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+j+"</span>  \n"
    output_str += "  \n"
    return output_str

    
    
def displayresults_short_streamlit (route,startstation,endstation,ticketflag):
    global linemap
    output_content = " "
    output_details = " "
    lines_to_draw = []
    name_to_draw = []
    color_to_draw = []
    linename_to_draw = []
    if route[0]==1:
        results=searchroute(startstation,endstation,route[1],timenow,ticketflag)
        if results:
            output_content = output_content + str(results[7])
            output_details = UIdisplay_streamlit(results, output_details)
            coordinates_tmp = []
            
            for j in results[5]:                
                for m in list_station:
                    if j==m.get_name():
                        coordinates_tmp.append([float(m.get_openposition()[1]),float( m.get_openposition()[0])])
            for k in list_line:
                if k.get_numero()==results[7]:
                    linetemp=k   
                    color_to_draw.append('rgb({}, {}, {})'.format(linetemp.get_linecolor()[0], linetemp.get_linecolor()[1], linetemp.get_linecolor()[2]))
                    linename_to_draw.append(str(linetemp.get_numero()))
                    
            lines_to_draw.append(coordinates_tmp)
            
            name_to_draw.append(results[5])

            # st.write(results[7])
        else:
            return 0
    if route[0]==2:
        results=searchroute(startstation,route[2],route[1],timenow,ticketflag)
        if results:
            coordinates_tmp = []

            output_content = output_content + str(results[7])
            output_content = output_content + " → "
            output_details = UIdisplay_streamlit(results, output_details)
            for j in results[5]:                
                for m in list_station:
                    if j==m.get_name():
                        coordinates_tmp.append([float(m.get_openposition()[1]),float( m.get_openposition()[0])])

            for k in list_line:
                if k.get_numero()==results[7]:
                    linetemp=k   
                    color_to_draw.append('rgb({}, {}, {})'.format(linetemp.get_linecolor()[0], linetemp.get_linecolor()[1], linetemp.get_linecolor()[2]))
                    linename_to_draw.append(str(linetemp.get_numero()))
            lines_to_draw.append(coordinates_tmp)
            name_to_draw.append(results[5])

        else:
            return 0
        results=searchroute(route[2],endstation,route[3],results[-4],results[-1])
        if results:
            coordinates_tmp = []

            output_content = output_content + str(results[7])
            output_details = UIdisplay_streamlit(results, output_details)
            for j in results[5]:                
                for m in list_station:
                    if j==m.get_name():
                        coordinates_tmp.append([float(m.get_openposition()[1]),float( m.get_openposition()[0])])

            for k in list_line:
                if k.get_numero()==results[7]:
                    linetemp=k   
                    color_to_draw.append('rgb({}, {}, {})'.format(linetemp.get_linecolor()[0], linetemp.get_linecolor()[1], linetemp.get_linecolor()[2]))
                    linename_to_draw.append(str(linetemp.get_numero()))
            lines_to_draw.append(coordinates_tmp)
            name_to_draw.append(results[5])

        else:
            return 0      
    if route[0]==3:

        results=searchroute(startstation,route[2],route[1],timenow,ticketflag)
        if results:
            coordinates_tmp = []

            output_content = output_content + str(results[7])
            output_content = output_content + " → "
            output_details = UIdisplay_streamlit(results, output_details)
            for j in results[5]:                
                for m in list_station:
                    if j==m.get_name():
                        coordinates_tmp.append([float(m.get_openposition()[1]),float( m.get_openposition()[0])])

            for k in list_line:
                if k.get_numero()==results[7]:
                    linetemp=k   
                    color_to_draw.append('rgb({}, {}, {})'.format(linetemp.get_linecolor()[0], linetemp.get_linecolor()[1], linetemp.get_linecolor()[2]))
                    linename_to_draw.append(str(linetemp.get_numero()))
            lines_to_draw.append(coordinates_tmp)
            name_to_draw.append(results[5])

        else:
            return 0
        results=searchroute(route[2],route[4],route[3],results[-4],results[-1])
        if results:
            coordinates_tmp = []

            output_content = output_content + str(results[7])
            output_content = output_content + " → "
            output_details = UIdisplay_streamlit(results, output_details)
            for j in results[5]:                
                for m in list_station:
                    if j==m.get_name():
                        coordinates_tmp.append([float(m.get_openposition()[1]),float( m.get_openposition()[0])])
            for k in list_line:
                if k.get_numero()==results[7]:
                    linetemp=k   
                    color_to_draw.append('rgb({}, {}, {})'.format(linetemp.get_linecolor()[0], linetemp.get_linecolor()[1], linetemp.get_linecolor()[2]))
                    linename_to_draw.append(str(linetemp.get_numero()))
            lines_to_draw.append(coordinates_tmp)
            name_to_draw.append(results[5])

        else:
            return 0
        results=searchroute(route[4],endstation,route[5],results[-4],results[-1])
        if results:
            coordinates_tmp = []

            output_content = output_content + str(results[7])
            output_details = UIdisplay_streamlit(results, output_details)
            for j in results[5]:                
                for m in list_station:
                    if j==m.get_name():
                        coordinates_tmp.append([float(m.get_openposition()[1]),float( m.get_openposition()[0])])
            for k in list_line:
                if k.get_numero()==results[7]:
                    linetemp=k   
                    color_to_draw.append('rgb({}, {}, {})'.format(linetemp.get_linecolor()[0], linetemp.get_linecolor()[1], linetemp.get_linecolor()[2]))
                    linename_to_draw.append(str(linetemp.get_numero()))
            lines_to_draw.append(coordinates_tmp)
            name_to_draw.append(results[5])

        else:
            return 0
    if route[0]==4:

        results=searchroute(startstation,route[2],route[1],timenow,ticketflag)
        if results:
            coordinates_tmp = []

            output_content = output_content + str(results[7])
            output_content = output_content + " → "
            output_details = UIdisplay_streamlit(results, output_details)
            for j in results[5]:                
                for m in list_station:
                    if j==m.get_name():
                        coordinates_tmp.append([float(m.get_openposition()[1]),float( m.get_openposition()[0])])
            for k in list_line:
                if k.get_numero()==results[7]:
                    linetemp=k   
                    color_to_draw.append('rgb({}, {}, {})'.format(linetemp.get_linecolor()[0], linetemp.get_linecolor()[1], linetemp.get_linecolor()[2]))
                    linename_to_draw.append(str(linetemp.get_numero()))
            lines_to_draw.append(coordinates_tmp)
            name_to_draw.append(results[5])

        else:
            return 0
        results=searchroute(route[2],route[4],route[3],results[-4],results[-1])
        if results:
            coordinates_tmp = []

            output_content = output_content + str(results[7])
            output_content = output_content + " → "
            output_details = UIdisplay_streamlit(results, output_details)
            for j in results[5]:                
                for m in list_station:
                    if j==m.get_name():
                        coordinates_tmp.append([float(m.get_openposition()[1]),float( m.get_openposition()[0])])
            for k in list_line:
                if k.get_numero()==results[7]:
                    linetemp=k   
                    color_to_draw.append('rgb({}, {}, {})'.format(linetemp.get_linecolor()[0], linetemp.get_linecolor()[1], linetemp.get_linecolor()[2]))
                    linename_to_draw.append(str(linetemp.get_numero()))
            lines_to_draw.append(coordinates_tmp)
            name_to_draw.append(results[5])

        else:
            return 0
        results=searchroute(route[4],route[6],route[5],results[-4],results[-1])
        if results:
            coordinates_tmp = []

            output_content = output_content + str(results[7])
            output_content = output_content + " → "
            output_details = UIdisplay_streamlit(results, output_details)
            for j in results[5]:                
                for m in list_station:
                    if j==m.get_name():
                        coordinates_tmp.append([float(m.get_openposition()[1]),float( m.get_openposition()[0])])
            for k in list_line:
                if k.get_numero()==results[7]:
                    linetemp=k   
                    color_to_draw.append('rgb({}, {}, {})'.format(linetemp.get_linecolor()[0], linetemp.get_linecolor()[1], linetemp.get_linecolor()[2]))
                    linename_to_draw.append(str(linetemp.get_numero()))
            lines_to_draw.append(coordinates_tmp)
            name_to_draw.append(results[5])

        else:
            return 0                     
        results=searchroute(route[6],endstation,route[7],results[-4],results[-1])
        if results:
            coordinates_tmp = []

            output_content = output_content + str(results[7])
            output_details = UIdisplay_streamlit(results, output_details)
            for j in results[5]:                
                for m in list_station:
                    if j==m.get_name():
                        coordinates_tmp.append([float(m.get_openposition()[1]),float( m.get_openposition()[0])])
            for k in list_line:
                if k.get_numero()==results[7]:
                    linetemp=k   
                    color_to_draw.append('rgb({}, {}, {})'.format(linetemp.get_linecolor()[0], linetemp.get_linecolor()[1], linetemp.get_linecolor()[2]))
                    linename_to_draw.append(str(linetemp.get_numero()))
            lines_to_draw.append(coordinates_tmp)
            name_to_draw.append(results[5])

        else:
            return 0

    if results[6] > 1440:
        results6 = results[6] - 1440
    else:
        results6 = results[6]
    spendtime = results[6] - timenow
    output_content += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + "&nbsp;&nbsp;约" + "%d"%int(spendtime) + "分钟&nbsp;&nbsp;" + "%02d"%int(results6//60) + ":" + "%02d"%int(results6%60) + "到达"
    with st.expander(output_content):
        m = folium.Map(location=[34.93619181,112.3864124], zoom_start=14,width='90%')  
        for i in range(len(lines_to_draw)):        
            folium.PolyLine(locations=lines_to_draw[i], color = color_to_draw[i]).add_to(m)
            for j in range(len(lines_to_draw[i])):
                if i > 0 and j == 0:    
                    label_output = name_to_draw[i][j] + " 由" + linename_to_draw[i-1] + "路换乘" + linename_to_draw[i] + "路"
                    folium.CircleMarker(location=lines_to_draw[i][j], tooltip=label_output, max_width=300, fill_opacity=1,  fill = True, opacity=1, color='grey', stroke=False).add_to(m)
                else:
                    label_output = name_to_draw[i][j] + " " + linename_to_draw[i] + "路" 
                    folium.CircleMarker(location=lines_to_draw[i][j], tooltip=label_output, max_width=300, fill_opacity=0.6,  fill = True, opacity=1, color=color_to_draw[i], stroke=False).add_to(m)
        folium_static(m)    
        st.markdown(output_details,unsafe_allow_html=True)

    #st.write(" ", "%02d"%int(results[6]//60),":","%02d"%int(results[6]%60),"</p>")

    
        

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
      line_object = busline(line_number[i], 0, 24, line_company[i], 1,1, fast_normal_timetable, fast_normal_timetable, 0)
   if line_timetable_type[i] == 1:
      line_object = busline(line_number[i], 5, 24, line_company[i], 1,1, main_normal_timetable, main_normal_timetable, 1)
   if line_timetable_type[i] == 2:
      line_object = busline(line_number[i], 5, 24, line_company[i], 1,1, slow_normal_timetable, slow_normal_timetable, 2)

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

station_position_data = read_excel("line-stations-data/stations-info.xls", 0)

for i in list_station:
    for j in station_position_data:
        if i.get_name() == j[0]:
            i.add_openposition([j[3],j[4]])
    i.add_position([1,1,1,1],1)
    i.add_shortname("xxx")
    list_station_name.append(i.get_name())
   
# print(list_station_name)
# csv_file = 'line-stations-data/stations-info-original.csv'
# with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
#     writer = csv.writer(file)
    
#     for row in list_station_name:
#         writer.writerow(row)
        
list_line_name = []
for i in list_line:
    list_line_name.append(str(i.get_numero()))

issunday=0
for i in list_station:
    i.initialiser()

st.set_page_config(
    page_title="小浪底大区公共交通查询系统",
    page_icon="logo.png"
)

timenow = (datetime.now().time().hour+2)*60+datetime.now().time().minute
if timenow >= 1440:
    timenow -= 1440


def route_searcher():
    st.title("路线规划")
    
    if 'selected_time' not in st.session_state:
        st.session_state.selected_time = datetime.now().time()
        now = datetime.now().time()
        new_hour = (now.hour + 2) % 24
        new_time = now.replace(hour=new_hour)
        st.session_state.selected_time = new_time
    
    col1, col2 ,col3= st.columns(3)
    with col1:
        start_station = st.selectbox("出发地",list_station_name,index = 0)
    with col2:
        end_station = st.selectbox("目的地",list_station_name,index = 10)
    with col3:
        selected_time = st.time_input("出发时间", value=st.session_state.selected_time)
    is_button_applied = st.button("查询")
    
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    local_css("style.css")
    
    #hour=time.localtime().tm_hour
    #minute=time.localtime().tm_min

    
    
    
    if is_button_applied:
        hour = selected_time.hour
        minute = selected_time.minute
        global timenow
        timenow=60*hour+minute
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
        for i in range(min(len(route_sorted2),15)):
            ticketflag_short=[]
            displayresults_short_streamlit(route_sorted2[i],start_station,end_station,ticketflag_short)
            
            
def line_searcher():
    st.title("线路信息")
    
    
    st.subheader("查询路号")
    line_selected = st.selectbox("",list_line_name,index = 0)
    lineselected = list_line[0]
    for i in list_line:
        if line_selected == str(i.get_numero()) :
            lineselected = i
    color_str = 'rgb({}, {}, {})'.format(lineselected.get_linecolor()[0], lineselected.get_linecolor()[1], lineselected.get_linecolor()[2])
    m = folium.Map(location=[34.93619181,112.3864124], zoom_start=14,width='90%')  
    coordinates = []
    for i in lineselected.get_station():
        for j in list_station:
            if i == j.get_name():
                folium.CircleMarker(location=[j.get_openposition()[1], j.get_openposition()[0]], tooltip=j.get_name(), max_width=300, fill_opacity=0.6,  fill = True, opacity=1, color=color_str, stroke=False).add_to(m)
                coordinates.append([float(j.get_openposition()[1]),float( j.get_openposition()[0])])
    folium.PolyLine(locations=coordinates, color=color_str).add_to(m)
    folium_static(m)    

            
            
    lineselected.get_info_streamlit()
    
    
    st.write("核心线路")
    st.image(["line_logo/1.png","line_logo/3.png","line_logo/4.png","line_logo/5.png","line_logo/6.png","line_logo/95.png"])
    st.write("主干线路")
    st.image(["line_logo/2.png","line_logo/7.png","line_logo/8.png","line_logo/9.png","line_logo/10.png","line_logo/11.png","line_logo/12.png","line_logo/16.png","line_logo/60.png","line_logo/96.png"])
    st.write("支线")
    st.image(["line_logo/14.png","line_logo/15.png","line_logo/17.png","line_logo/50.png","line_logo/51.png","line_logo/61.png","line_logo/62.png","line_logo/63.png","line_logo/64.png","line_logo/69.png","line_logo/91.png","line_logo/92.png","line_logo/93.png","line_logo/97.png","line_logo/98.png","line_logo/99.png"])



    


def station_searcher():
    global timenow
    timenow = (datetime.now().time().hour+2)*60+datetime.now().time().minute
    if timenow >= 1440:
        timenow -= 1440   
    st.title("候车查询")
    timestr = "当前时刻" + "%02d"%int(timenow//60) + ":" + "%02d"%int(timenow%60)
    st.write(timestr)
    st.subheader("点击站点查询")

    
    m = folium.Map(location=[34.93619181,112.3864124], zoom_start=14,width='90%')  
    

    for i in list_station:
        
        show_str = "<p>" + i.get_name() + "  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + "</p>"
        show_str += i.get_info_streamlit_popup() + i.get_timetable_streamlit_popup()
        folium.CircleMarker(location=[i.get_openposition()[1], i.get_openposition()[0]], popup=show_str, max_width=300, tooltip=i.get_name(), fill_opacity=0.6,  fill = True, opacity=1, stroke=False).add_to(m)

    folium_static(m)    
    
    st.subheader("或选择/输入站点")
    station_selected= st.selectbox("", list_station_name, index=0)
    stationselected = list_station[0]
    for i in list_station:
        if station_selected == i.get_name():
            stationselected = i
    stationselected.get_info_streamlit()
    

def browser_map():
    github_pdf_url = "https://github.com/xuezhongh97/newxiaolangdi/blob/main/plan2024mini.pdf"
    st.markdown(f'[小浪底大区公共交通线路图、核心线路图、综合时刻表、票价]({github_pdf_url})')

def main(): 
    st.sidebar.image("logo.png")
    
    page_selection = st.sidebar.radio("", ("路线规划", "线路信息", "候车查询", "交通地图"))

    if page_selection == "路线规划":
        route_searcher()
    elif page_selection == "线路信息":
        line_searcher()
    elif page_selection == "候车查询":
        station_searcher()
    elif page_selection == "交通地图":
        browser_map()

if __name__ == "__main__":
    main()
    

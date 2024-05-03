#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 16:04:54 2024

@author: xue
"""

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

def read_excel(excel_path, sheet_no = 0):
    book = xlrd.open_workbook(excel_path)
    sheet = book.sheet_by_index(sheet_no)
    return np.array([list(map(lambda x : x.value, sheet.row(i))) for i in range(sheet.nrows)])


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
   
list_line_name = []
for i in list_line:
    list_line_name.append(str(i.get_numero()))

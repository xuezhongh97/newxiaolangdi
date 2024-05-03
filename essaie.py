import streamlit as st
from streamlit_folium import folium_static
import folium

# 创建地图对象，设置初始位置和缩放级别
m = folium.Map(location=[34.93619181, 112.3864124], zoom_start=15)

# 添加 Marker，使用 HTML 标签的加粗效果
folium.Marker(location=[34.93619181, 112.3864124], popup="<b>站点 A</b><br>这是一个示例站点。").add_to(m)

# 显示地图
folium_static(m)

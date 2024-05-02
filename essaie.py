import folium

# 创建地图对象，设置初始位置和缩放级别
m = folium.Map(location=[52.5200, 13.4050], zoom_start=12)  # 例如，以柏林为中心

# 定义路线的起点和终点坐标
route = [
    [52.5200, 13.4050],  # 起点坐标
    [52.5206, 13.4100],  # 途经点
    [52.5156, 13.3776]   # 终点坐标
]

# 在地图上添加折线
folium.PolyLine(route, color='blue', weight=5, opacity=0.8).add_to(m)

# 保存地图到 HTML 文件，或直接显示
m.save('route.html')  # 保存到文件
# 或直接在 Jupyter Notebook 中显示
# m

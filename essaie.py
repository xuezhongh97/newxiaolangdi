import streamlit as st

# 模拟选项卡的选项
tabs = ["Home", "Profile", "Settings"]

# 使用radio按钮在侧边栏创建选项卡效果
tab_selection = st.sidebar.radio("Tabs", tabs)

# 根据选项卡显示内容
if tab_selection == "Home":
    st.write("This is the Home tab content.")
elif tab_selection == "Profile":
    st.write("This is the Profile tab content.")
elif tab_selection == "Settings":
    st.write("This is the Settings tab content.")

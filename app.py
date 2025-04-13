import streamlit as st
import json
from datetime import datetime
import os

DATA_FILE = "cycle_info.json"

def get_exercise_recommendation(day, cycle_length, period_length=5):
    if day <= period_length:
        return "今天是经期，适合休息或做轻柔的瑜伽 🤍"
    elif day <= 14:
        return "你的能量正在上升！可以尝试慢跑、举铁等中强度运动 💪"
    elif day == 15:
        return "排卵期注意休息，但若感觉良好可以做些力量训练 🔥"
    elif day < cycle_length:
        return "进入黄体期，适合放松拉伸、散步或轻度有氧运动 🚶‍♀️"
    else:
        return "超出设定周期，请检查设定"

def load_cycle_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return None

def save_cycle_data(start_date, cycle_length):
    data = {
        "start_date": start_date,
        "cycle_length": cycle_length
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# 页面开始
st.set_page_config(page_title="你好，小悦", page_icon="🌼")
st.markdown("## 🌤️ 嗨，小悦")

data = load_cycle_data()

if data is None:
    st.markdown("### 📝 让我们从了解你开始")
    st.markdown("这是你第一次来吗？请告诉我你的月经周期信息，我会根据这些来陪你安排日常运动～")

    start_date = st.date_input("📅 请选择本次月经的第一天", value=datetime.today())
    cycle_length = st.number_input("🌀 你的月经周期长度是（天）", min_value=20, max_value=40, value=28)

    if st.button("✅ 保存并开始"):
        save_cycle_data(start_date.strftime("%Y-%m-%d"), int(cycle_length))
        st.success("记录好了！请刷新页面看看我为你准备的建议 💌")
else:
    start = datetime.strptime(data["start_date"], "%Y-%m-%d")
    cycle_len = int(data["cycle_length"])
    today = datetime.today()
    delta = (today - start).days
    day_in_cycle = (delta % cycle_len) + 1  # 第1天开始

    st.markdown(f"""
    ### 🌱 今天是你本周期的第 **{day_in_cycle} 天**
    {get_exercise_recommendation(day_in_cycle, cycle_len)}
    """)

    st.markdown("---")
    st.caption("✨ 我会每天根据你的周期阶段，温柔地给你贴心建议 🧘")

    with st.expander("🔧 想重新设置你的周期信息？"):
        if st.button("重新开始设置"):
            os.remove(DATA_FILE)
            st.warning("已清除记录，请刷新页面重新设置 🌸")
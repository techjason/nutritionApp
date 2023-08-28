import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="營養計算器 | 港大中風團隊", page_icon="🧠", layout="wide")

# This makes page look better, but it is unsafe
st.markdown('''<style>
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .css-1vq4p4l.e1fqkh3o4 {margin-top: -75px;}''', unsafe_allow_html=True)


image = Image.open('hkustrokelogo.png')

st.image(image, width=300)
st.title("🍉 營養計算器 🇭🇰")

@st.cache_data()
def traffic_light_color(value, low, medium, high):
    if value < low:
        return '#FF4B13'
    elif value < medium:
        return '#FFBE22 '
    else:
        return '#FF5151'
    

@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=0", "/export?format=csv")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["gsheets_url"])


# Search functionality
search_term = st.text_input("Search for a food item:")

selected_food = None

if search_term:
    mask = df['Food Item'].str.contains(search_term, na=False)
    filtered_df = df[mask]
    
    if not filtered_df.empty:
        st.write("Search Results:")
        for food_item in filtered_df['Food Item']:
            if st.button(food_item):
                selected_food = food_item
                break
if selected_food:
    # Display details for the selected food item
    food_details = df[df['Food Item'] == selected_food].iloc[0]

    # Display food name
    st.header(f"Details for {food_details['Food Item']}")

    # Display macronutrients using a circular ring chart
    st.subheader("常量營養素:")
    macros_values = [food_details['蛋白質 (g)'], food_details['脂肪 (g)'], food_details['碳水化合物 (g)']]
    macros_labels = ['蛋白質', '脂肪', '碳水化合物']
    colors = ['blue', 'green', 'orange']

    col1, col2, col3 = st.columns(3)
    

    with col1:
        fig, ax = plt.subplots(figsize=(3, 3), subplot_kw=dict(aspect="equal"))
        ax.pie(macros_values, colors=colors, startangle=90, wedgeprops=dict(width=0.3))
        plt.axis('off')  # Turn off the axis
        plt.gca().set_facecolor('none')  # Make the background transparent
        st.pyplot(fig, transparent=True)

    with col2:
        # Display the percentage values as text with corresponding colors
        total_macros = sum(macros_values)
        fat_percentage = food_details['脂肪 (g)'] / total_macros * 100
        sugar_percentage = food_details['添加糖 (g)'] / total_macros * 100
        sodium_percentage = food_details['鈉 (mg)'] / total_macros * 100

        # Warnings based on nutrition guidelines
        if fat_percentage > 30: # Assuming more than 30% fat is considered high
            st.error("警告: 此食品脂肪含量過高！")

        if sugar_percentage > 10: # Assuming more than 10% sugar is considered high
            st.error("警告: 此食品含糖量過高！")

        if sodium_percentage > 5: # Assuming more than 5% sodium is considered high
            st.error("警告: 此食品鈉含量過高！")

        st.title(f"卡路里: {food_details['卡路里']}")
        for label, value, color in zip(macros_labels, macros_values, colors):
            percentage = value / total_macros * 100
            st.markdown(f"<span style='color:{color};'>{label}: {percentage:.1f}%</span>", unsafe_allow_html=True)



    with col3:
    # Display micronutrients
        st.subheader("微量營養素:")
        micros = ['飽和脂肪 (g)', '反式脂肪 (g)', '添加糖 (g)', '鈉 (mg)', '磷 (mg)', '鉀 (mg)']
        traffic_light_rules = {
            '脂肪 (g)': (3, 17.5),
            '飽和脂肪 (g)': (1.5, 5),
            '添加糖 (g)': (5, 22.5),
            '鈉 (mg)': (300, 1500)
        }
        for nutrient, (low, medium) in traffic_light_rules.items():
            value = food_details[nutrient]
            color = traffic_light_color(value, low, medium, float('inf'))
            st.markdown(f"<span style='color:{color};'>{nutrient}: {value}</span>", unsafe_allow_html=True)

        # Explanation of the traffic light system
        st.caption("交通號誌系統解釋:")
        st.caption("綠色: 攝取量適中")
        st.caption("黃色: 攝取量輕微過高")
        st.caption("紅色: 攝取量超標")

#---------------------Setting up data-----------------------------
# @st.cache_data
# def get_data(str_data: str, num_data: str):    
#     df =  pd.read_csv(str_data)
#     df_num = pd.read_csv(num_data)
#     df_num = df_num.drop(index=0, columns="Food Item").astype(float)
#     df_num = df_num.reset_index(drop=True)
#     return df, df_num
# df, df_num = get_data("data/for_app.csv", "data/to_analyze.csv")
# to_show = ["Calories", "Prot (g)", "Fat (g)", "SatFat (g)", "TransFat (g)", "Carb (g)", "SugAdd (g)"]

# if "fil_cols" not in st.session_state:
#     st.session_state["fil_cols"] = []
#     st.session_state["col_ranges"] = []

# #--------------------Streamlit page--------------------------------

# col = st.columns([3,1,1])

# with col[0]:
#     st.markdown("# 營養食物 🥗")
#     st.markdown("🌮 Plan your diet intelligently 🍉☕")
#     st.markdown("Use the filters provided on the sidebar to find food items just right for you!")
#     st.markdown("##### Note:- Measurements are per 100g")
    
# with col[2]:
#     st.image("icon.png", width=200)

# with st.sidebar:
#     st.title("Choose your diet!")
    
#     filter_tab, cols_tab = st.tabs(["Filters", "Show Columns"])
    
#     with filter_tab:
#         fil_cols = st.session_state["fil_cols"]
#         col_ranges = st.session_state["col_ranges"]
        
#         no_of_rows = st.number_input("Max Rows to display", min_value=1, 
#                                      max_value=len(df), value=50, step=1)
#         search_text = st.text_input("Search food items by name", placeholder="Food name")
        
#         st.header("Add Filters")
        
#         default = "Nutrient List"
#         nt_list = df.columns.to_series()
#         nt_list[0] = default
#         fil_nut = st.selectbox("Select Nutrient", nt_list)
        
#         cols = st.columns(2)
#         with cols[0]:
#             min_value = st.number_input("Min", min_value=0., max_value=100_000., step=0.01)
#         with cols[1]:
#             max_value = st.number_input("Max", min_value=0., max_value=100_000., step=0.01)
            
#         if st.button("\\+ Add/Modify Filter", type="primary"):
#             if fil_nut not in [default]+fil_cols and min_value<=max_value:
#                 fil_cols.append(fil_nut)
#                 col_ranges.append([min_value, max_value])
                
#             elif min_value > max_value:
#                 st.warning("Min should be less than Max")
            
#             elif fil_nut in fil_cols:
#                 col_ranges[fil_cols.index(fil_nut)] = [min_value, max_value]
                
#         for i in range(len(fil_cols)):
#             if i >= len(fil_cols): break
#             rem_key = f"remove_{i}"
#             if rem_key in st.session_state and st.session_state[rem_key]:
#                 del fil_cols[i]
#                 del col_ranges[i]
#                 del st.session_state[rem_key]
        
#         for i in range(len(fil_cols)):
#             cols = st.columns([3,1])
#             cols[0].subheader(fil_cols[i])
#             cols[1].button(chr(10006), key=f"remove_{i}")                
            
#             cols = st.columns(2)
#             cols[0].caption(f"**Min:** {col_ranges[i][0]:.2f}")
#             cols[1].caption(f"**Max:** {col_ranges[i][1]:.2f}")
        
#     with cols_tab:
#         for col in df.columns:
#             if col == "Food Item": continue
#             if not st.checkbox(col, value=True if col in to_show else False):
#                 df = df.drop(columns=col)

# for col, [min, max] in zip(fil_cols, col_ranges):
#     cond = (df_num[col] >= min) & (df_num[col] <= max)
#     df = df[cond]
#     df_num = df_num[cond]

# if search_text:
#     search_text = search_text.lower().strip()
#     df = df[df["Food Item"].str.lower().str.contains(search_text)]
# df = df.iloc[:no_of_rows]
# df = df.reset_index(drop=True)
# df.index = df.index + 1
# st.table(df)
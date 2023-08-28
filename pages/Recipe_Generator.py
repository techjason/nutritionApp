import streamlit as st
import os
import openai

openai.api_key = st.secrets.openai_key


# # Streamlit UI
# st.title('中風患者的健康食譜推薦')

# # User Inputs
# people = st.number_input('您要為多少人烹飪？', min_value=1, max_value=10, value=1, step=1)
# time = st.slider('您有多少時間（以分鐘計）？', 5, 180, 30)
# skill_level = st.selectbox('您的烹飪技能等級是：', ['初學者', '中級', '高級'])
# ingredients = st.text_area('您手頭有哪些食材？（用逗號分隔）')

# # Generate button
# if st.button('獲取食譜推薦'):
#     # Base prompt
#     prompt = f"我需要一個適合中風患者的健康食譜，適合 {people} 人，我有 {time} 分鐘，我的烹飪技能等級是 {skill_level}。"

#     # Add ingredients to prompt if provided
#     if ingredients:
#         prompt += f" 我有以下食材：{ingredients}。"
    
#     prompt += " 請提供食材清單、製作指南、廚房工具、熱量、所需時間、技能等級和營養成分。"
    
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ],
#         temperature=0.6,
#         max_tokens=2000,

#     )
    
#     # Displaying the AI's response
#     st.subheader('食譜推薦：')
#     st.write(response.choices[0].message['content'])




# OpenAI API key setup

st.title('中風患者的健康食譜推薦')

# User Inputs
people = st.number_input('您要為多少人烹飪？', min_value=1, max_value=10, value=2, step=1)
time = st.slider('您有多少時間（以分鐘計）？', 5, 180, 30)
skill_level = st.selectbox('您的烹飪技能等級是：', ['初學者', '中級', '高級'])
ingredients = st.text_area('您手頭有哪些食材？（用逗號分隔） - 這是可選的，如果留空，它將自動建議要使用的食材')

# Generate button
if st.button('獲取食譜推薦'):
    # Base prompt
    prompt = f"我需要一個適合中風患者的健康食譜，適合 {people} 人，我有 {time} 分鐘，我的烹飪技能等級是 {skill_level}。"
    
    # Add ingredients to prompt if provided
    if ingredients:
        prompt += f" 我有以下食材：{ingredients}。"
    
    prompt += " 請提供食材清單、製作指南、廚房工具、熱量、所需時間、技能等級和營養成分。"
    
    res_box = st.empty()
    report = []
    # Looping over the response
    for resp in openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                            messages=[
                                                {
                                                    "role": "user",
                                                    "content": prompt
                                                }
                                            ],
                                            max_tokens=2000, 
                                            temperature=0.6,
                                            stream=True):
        # Join method to concatenate the elements of the list into a single string
        if 'content' in resp.choices[0]['delta']:
            report.append(resp.choices[0]['delta']['content'])
            result = "".join(report).strip()
            # result = result.replace("\n", "")        
            res_box.markdown(f'*{result}*') 

st.write('---')
st.info("有時AI可能會提供不准確的回應。")






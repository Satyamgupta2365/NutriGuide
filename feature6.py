import streamlit as st
from groq import Groq


api_key = "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"


client = Groq(api_key=api_key)

def get_condition_info(condition, time_period=None):
    messages = [
        {
            "role": "user",
            "content": (
                f"Provide detailed information for {condition}.\n"
                "1. Conditional-specific nutritional guidelines\n"
                "2. Customized meal planning. Include options for day, week, or month.\n"
                "3. Symptom management tips\n"
                "4. Educational content and lifestyle tips.\n"
                "Please format the response accordingly."
            )
        }
    ]

    if time_period:
        messages[0]["content"] += f"\nProvide meal planning for: {time_period}."

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
    )

    
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""
    return response_text


st.title("NutriGuide.AI - Chronic Condition Support")
st.header("Personalized Dietary Support for Chronic Conditions")


st.subheader("Select Your Chronic Condition:")
conditions = [
    "Diabetes", "Hypertension", "Cardiovascular Disease", "Obesity",
    "Fatty Liver", "Asthma", "Chronic Kidney Disease", "Osteoporosis",
    "GERD", "IBS"
]
condition = st.selectbox("Choose a condition:", conditions)


time_period = None
if condition != "Other":
    st.subheader("Meal Planning Duration")
    time_period = st.radio("Choose a meal planning duration:", ["Day", "Week", "Month"])


if st.button("Get Nutrition Plan and Advice"):
    if condition == "Other":
        condition = st.text_input("Please specify your condition:")

    if condition:
        st.info("Generating personalized recommendations... This may take a few moments.")
        response = get_condition_info(condition, time_period)
        st.success("Here's your personalized nutrition and lifestyle guidance:")
        st.write(response)
    else:
        st.warning("Please specify a chronic condition to continue.")

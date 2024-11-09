 
import streamlit as st
from groq import Groq


API_KEY = "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"  


client = Groq(api_key=API_KEY)


def get_meal_plan(age, sex, weight_goal, eating_habits, dietary_restrictions,intermittent_fast_timing ,traditional_diet,Duration):
    
    messages = [
        {
            "role": "user",
            "content": f"Write a personalized meal generation for the following parameters\n"
                       f"1. Age: {age}\n"
                       f"2. Sex: {sex}\n"
                       f"3. Weight goal: {weight_goal}\n"
                       f"4. Food eating habits: {eating_habits}\n"
                       f"5. Dietary restrictions: {dietary_restrictions}\n"
                       f"6. Intermittent fasting :{intermittent_fast_timing}\n"
                       f"7. Traditional diet: {traditional_diet}\n"
                       f"8. duration :{Duration}\n"
        },
        {
            "role": "assistant",
            "content": "dont inlucde to consult wiht dietictian message ,start with your personlized meal plan is\n"
                       "Provide a meal plan based on the above parametersand also include the cost of the meals in INR\n"
                       "make sure first the dish must be mentioned followed by ingeredints and its cost then approximation of entire dish\n"
                       "when its intermittent fasting make sure to take time which user provides\n"
                       "provide deatils of the paramter choosen by the user before giving the diet \n"

        }
    ]

    
    try:
        completion = client.chat.completions.create(
            model="llama-3.2-90b-text-preview",
            messages=messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,  
            stop=None,
        )

        
        meal_plan = completion.choices[0].message.content
        return meal_plan
    except Exception as e:
        return {"error": str(e)}


st.title("NutriGuide.AI - Personalized Meal Plan")
age = st.number_input("Enter your age:", min_value=0, max_value=120)
sex = st.selectbox("Select your sex:", ["Male", "Female", "Other"])
weight_goal = st.selectbox("Weight goal:", ["Gain", "Loss"])
eating_habits = st.selectbox("Eating habits:", ["Omnivore", "Flexitarian", "Pescatarian", "Vegetarian", "Vegan"])
dietary_restrictions = st.selectbox("Dietary restrictions:",["none", "mediterranean", "paleo", "whole30", 
                                    "low carb", "high carb", "gluten-free", "lactose-free", "raw food", "alkaline food"])
intermittent_fast_timing = st.selectbox( "Select your intermittent fasting schedule:", ["none","16/8", "18/6", "20/4"])

traditional_diet = st.selectbox ("Choose traditional diet:", ["none", "ayurvedic", "macrobiotic", "halal", "kosher"])
Duration = st.selectbox("The time period for which u want the meal plan:",["one day","one week","one month"])

if st.button("Get Meal Plan"):
    meal_plan = get_meal_plan(age, sex, weight_goal, eating_habits, dietary_restrictions.split(","),intermittent_fast_timing, traditional_diet.split(","),Duration.split(","))
    st.write(meal_plan) 

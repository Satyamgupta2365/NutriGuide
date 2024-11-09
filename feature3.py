import google.generativeai as genai
import streamlit as st
import os

api_key = "AIzaSyC4f-d-Igv6UWdHKoMgZcNfRTeQBFVgtUw"  
genai.configure(api_key=api_key)

if not os.path.exists("temp"):
    os.makedirs("temp")

st.title("Food Allergen Checker")
st.write("Check if a food dish contains any allergens you have or general allergens.")


food_item = st.text_input("Enter the food dish you want to check (e.g., Pizza):")


allergen = st.text_input("Enter any specific allergens if you have (optional) e.g., peanuts, garlic:")


image_file = st.file_uploader("Upload a photo of the food dish (optional):", type=["jpg", "jpeg", "png"])

if st.button("Check Allergens"):
    
    temp_image_path = None

    if food_item or image_file:
        
        prompt = ""

        if allergen:
            if food_item:
                prompt += f"The dish '{food_item}' is being analyzed. I am allergic to '{allergen}'. Does this dish contain my allergen? Please provide a simple 'yes', 'no', 'high probability', or 'low chances', and 4-5 lines of explanation and also warning about avoiding to use '{allergen} in the dish"
            if image_file:
                
                temp_image_path = os.path.join("temp", image_file.name)
                with open(temp_image_path, "wb") as f:
                    f.write(image_file.getbuffer())
                prompt += f"\nThis is the food '{temp_image_path}' I am going to eat. I am allergic to '{allergen}'. You don't have to determine the exact ingredients ,Just tell if generally the food dish can contain '{allergen}? First, give a one-word answer like 'Yes,' 'No,' 'May Contain,' or 'High Chance,' followed by a detailed explanation and also warning about avoiding to use '{allergen} in the dish."
        else:
            if food_item:
                prompt += f"Analyze the dish '{food_item}' for potential allergens. What ingredients might cause allergic reactions? Please provide a summary."
            if image_file:
                
                temp_image_path = os.path.join("temp", image_file.name)
                with open(temp_image_path, "wb") as f:
                    f.write(image_file.getbuffer())
                prompt += f"\nThis is the food '{temp_image_path}' I am going to eat. What ingredients might cause allergic reactions? Please provide a summary."

        
        if prompt:  
            model = genai.GenerativeModel("gemini-1.5-flash")
            try:
                if temp_image_path:  
                    myfile = genai.upload_file(temp_image_path)  
                    result = model.generate_content(
                        [
                            myfile,
                            "\n\n",
                            prompt,
                        ]
                    )
                else:
                    
                    result = model.generate_content(prompt)

                
            
                response_lines = result.text.splitlines()
                simple_response = response_lines[0] if response_lines else "No response received."
                explanation = "\n".join(response_lines[1:]) if len(response_lines) > 1 else ""

                
                if "yes" in simple_response.lower():
                    response_color = "#FF4D4D"  
                elif "high probability" in simple_response.lower():
                    response_color = "#FF4D4D"  
                elif "no" in simple_response.lower():
                    response_color = "#ADD8E6"  
                elif "low chances" in simple_response.lower():
                    response_color = "#B0E0E6"  
                else:
                    response_color = "#D3D3D3"  

                
                st.success("Allergen check completed!")
                st.markdown(
                    f"<div style='border: 2px solid {response_color}; padding: 10px; border-radius: 5px; background-color: {response_color};'>Response: {simple_response}</div>",
                    unsafe_allow_html=True
                )

                
                if explanation:
                    st.markdown(
                        f"<div style='border: 2px solid #2196F3; padding: 10px; border-radius: 5px;'><strong>Explanation:</strong><br>{result.text}</div>",
                        unsafe_allow_html=True
                    )

            except Exception as e:
                st.error(f"An error occurred during the allergen check: {e}")
        else:
            st.error("Unable to generate a prompt for the AI. Please check your inputs.")
    else:
        st.error("Please enter a food dish or upload a photo to check.")

    
    if temp_image_path and os.path.exists(temp_image_path):
        os.remove(temp_image_path)

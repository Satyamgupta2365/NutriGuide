import google.generativeai as genai
import streamlit as st
import os

api_key = "AIzaSyC4f-d-Igv6UWdHKoMgZcNfRTeQBFVgtUw"  
genai.configure(api_key=api_key)

if not os.path.exists("temp"):
    os.makedirs("temp")

st.title("Food Nutrient Analyzer")
st.write("Upload an image of food items, and we'll analyze the nutrient composition.")

image_file = st.file_uploader("Upload an image of food:", type=["jpg", "jpeg", "png"])

if image_file:
    temp_image_path = os.path.join("temp", image_file.name)
    with open(temp_image_path, "wb") as f:
        f.write(image_file.getbuffer())

    st.image(image_file, caption="Uploaded Image", use_column_width=True)
    if st.button("Analyze Nutrients"):
        try:
            myfile = genai.upload_file(temp_image_path)
            model = genai.GenerativeModel("gemini-1.5-flash")
            result = model.generate_content(
                [
                    myfile,
                    "\n\n",
                    """You are an expert nutritionist. Analyze the food dish or dishes in this image and provide a detailed breakdown of the nutrient composition, and you do not need to provide exact composition; you can give expected ranges including expected values for calories, protein, fats, carbohydrates, vitamins, and minerals. 
                    Provide the analysis in the following format in bullet points:
                    - Food Item: 
                      - Calories: X
                      - Protein: Yg
                      - Fats: Zg
                      - Carbohydrates: Ag
                      - Vitamins: [List]
                      - Minerals: [List]

                    
                      
                      
                    """
                ]
            )

            st.success("Nutrient analysis completed!")
            st.write(result.text)

            
            balance_result = model.generate_content(
                [
                    result.text,
                    "\n\n",
                    """See if the food is junk and having so many calories and not considered good for health and Based on the nutrient analysis provided, categorize the meal as and do not double bold:
                    - Not Healthy
                    -Healthy
                    -Nutritious
                    - Somewhat balanced
                    - Highly balanced and nutritious
                    Provide a short explanation for your assessment and if required give tips to make it more balanced.
                    """
                ]
            )

            
            st.markdown("<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>"
                        "<strong>Meal Balance Assessment:</strong><br>"
                        f"{balance_result.text}"
                        "</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")

    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)

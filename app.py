# ### Health Management APP
# from dotenv import load_dotenv

# load_dotenv() ## load all the environment variables

# import streamlit as st
# import os
# import google.generativeai as genai
# from PIL import Image

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ## Function to load Google Gemini Pro Vision API And get response

# def get_gemini_repsonse(input,image,prompt):
#     model=genai.GenerativeModel('gemini-2.0-flash-lite')
#     response=model.generate_content([input,image[0],prompt])
#     return response.text

# def input_image_setup(uploaded_file):
#     # Check if a file has been uploaded
#     if uploaded_file is not None:
#         # Read the file into bytes
#         bytes_data = uploaded_file.getvalue()

#         image_parts = [
#             {
#                 "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
#                 "data": bytes_data
#             }
#         ]
#         return image_parts
#     else:
#         raise FileNotFoundError("No file uploaded")
    
# ##initialize our streamlit app

# st.set_page_config(page_title="Gemini Health App")

# st.header("Gemini Health App")
# input=st.text_input("Input Prompt: ",key="input")
# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
# image=""   
# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image.", use_column_width=True)


# submit=st.button("Tell me the total calories")

# input_prompt="""
# You are an expert in nutritionist where you need to see the food items from the image
#                and calculate the total calories, also provide the details of every food items with calories intake
#                is below format

#                1. Item 1 - no of calories
#                2. Item 2 - no of calories
#                ----
#                ----


# """

# ## If submit button is clicked

# if submit:
#     image_data=input_image_setup(uploaded_file)
#     response=get_gemini_repsonse(input_prompt,image_data,input)
#     st.subheader("The Response is")
#     st.write(response)

from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import datetime

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Custom CSS for modern health app styling
def load_css():
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    }
    
    .title-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 3rem;
        margin: 2rem 0;
        border: 1px solid rgba(0, 0, 0, 0.3);
        text-align: center;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    .main-title {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: rgba(0, 0, 0, 0.7);
        font-size: 1.3rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    .feature-card {
        background: rgba(0, 0, 0, 0.9);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 40px rgba(31, 38, 135, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
    }
    
    .success-message {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .warning-message {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 30px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        margin: 0.5rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .health-stats {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .response-container {
        background: rgba(0,0, 0, 0.6);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        border-left: 6px solid #4ECDC4;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .nutrition-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: #333;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .goal-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: #333;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def get_health_prompts():
    return {
        "calorie_count": """
        You are an expert nutritionist. Analyze the food items in the image and provide:
        1. Total calories for the entire meal
        2. Detailed breakdown of each food item with calories
        3. Serving size estimation
        4. Nutritional category (healthy/moderate/high calorie)
        
        Format:
        **TOTAL CALORIES: XXX kcal**
        
        **Food Items:**
        1. Item 1 - XXX calories
        2. Item 2 - XXX calories
        
        **Nutritional Assessment:**
        [Brief assessment of the meal's nutritional value]
        """,
        
        "nutritional_analysis": """
        As a certified nutritionist, provide comprehensive nutritional analysis:
        1. Macronutrients breakdown (Carbs, Protein, Fat)
        2. Key vitamins and minerals present
        3. Fiber content estimation
        4. Sugar content assessment
        5. Sodium levels
        6. Overall nutritional score (1-10)
        7. Health benefits of this meal
        """,
        
        "diet_recommendations": """
        As a diet specialist, analyze the meal and provide:
        1. Is this meal suitable for weight loss/maintenance/gain?
        2. Recommendations for improving nutritional value
        3. What to add/remove for better balance
        4. Best time to consume this meal
        5. Portion size recommendations
        6. Alternative healthier options
        """,
        
        "meal_planning": """
        As a meal planning expert, suggest:
        1. What to eat before/after this meal for balance
        2. Daily meal plan incorporating this food
        3. Weekly meal prep suggestions
        4. Complementary foods for nutritional balance
        5. Hydration recommendations
        6. Exercise recommendations post-meal
        """,
        
        "health_warnings": """
        As a health advisor, identify:
        1. Any potential allergens in the food
        2. Foods to avoid for specific conditions (diabetes, hypertension, etc.)
        3. Overconsumption warnings
        4. Interaction with medications (general advice)
        5. Digestive considerations
        6. Special dietary considerations (vegan, keto, etc.)
        """,
        
        "fitness_integration": """
        As a fitness nutritionist, provide:
        1. Pre/post workout meal assessment
        2. Calories burned equivalent exercises
        3. Muscle building/recovery benefits
        4. Energy levels impact
        5. Performance enhancement suggestions
        6. Recovery meal recommendations
        """
    }

def calculate_bmi(weight, height):
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        category = "Underweight"
        color = "#FF6B6B"
    elif bmi < 25:
        category = "Normal"
        color = "#4ECDC4"
    elif bmi < 30:
        category = "Overweight"
        color = "#FFE66D"
    else:
        category = "Obese"
        color = "#FF6B6B"
    
    return bmi, category, color

def main():
    st.set_page_config(
        page_title="AI Health & Nutrition Analyzer",
        page_icon="🍎",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    load_css()
    
    # Header
    st.markdown("""
    <div class="title-container">
        <h1 class="main-title">🍎 AI Health & Nutrition Analyzer</h1>
        <p class="subtitle">Your Personal AI Nutritionist & Health Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'daily_calories' not in st.session_state:
        st.session_state.daily_calories = 0
    if 'meals_analyzed' not in st.session_state:
        st.session_state.meals_analyzed = 0
    if 'health_goals' not in st.session_state:
        st.session_state.health_goals = {}
    
    # Sidebar - Health Profile
    with st.sidebar:
        st.markdown("### 👤 Health Profile")
        
        # Basic Info
        age = st.number_input("Age", min_value=10, max_value=120, value=25)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
        
        # Calculate BMI
        if weight and height:
            bmi, category, color = calculate_bmi(weight, height)
            st.markdown(f"""
            <div class="metric-card">
                <h4>BMI Calculator</h4>
                <h2 style="color: white;">{bmi:.1f}</h2>
                <p style="color: {color}; font-weight: bold; background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 10px;">{category}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Activity Level
        activity_level = st.selectbox(
            "Activity Level",
            ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"]
        )
        
        # Health Goals
        st.markdown("### 🎯 Health Goals")
        goal = st.selectbox(
            "Primary Goal",
            ["Weight Loss", "Weight Maintenance", "Weight Gain", "Muscle Building", "General Health"]
        )
        
        # Daily Stats
        st.markdown("### 📊 Today's Stats")
        st.markdown(f"""
        <div class="health-stats">
            <p><strong>Calories Tracked:</strong> {st.session_state.daily_calories}</p>
            <p><strong>Meals Analyzed:</strong> {st.session_state.meals_analyzed}</p>
            <p><strong>Date:</strong> {datetime.date.today()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Reset button
        if st.button("🔄 Reset Daily Stats"):
            st.session_state.daily_calories = 0
            st.session_state.meals_analyzed = 0
            st.success("Stats reset!")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 📸 Food Image Analysis")
        
        # Image upload
        uploaded_file = st.file_uploader(
            "Upload your food image:",
            type=["jpg", "jpeg", "png"],
            help="Take a clear photo of your meal for accurate analysis"
        )
        
        # Custom input
        custom_input = st.text_area(
            "Additional Information (Optional):",
            placeholder="Specify serving size, ingredients, cooking method, or any other details...",
            height=100
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Your meal is ready for analysis! 🍽️", use_column_width=True)
            
            st.markdown("""
            <div class="success-message">
                ✅ Image uploaded successfully! Choose an analysis type below.
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Quick Settings")
        
        # Meal type
        meal_type = st.selectbox(
            "Meal Type:",
            ["Breakfast", "Lunch", "Dinner", "Snack", "Pre-workout", "Post-workout"]
        )
        
        # Diet preferences
        diet_type = st.multiselect(
            "Dietary Preferences:",
            ["Vegetarian", "Vegan", "Keto", "Paleo", "Low-carb", "Gluten-free", "Dairy-free"]
        )
        
        # Health conditions
        health_conditions = st.multiselect(
            "Health Considerations:",
            ["Diabetes", "Hypertension", "Heart Disease", "Food Allergies", "None"]
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis buttons
    st.markdown("### 🔍 Choose Your Analysis")
    
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    
    with col1:
        submit1 = st.button("🔥 Calorie Counter", key="calories")
    with col2:
        submit2 = st.button("📊 Nutrition Analysis", key="nutrition")
    with col3:
        submit3 = st.button("💡 Diet Recommendations", key="diet")
    with col4:
        submit4 = st.button("📅 Meal Planning", key="planning")
    with col5:
        submit5 = st.button("⚠️ Health Warnings", key="warnings")
    with col6:
        submit6 = st.button("💪 Fitness Integration", key="fitness")
    
    # Get prompts
    prompts = get_health_prompts()
    
    # Analysis function
    def perform_analysis(prompt_key, title, icon):
        if uploaded_file is not None:
            with st.spinner(f"Analyzing your meal... {icon}"):
                try:
                    image_data = input_image_setup(uploaded_file)
                    
                    # Add context to prompt
                    context = f"\nMeal Type: {meal_type}\nDiet Preferences: {', '.join(diet_type) if diet_type else 'None'}\nHealth Considerations: {', '.join(health_conditions) if health_conditions else 'None'}\nAdditional Info: {custom_input if custom_input else 'None'}"
                    
                    response = get_gemini_response(prompts[prompt_key] + context, image_data, custom_input)
                    
                    st.markdown(f"""
                    <div class="response-container">
                        <h3>{icon} {title}</h3>
                        {response}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Update stats
                    st.session_state.meals_analyzed += 1
                    if prompt_key == "calorie_count":
                        # Extract calories (simplified - you might want to improve this)
                        try:
                            import re
                            calorie_match = re.search(r'(\d+)\s*kcal', response)
                            if calorie_match:
                                calories = int(calorie_match.group(1))
                                st.session_state.daily_calories += calories
                        except:
                            pass
                    
                    st.success("✅ Analysis completed successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
        else:
            st.markdown("""
            <div class="warning-message">
                📸 Please upload a food image first!
            </div>
            """, unsafe_allow_html=True)
    
    # Handle button clicks
    if submit1:
        perform_analysis("calorie_count", "Calorie Analysis", "🔥")
    elif submit2:
        perform_analysis("nutritional_analysis", "Nutritional Breakdown", "📊")
    elif submit3:
        perform_analysis("diet_recommendations", "Diet Recommendations", "💡")
    elif submit4:
        perform_analysis("meal_planning", "Meal Planning Suggestions", "📅")
    elif submit5:
        perform_analysis("health_warnings", "Health Considerations", "⚠️")
    elif submit6:
        perform_analysis("fitness_integration", "Fitness Integration", "💪")
    
    # Health tips section
    st.markdown("### 💡 Daily Health Tips")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="nutrition-card">
            <h4>🥗 Nutrition Tip</h4>
            <p>Include colorful vegetables in every meal for diverse nutrients and antioxidants.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="nutrition-card">
            <h4>💧 Hydration</h4>
            <p>Drink water before meals to aid digestion and help control portion sizes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="nutrition-card">
            <h4>⏰ Timing</h4>
            <p>Eat your largest meal when you're most active to optimize energy usage.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: rgba(0,0,0,0.6); padding: 2rem;">
        <p>🍎 Stay healthy with AI-powered nutrition insights | Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Nutrition Engine", layout="wide")

st.title("🥗 AI Nutrition Engine")
st.caption("Personalized Indian Nutrition Planner")

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("clean_food_dataset.csv")

# =========================
# SIDEBAR USER INPUT
# =========================
st.sidebar.header("👤 User Profile")

body_type = st.sidebar.selectbox(
    "Body Type",
    ["Ectomorph", "Mesomorph", "Endomorph"]
)

activity_level = st.sidebar.selectbox(
    "Activity Level",
    ["Low", "Medium", "High"]
)

diet_type = st.sidebar.selectbox(
    "Diet Preference",
    ["Vegetarian", "Vegan", "Non-Vegetarian", "Bengali Diet"]
)

calories_target = st.sidebar.number_input(
    "Daily Calories",
    1200,
    4000,
    2000
)

st.sidebar.markdown("---")
st.sidebar.info("AI builds your nutrition plan based on dataset")

# =========================
# HELPER FUNCTION
# =========================
def get_foods(max_cal):
    filtered = df[df["calories"] <= max_cal]
    return filtered.sample(min(10, len(filtered)))

# =========================
# MEAL PLAN GENERATOR
# =========================
st.subheader("🍱 AI Meal Plan Generator")

if st.button("Generate Meal Plan"):

    breakfast = get_foods(calories_target * 0.3)
    lunch = get_foods(calories_target * 0.4)
    dinner = get_foods(calories_target * 0.3)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🌅 Breakfast")
        st.dataframe(breakfast[["food_name", "calories", "protein", "carbs", "fat"]])

    with col2:
        st.markdown("### 🍛 Lunch")
        st.dataframe(lunch[["food_name", "calories", "protein", "carbs", "fat"]])

    with col3:
        st.markdown("### 🌙 Dinner")
        st.dataframe(dinner[["food_name", "calories", "protein", "carbs", "fat"]])

# =========================
# MACRO CALCULATOR
# =========================
st.subheader("📊 Macro Breakdown")

if st.button("Calculate Macros"):

    protein = calories_target * 0.3 / 4
    carbs = calories_target * 0.4 / 4
    fat = calories_target * 0.3 / 9

    col1, col2, col3 = st.columns(3)

    col1.metric("Protein (g)", round(protein, 2))
    col2.metric("Carbs (g)", round(carbs, 2))
    col3.metric("Fat (g)", round(fat, 2))

# =========================
# SMART FOOD SEARCH
# =========================
st.subheader("🔍 Smart Food Search")

query = st.text_input("Search food (e.g. rice, tea, curry)")

if st.button("Search Food"):

    result = df[df["food_name"].str.contains(query, case=False, na=False)]

    if len(result) == 0:
        st.warning("No food found")
    else:
        st.dataframe(result[["food_name", "calories", "protein", "carbs", "fat"]])
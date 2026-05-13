import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="AI Nutrition Engine", layout="wide")

st.title("🥗 AI Nutrition Engine (Streamlit Only Demo)")
st.caption("No backend needed — fully working prototype")

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("clean_food_dataset.csv")

# =========================
# SIDEBAR USER INPUT
# =========================
st.sidebar.header("👤 User Profile")

body_type = st.sidebar.selectbox("Body Type", ["Ectomorph", "Mesomorph", "Endomorph"])
activity_level = st.sidebar.selectbox("Activity Level", ["Low", "Medium", "High"])
diet_type = st.sidebar.selectbox("Diet Preference", ["Vegetarian", "Vegan", "Non-Vegetarian", "Bengali Diet"])

calories_target = st.sidebar.number_input("Daily Calories", 1200, 4000, 2000)

st.sidebar.markdown("---")
st.sidebar.info("AI adapts nutrition plan based on dataset")

# =========================
# FILTER FUNCTION
# =========================
def get_foods(max_cal):
    return df[df["calories"] <= max_cal].sample(min(10, len(df)))

# =========================
# MEAL PLAN GENERATOR
# =========================
st.subheader("🍱 AI Meal Plan Generator (Demo)")

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

    st.metric("Protein (g)", round(protein, 2))
    st.metric("Carbs (g)", round(carbs, 2))
    st.metric("Fat (g)", round(fat, 2))


# =========================
# SMART FOOD SEARCH
# =========================
st.subheader("🔍 Smart Food Search")

query = st.text_input("Search food")

if st.button("Search"):

    result = df[df["food_name"].str.contains(query, case=False, na=False)]

    if len(result) == 0:
        st.warning("No food found")
    else:
        st.dataframe(result[["food_name", "calories", "protein", "carbs", "fat"]])


# =========================
# FOOD SCANNER (SIMULATED)
# =========================
st.subheader("📷 Smart Food Scanner (Demo)")

food_input = st.text_input("Enter food name (simulate image scan)")

if st.button("Scan Food"):

    match = df[df["food_name"].str.contains(food_input, case=False, na=False)]

   
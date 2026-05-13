import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Nutrition Engine", layout="wide")

st.title("🥗 AI Nutrition Engine")
st.caption("Personalized Indian Diet Planner + Smart AI Food System")

# =========================
# SIDEBAR - USER PROFILE
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

goal = st.sidebar.selectbox(
    "Fitness Goal",
    ["Fat Loss", "Muscle Gain", "Maintenance"]
)

calories = st.sidebar.number_input(
    "Daily Calorie Target",
    min_value=1200,
    max_value=4000,
    value=2000
)

st.sidebar.markdown("---")
st.sidebar.info("AI adapts meal plans based on your profile ⚡")


# =========================
# MEAL PLAN GENERATOR
# =========================
st.markdown("## 🍱 AI Meal Planner")

if st.button("Generate Meal Plan"):

    res = requests.get(
        f"{BASE_URL}/meal-plan",
        params={
            "goal": goal,
            "diet": diet_type,
            "calories": calories
        }
    )

    data = res.json()

    st.success("Your Personalized Meal Plan is Ready 🎯")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🌅 Breakfast")
        for item in data["meal_plan"]["breakfast"]:
            st.write(f"🍽 {item['food_name']} ({item['calories']} kcal)")

    with col2:
        st.subheader("🍛 Lunch")
        for item in data["meal_plan"]["lunch"]:
            st.write(f"🍽 {item['food_name']} ({item['calories']} kcal)")

    with col3:
        st.subheader("🌙 Dinner")
        for item in data["meal_plan"]["dinner"]:
            st.write(f"🍽 {item['food_name']} ({item['calories']} kcal)")


# =========================
# MACRO BREAKDOWN
# =========================
st.markdown("---")
st.markdown("## 📊 Macro Breakdown")

if st.button("Calculate Macros"):

    res = requests.get(f"{BASE_URL}/macros", params={"calories": calories})
    data = res.json()

    col1, col2, col3 = st.columns(3)

    col1.metric("Protein (g)", data["protein_g"])
    col2.metric("Carbs (g)", data["carbs_g"])
    col3.metric("Fat (g)", data["fat_g"])


# =========================
# SMART FOOD SEARCH (FIXED UI)
# =========================
st.markdown("---")
st.markdown("## 🔍 Smart Food Search")

query = st.text_input("Search food (e.g. tea, rice, curry)")

if st.button("Search Food"):

    res = requests.get(f"{BASE_URL}/search", params={"query": query})
    data = res.json()

    if not data:
        st.warning("No food found 😔 Try another keyword")
    else:
        for food in data:
            with st.container():
                st.markdown(f"### 🍽 {food['food_name']}")
                st.write(f"🔥 Calories: {food['calories']} kcal")
                st.write(f"💪 Protein: {food['protein']} g")
                st.write(f"🍞 Carbs: {food['carbs']} g")
                st.write(f"🧈 Fat: {food['fat']} g")
                st.divider()


# =========================
# FOOD SCANNER (SIMULATED)
# =========================
st.markdown("---")
st.markdown("## 📷 Smart Food Scanner (Demo)")

food_item = st.text_input("Enter food item (simulate image scan)")

if st.button("Scan Food"):

    res = requests.get(f"{BASE_URL}/scan-food", params={"item": food_item})
    data = res.json()

    if "message" in data:
        st.error(data["message"])
    else:
        st.success("Food Detected!")

        st.markdown(f"### 🍽 {data['detected_food']}")
        st.write(f"🔥 Calories: {data['calories']}")
        st.write(f"💪 Protein: {data['protein']}")
        st.write(f"🍞 Carbs: {data['carbs']}")
        st.write(f"🧈 Fat: {data['fat']}")


# =========================
# ADAPTIVE ENGINE
# =========================
st.markdown("---")
st.markdown("## 🧠 Adaptive AI Engine")

if st.button("Run Adaptive Engine"):

    res = requests.get(f"{BASE_URL}/adaptive-plan")
    data = res.json()

    st.success("AI Adjusted Your Plan")

    st.metric("Adjusted Calories", data["adjusted_calories"])
    st.info(data["reasoning"])
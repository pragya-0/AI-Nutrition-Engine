from fastapi import FastAPI
import pandas as pd
import random

app = FastAPI()

# Load dataset
df = pd.read_csv("clean_food_dataset.csv")


# =========================
# BASIC ENDPOINTS (KEEP)
# =========================

@app.get("/")
def home():
    return {"message": "AI Nutrition Engine Running 🚀"}


@app.get("/foods")
def foods():
    return df.to_dict(orient="records")


@app.get("/search")
def search(query: str):
    result = df[df["food_name"].str.contains(query, case=False, na=False)]
    return result.to_dict(orient="records")


@app.get("/recommend")
def recommend(max_calories: float = 200):
    result = df[df["calories"] <= max_calories]
    return result.sample(min(5, len(result))).to_dict(orient="records")


# =========================
# AI FEATURE 1: MACRO ENGINE
# =========================

@app.get("/macros")
def macros(calories: int = 2000):

    protein = (calories * 0.25) / 4
    carbs = (calories * 0.50) / 4
    fat = (calories * 0.25) / 9

    return {
        "calories": calories,
        "protein_g": round(protein, 2),
        "carbs_g": round(carbs, 2),
        "fat_g": round(fat, 2)
    }


# =========================
# AI FEATURE 2: MEAL PLAN GENERATOR
# =========================

@app.get("/meal-plan")
def meal_plan(goal: str = "fat_loss", diet: str = "veg", calories: int = 2000):

    foods = df.copy()

    # Simple filtering logic
    low_cal_foods = foods[foods["calories"] <= 400]

    if len(low_cal_foods) < 6:
        low_cal_foods = foods

    breakfast = low_cal_foods.sample(2).to_dict(orient="records")
    lunch = low_cal_foods.sample(2).to_dict(orient="records")
    dinner = low_cal_foods.sample(2).to_dict(orient="records")

    return {
        "goal": goal,
        "diet": diet,
        "target_calories": calories,
        "meal_plan": {
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner
        }
    }


# =========================
# AI FEATURE 3: SMART FOOD SCANNER (SIMULATED)
# =========================

@app.get("/scan-food")
def scan_food(item: str):

    result = df[df["food_name"].str.contains(item, case=False, na=False)]

    if result.empty:
        return {"message": "Food not found"}

    food = result.iloc[0]

    return {
        "detected_food": food["food_name"],
        "calories": float(food["calories"]),
        "protein": float(food["protein"]),
        "carbs": float(food["carbs"]),
        "fat": float(food["fat"])
    }


# =========================
# AI FEATURE 4: ADAPTIVE ENGINE (BASIC VERSION)
# =========================

user_state = {
    "steps": 8000,
    "workouts": 3,
    "weight_change": -0.5
}


@app.get("/adaptive-plan")
def adaptive_plan():

    base_calories = 2000

    if user_state["steps"] > 10000:
        base_calories += 200

    if user_state["workouts"] >= 4:
        base_calories += 150

    if user_state["weight_change"] > 1:
        base_calories -= 200

    return {
        "adjusted_calories": base_calories,
        "reasoning": "Based on steps, workouts, and weight change"
    }
import pandas as pd

# Load dataset
df = pd.read_csv("Indian_Food_Nutrition_Processed.csv")

# Show columns (debug step)
print("Original Columns:")
print(df.columns)

# Remove duplicates
df = df.drop_duplicates()

# Remove empty rows
df = df.dropna()

# Rename columns to standard format (VERY IMPORTANT for AI system)
df = df.rename(columns={
    "Dish Name": "food_name",
    "Calories (kcal)": "calories",
    "Carbohydrates (g)": "carbs",
    "Protein (g)": "protein",
    "Fats (g)": "fat"
})

# Keep only required columns for your AI engine
df = df[["food_name", "calories", "carbs", "protein", "fat"]]

# Save cleaned dataset
df.to_csv("clean_food_dataset.csv", index=False)

# Preview
print("\nCleaned Data Preview:")
print(df.head())
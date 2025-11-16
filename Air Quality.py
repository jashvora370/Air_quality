# Smart Air Quality Analysis & Visualization System
# Libraries Used:
# - tkinter : For GUI
# - pandas : For data handling
# - matplotlib : For data visualization

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("air_quality_data.csv")

# Data Cleaning
data.dropna(subset=["city", "pollutant_id", "pollutant_avg"], inplace=True)
data.drop_duplicates(inplace=True)
data["pollutant_avg"] = pd.to_numeric(data["pollutant_avg"], errors="coerce")

# Display dataset info
print("Dataset Loaded Successfully!")
print("Number of Rows and Columns:", data.shape)
print("\nColumns in Dataset:")
print(list(data.columns))
print("\nFirst 5 Rows:")
print(data.head())

# Check required columns
required_columns = {"city", "pollutant_id", "pollutant_avg"}
if not required_columns.issubset(data.columns):
    messagebox.showerror("Error", "Dataset missing required columns!")

# Get list of unique cities
cities = sorted(data["city"].unique())

# Analyze selected city
def analyze_city():
    selected_city = city_var.get()
    if not selected_city:
        messagebox.showwarning("Warning", "Please select a city.")
        return

    city_data = data[data["city"] == selected_city]
    if city_data.empty:
        messagebox.showinfo("Info", "No data available for this city.")
        return

    pollutant_summary = city_data.groupby("pollutant_id")["pollutant_avg"].mean()
    avg_aqi = pollutant_summary.mean()

    # Air quality status
    if avg_aqi <= 50:
        status = "Good"
        advice = "Air quality is good. Enjoy outdoor activities."
    elif avg_aqi <= 100:
        status = "Moderate"
        advice = "Air quality is acceptable. Sensitive people should limit outdoor activity."
    elif avg_aqi <= 200:
        status = "Poor"
        advice = "Air quality is unhealthy. People with breathing issues should stay indoors."
    else:
        status = "Severe"
        advice = "Hazardous air quality. Avoid going outdoors."

    # Last updated date (supporting two common column names)
    if "last_update" in data.columns:
        last_update = city_data["last_update"].iloc[-1]
    elif "Last Updated" in data.columns:
        last_update = city_data["Last Updated"].iloc[-1]
    else:
        last_update = "Not Available"

    # Show result in GUI
    result_label.config(
        text=f"City: {selected_city}\nAverage AQI: {avg_aqi:.2f}\nStatus: {status}\nLast Updated: {last_update}"
    )
    advice_label.config(text=f"Health Advice: {advice}")

    # --- Bar Graph ---
    plt.figure(figsize=(6, 4))
    pollutant_summary.plot(kind="bar", color="lightblue", edgecolor="black")
    plt.title(f"Pollutant Levels in {selected_city}")
    plt.xlabel("Pollutant Type")
    plt.ylabel("Average Concentration")
    plt.tight_layout()
    plt.show()

    # --- Pie Chart (composition) ---
    plt.figure(figsize=(5, 5))
    pollutant_summary.plot(kind="pie", autopct="%1.1f%%", startangle=90)
    plt.title(f"Pollutant Composition in {selected_city}")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()

# Top 5 Polluted Cities
def show_top_cities():
    top_cities = (
        data.groupby("city")["pollutant_avg"].mean().sort_values(ascending=False).head(5)
    )
    plt.figure(figsize=(6, 4))
    top_cities.plot(kind="bar", color="tomato", edgecolor="black")
    plt.title("Top 5 Most Polluted Cities")
    plt.xlabel("City")
    plt.ylabel("Average AQI Level")
    plt.tight_layout()
    plt.show()

# Top 5 Cleanest Cities
def show_clean_cities():
    clean_cities = (
        data.groupby("city")["pollutant_avg"].mean().sort_values(ascending=True).head(5)
    )
    plt.figure(figsize=(6, 4))
    clean_cities.plot(kind="bar", color="lightgreen", edgecolor="black")
    plt.title("Top 5 Cleanest Cities (Lowest Pollution)")
    plt.xlabel("City")
    plt.ylabel("Average AQI Level")
    plt.tight_layout()
    plt.show()

# Pollutant Info
def show_pollutant_info():
    info = (
        "Common Air Pollutants and Their Effects:\n\n"
        "PM2.5 - Fine particles that affect lungs and heart.\n"
        "PM10 - Larger dust particles that irritate eyes and throat.\n"
        "NO2 - Causes breathing difficulties and asthma.\n"
        "SO2 - Affects respiratory system and causes coughing.\n"
        "O3 (Ozone) - Triggers asthma attacks and chest pain.\n"
        "CO - Reduces oxygen in the blood and is harmful to the heart."
    )
    messagebox.showinfo("Pollutant Information", info)

# --- AUTOCOMPLETE: function to update combobox suggestions as user types ---
def on_keyrelease(event):
    # Get current text from combobox
    value = event.widget.get()
    value = value.strip().lower()

    # If empty, show full list
    if value == '':
        data_list = cities
    else:
        # Filter cities containing the typed string (case-insensitive)
        data_list = [item for item in cities if value in item.lower()]

    # Update combobox values with the filtered list
    city_menu['values'] = data_list

    # Optionally open the dropdown list to show suggestions if there are matches
    if data_list:
        try:
            city_menu.event_generate('<Down>')
        except Exception:
            pass

# Tkinter GUI
root = tk.Tk()
root.title("Smart Air Quality Analysis System")
root.geometry("540x440")

# Title
title_label = tk.Label(root, text="Smart Air Quality Analysis System", font=("Arial", 14, "bold"), bg="lightyellow")
title_label.pack(pady=10)

# Dropdown with autocomplete enabled (user may type)
city_var = tk.StringVar()
city_label = tk.Label(root, text="Select City:", font=("Arial", 11), bg="lightblue")
city_label.pack()
# Note: state="readonly" removed so user can type; values filled from 'cities'
city_menu = ttk.Combobox(root, textvariable=city_var, values=cities, width=35)
city_menu.pack(pady=5)

# Bind key release event to combobox for type-ahead behavior
city_menu.bind('<KeyRelease>', on_keyrelease)

# Buttons
analyze_btn = tk.Button(root, text="Analyze City", command=analyze_city, bg="lightgreen", width=20)
analyze_btn.pack(pady=8)
top_btn = tk.Button(root, text="Show Top 5 Polluted Cities", command=show_top_cities, bg="lightcoral", width=25)
top_btn.pack(pady=8)
clean_btn = tk.Button(root, text="Show Top 5 Cleanest Cities", command=show_clean_cities, bg="lightgreen", width=25)
clean_btn.pack(pady=8)
info_btn = tk.Button(root, text="View Pollutant Information", command=show_pollutant_info, bg="lightblue", width=25)
info_btn.pack(pady=8)

# Labels
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="white")
result_label.pack(pady=10)
advice_label = tk.Label(root, text="", font=("Arial", 11), wraplength=460, bg="white")
advice_label.pack(pady=10)

# Run GUI
root.mainloop()

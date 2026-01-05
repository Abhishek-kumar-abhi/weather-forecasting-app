import requests
import tkinter as tk
from tkinter import messagebox
import datetime
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# 🔐 API Key and URL (Get your API key from OpenWeatherMap)
API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')


def get_weather():
    """Fetches weather information for the given city using OpenWeatherMap API."""
    city_name = city_entry.get()
    if not city_name:
        messagebox.showerror("Input Error", "Please enter a city name!")
        return

    try:
        # Step 1: Send a request to the API with the city name
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric'  # Get temperature in Celsius (use 'imperial' for Fahrenheit)
        }
        response = requests.get(BASE_URL, params=params)

        # Step 2: Check if the response is successful
        if response.status_code == 200:
            data = response.json()

            # Extract weather details from the JSON response
            city = data['name']
            country = data['sys']['country']
            temperature = data['main']['temp']
            feels_like = data['main']['feels_like']
            min_temp = data['main']['temp_min']
            max_temp = data['main']['temp_max']
            humidity = data['main']['humidity']
            visibility = data['visibility'] / 1000  # Convert from meters to km
            weather_description = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            clouds = data['clouds']['all']  # Cloudiness in percentage
            sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p')
            sunset = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p')

            # Display the weather information in the labels
            result_label.config(text=f"🌤️  Weather Forecast for {city} ({country})")
            weather_info_label.config(
                text=f"🌡️ Temperature: {temperature}°C (Min: {min_temp}°C, Max: {max_temp}°C)\n"
                     f"🥵 Feels Like: {feels_like}°C\n"
                     f"🌤️ Sky: {weather_description.capitalize()}\n"
                     f"💧 Humidity: {humidity}%\n"
                     f"💨 Wind Speed: {wind_speed} m/s\n"
                     f"☁️ Cloud Cover: {clouds}%\n"
                     f"🔎 Visibility: {visibility} km\n"
                     f"🌅 Sunrise: {sunrise}\n"
                     f"🌇 Sunset: {sunset}"
            )

        elif response.status_code == 404:
            messagebox.showerror("City Not Found", "City not found. Please check the city name and try again.")
        else:
            messagebox.showerror("Error", f"Something went wrong. Error code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Connection Error", f"An error occurred: {e}")


def clear_fields():
    """Clears the city input and weather information."""
    city_entry.delete(0, tk.END)
    result_label.config(text="")
    weather_info_label.config(text="")


# 🔥 Create the main window
root = tk.Tk()
root.title("🌦️ Weather Forecast App")
root.geometry("400x500")
root.configure(bg="#2F4F4F")  # Dark slate gray background

# 🌇 Title Label
title_label = tk.Label(root, text="Weather Forecast App", font=("Helvetica", 18, "bold"), bg="#2F4F4F", fg="white")
title_label.pack(pady=10)

# 🏙️ City Input Field
city_entry_label = tk.Label(root, text="Enter City Name:", font=("Helvetica", 12), bg="#2F4F4F", fg="white")
city_entry_label.pack(pady=5)

city_entry = tk.Entry(root, font=("Helvetica", 14), width=20, justify='center')
city_entry.pack(pady=5)

# 🔘 Buttons for Get Weather and Clear
button_frame = tk.Frame(root, bg="#2F4F4F")
button_frame.pack(pady=10)

get_weather_button = tk.Button(button_frame, text="Get Weather", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", command=get_weather)
get_weather_button.pack(side="left", padx=10)

clear_button = tk.Button(button_frame, text="Clear", font=("Helvetica", 12, "bold"), bg="#f44336", fg="white", command=clear_fields)
clear_button.pack(side="left", padx=10)

# 📝 Labels to Display Weather Information
result_label = tk.Label(root, text="", font=("Helvetica", 14, "bold"), bg="#2F4F4F", fg="white", wraplength=380)
result_label.pack(pady=20)

weather_info_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#2F4F4F", fg="white", justify="left", wraplength=380)
weather_info_label.pack()

# 🚀 Run the application
root.mainloop()

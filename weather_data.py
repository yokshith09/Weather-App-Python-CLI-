import requests
import time
import os

API_KEY = "636e07cc7ada70a84e0e266b0dede53a"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

DUMMY_WEATHER = {
    "delhi": {"temp": 35, "description": "Hot and sunny", "humidity": 40, "feels_like": 36, "wind_speed": 5},
    "mumbai": {"temp": 30, "description": "Humid and cloudy", "humidity": 70, "feels_like": 32, "wind_speed": 3},
    "bangalore": {"temp": 25, "description": "Pleasant and cloudy", "humidity": 60, "feels_like": 25, "wind_speed": 4},
    "chennai": {"temp": 34, "description": "Humid and sunny", "humidity": 70, "feels_like": 35, "wind_speed": 6},
    "kolkata": {"temp": 33, "description": "Warm and cloudy", "humidity": 65, "feels_like": 34, "wind_speed": 5},
    "hyderabad": {"temp": 32, "description": "Sunny", "humidity": 55, "feels_like": 33, "wind_speed": 4},
    "pune": {"temp": 28, "description": "Mild and sunny", "humidity": 50, "feels_like": 28, "wind_speed": 3},
    "ahmedabad": {"temp": 37, "description": "Hot and dry", "humidity": 35, "feels_like": 39, "wind_speed": 7},
    "jaipur": {"temp": 38, "description": "Hot and sunny", "humidity": 30, "feels_like": 40, "wind_speed": 6},
    "lucknow": {"temp": 34, "description": "Warm and humid", "humidity": 60, "feels_like": 35, "wind_speed": 5},
    "coimbatore": {"temp": 29, "description": "Partly cloudy", "humidity": 60, "feels_like": 29, "wind_speed": 4},
    "surat": {"temp": 33, "description": "Warm and humid", "humidity": 70, "feels_like": 34, "wind_speed": 5},
    "kanpur": {"temp": 35, "description": "Hot and sunny", "humidity": 40, "feels_like": 36, "wind_speed": 5},
    "nagpur": {"temp": 34, "description": "Hot and dry", "humidity": 30, "feels_like": 35, "wind_speed": 6},
    "indore": {"temp": 31, "description": "Warm and sunny", "humidity": 45, "feels_like": 31, "wind_speed": 4},
    "thane": {"temp": 29, "description": "Cloudy", "humidity": 65, "feels_like": 30, "wind_speed": 4},
    "vadodara": {"temp": 36, "description": "Hot and dry", "humidity": 30, "feels_like": 38, "wind_speed": 6},
    "ghaziabad": {"temp": 33, "description": "Hot and humid", "humidity": 55, "feels_like": 34, "wind_speed": 5},
    "ludhiana": {"temp": 32, "description": "Sunny", "humidity": 50, "feels_like": 33, "wind_speed": 4},
    "agartala": {"temp": 28, "description": "Rainy", "humidity": 80, "feels_like": 28, "wind_speed": 7},
    "amritsar": {"temp": 30, "description": "Sunny", "humidity": 45, "feels_like": 30, "wind_speed": 4},
    "bhopal": {"temp": 33, "description": "Warm and sunny", "humidity": 50, "feels_like": 34, "wind_speed": 5},
    "cochin": {"temp": 31, "description": "Humid and cloudy", "humidity": 75, "feels_like": 32, "wind_speed": 6},
    "mysore": {"temp": 27, "description": "Pleasant", "humidity": 55, "feels_like": 27, "wind_speed": 3},
    "tirupati": {"temp": 34, "description": "Sunny", "humidity": 60, "feels_like": 35, "wind_speed": 5},
}

# Store last 5 searched cities with weather info
search_history = []

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_weather(city):
    city_lower = city.lower()
    try:
        params = {"q": city_lower, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params, timeout=5)

        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            feels_like = data["main"].get("feels_like", temp)
            description = data["weather"][0]["description"].capitalize()
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            dt = data.get("dt", None)
            if dt:
                dt_readable = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dt))
            else:
                dt_readable = "N/A"

            return temp, feels_like, description, humidity, wind_speed, dt_readable

        else:
            # API error fallback to dummy data
            if city_lower in DUMMY_WEATHER:
                print("[!] Using dummy weather data (API error).")
                d = DUMMY_WEATHER[city_lower]
                return d["temp"], d.get("feels_like", d["temp"]), d["description"], d["humidity"], d.get("wind_speed", 0), time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                return None
    except Exception as e:
        # Network or other error fallback to dummy data
        if city_lower in DUMMY_WEATHER:
            print("[!] Using dummy weather data (network error).")
            d = DUMMY_WEATHER[city_lower]
            return d["temp"], d.get("feels_like", d["temp"]), d["description"], d["humidity"], d.get("wind_speed", 0), time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return None

def print_weather(city, weather_data):
    temp, feels_like, description, humidity, wind_speed, dt = weather_data
    print(f"Weather in {city.capitalize()} (as of {dt}):")
    print(f"  Temperature: {temp}°C (Feels like: {feels_like}°C)")
    print(f"  Condition: {description}")
    print(f"  Humidity: {humidity}%")
    print(f"  Wind Speed: {wind_speed} m/s")
    print("-" * 40)

def show_search_history():
    if not search_history:
        print("No previous searches.")
        return
    print("\nLast 5 searched cities:")
    for city, data in search_history[-5:]:
        print_weather(city, data)

if __name__ == "__main__":
    while True:
        clear_screen()
        show_search_history()
        city = input("\nEnter city name (or type 'exit' to quit): ").strip()
        if city.lower() == "exit":
            print("Goodbye!")
            break

        weather = get_weather(city)
        if weather:
            print_weather(city, weather)
            # Save to history
            search_history.append((city, weather))
        else:
            print("City not found in API or dummy data.")
        
        input("\nPress Enter to continue...")

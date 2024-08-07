import requests
import json


def get_weather(city, api_key):
    # Build the API request URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    # Send the request and get the response
    response = requests.get(url)

    # Check for a successful response
    if response.status_code == 200:
        # Parse the JSON data
        data = json.loads(response.text)

        # Extract weather information
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"] - 273.15  # Convert Kelvin to Celsius

        # Return the weather report
        return {
            "description": weather_description,
            "temperature": temperature
        }
    else:
        return {
            "error": f"Unable to retrieve weather data. Status code: {response.status_code}",
            "content": response.text
        }


api_key = "63711b3cbf72f58cedbd15917e1b1715"
city = input("Enter city name: ")
weather = get_weather(city, api_key)

if "error" in weather:
    print(weather["error"])
    print(weather["content"])
else:
    print(f"Weather in {city}: {weather['description']}")
    print(f"Temperature: {weather['temperature']:.2f}°C")

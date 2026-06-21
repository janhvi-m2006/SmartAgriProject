from flask import Flask, render_template, request
import requests
import random
from datetime import datetime
app = Flask(__name__)
import google.generativeai as genai

import os
genai.configure(api_key=GEMINI_API_KEY)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route('/chat', methods=['GET', 'POST'])
def chat():

    answer = ""

    if request.method == "POST":

        question = request.form.get("question")

        try:

            prompt = f"""
You are a Smart Agriculture Assistant.

Give answer EXACTLY in this format:

🌾 Crop:
[Crop Name]

📌 Short Explanation:
[2-3 lines explanation]

✅ Tips:
1. First Tip
2. Second Tip
3. Third Tip

Keep answer short and farmer-friendly.
Use line breaks between all sections.

Question: {question}
"""

            response = model.generate_content(prompt)
            answer = response.text

        except Exception as e:
            answer = f"Error: {e}"

    return render_template("chat.html", answer=answer)

# Login Page
@app.route('/')
def login():
    return render_template('login.html')


# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# Weather
@app.route('/weather', methods=['GET', 'POST'])
def weather():

    result = None

    if request.method == "POST":

        city = request.form['city']

        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

        geo_data = requests.get(geo_url).json()

        if "results" in geo_data:

            latitude = geo_data["results"][0]["latitude"]
            longitude = geo_data["results"][0]["longitude"]

            weather_url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={latitude}&longitude={longitude}"
                f"&current=temperature_2m,relative_humidity_2m"
            )

            weather_data = requests.get(weather_url).json()

            result = {
                "city": city.title(),
                "temp": weather_data["current"]["temperature_2m"],
                "humidity": weather_data["current"]["relative_humidity_2m"],
                "condition": "Current Weather"
            }

    return render_template("weather.html", result=result)

# Crop Recommendation
@app.route('/crop', methods=['GET', 'POST'])
def crop():

    crop_name = ""

    if request.method == "POST":

        soil = request.form['soil'].lower()

        if soil == "black":
            crop_name = "Cotton"
        elif soil == "alluvial":
            crop_name = "Wheat"
        elif soil == "clay":
            crop_name = "Rice"
        else:
            crop_name = "Soybean"

    return render_template('crop_recommend.html', crop=crop_name)


# Fertilizer Suggestion
@app.route('/fertilizer', methods=['GET', 'POST'])
def fertilizer():

    fertilizer_name = ""

    if request.method == "POST":

        crop = request.form['crop'].lower()

        if crop == "rice":
            fertilizer_name = "Urea"
        elif crop == "wheat":
            fertilizer_name = "DAP"
        elif crop == "cotton":
            fertilizer_name = "NPK"
        else:
            fertilizer_name = "Organic Compost"

    return render_template('fertilizer.html', fertilizer=fertilizer_name)


# Disease Detection
@app.route('/disease', methods=['GET', 'POST'])
def disease():

    result = ""

    if request.method == "POST":

        image = request.files['image']

        if image:
            result = "Image Uploaded Successfully"

    return render_template('disease.html', result=result)

# Mandi Prices
@app.route('/prices', methods=['GET', 'POST'])
def prices():

    result = None

    if request.method == "POST":

        crop = request.form.get('crop')
        city = request.form.get('city')

        if crop and city:

            price = random.randint(15, 80)

            result = {
                "crop": crop.title(),
                "city": city.title(),
                "price": f"₹{price} / Kg",
                "source": "SmartAgri Market Data",
                "updated": datetime.now().strftime("%d-%m-%Y %H:%M")
            }

    return render_template("prices.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)

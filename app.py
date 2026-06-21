from flask import Flask, render_template, request
import requests
import random
from datetime import datetime
import os
import google.generativeai as genai

app = Flask(__name__)

# ---------------- GEMINI SETUP ----------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


# ---------------- AI CHATBOT ----------------
@app.route('/chat', methods=['GET', 'POST'])
def chat():

    answer = ""

    if request.method == "POST":

        question = request.form.get("question")

        try:
            prompt = f"""
You are a Smart Agriculture Assistant.

Answer in this format:
🌾 Crop:
📌 Explanation:
✅ Tips:

Keep answer short and simple.

Question: {question}
"""

            response = model.generate_content(prompt)
            answer = response.text

        except Exception:
            answer = "⚠ AI service temporarily unavailable. Please try again later."

    return render_template("chat.html", answer=answer)


# ---------------- LOGIN ----------------
@app.route('/')
def login():
    return render_template('login.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# ---------------- WEATHER ----------------
@app.route('/weather', methods=['GET', 'POST'])
def weather():

    result = None

    if request.method == "POST":

        city = request.form['city']

        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
            geo_data = requests.get(geo_url).json()

            if "results" in geo_data:

                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]

                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m"

                weather_data = requests.get(weather_url).json()

                result = {
                    "city": city.title(),
                    "temp": weather_data["current"]["temperature_2m"],
                    "humidity": weather_data["current"]["relative_humidity_2m"]
                }

        except:
            result = None

    return render_template("weather.html", result=result)


# ---------------- CROP ----------------
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


# ---------------- FERTILIZER ----------------
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


# ---------------- DISEASE ----------------
@app.route('/disease', methods=['GET', 'POST'])
def disease():

    result = ""

    if request.method == "POST":

        image = request.files['image']

        if image:
            result = "Image Uploaded Successfully"

    return render_template('disease.html', result=result)


# ---------------- MARKET PRICE ----------------
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
                "updated": datetime.now().strftime("%d-%m-%Y %H:%M")
            }

    return render_template("prices.html", result=result)


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request

app = Flask(__name__)

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

    result = ""

    if request.method == "POST":

        city = request.form['city']

        api_key = "YOUR_ACTUAL_API_KEY"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        data = requests.get(url).json()

        if data.get("cod") == 200:

            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["description"]

            result = f"""
            City: {city}<br>
            Temperature: {temp}°C<br>
            Humidity: {humidity}%<br>
            Condition: {condition}
            """
        else:
            result = "City not found"

    return render_template('weather.html', result=result)
    print(data)
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

    return render_template(
        'crop_recommend.html',
        crop=crop_name
    )


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

    return render_template(
        'fertilizer.html',
        fertilizer=fertilizer_name
    )


# Disease Detection
@app.route('/disease', methods=['GET', 'POST'])
def disease():

    result = ""

    if request.method == "POST":

        image = request.files['image']

        if image:
            result = "Image Uploaded Successfully"

    return render_template(
        'disease.html',
        result=result
    )


# Mandi Prices
@app.route('/prices', methods=['GET', 'POST'])
def prices():

    price = ""

    if request.method == "POST":

        crop = request.form['crop'].lower()

        if crop == "soybean":
            price = "₹4500 / Quintal"
        elif crop == "wheat":
            price = "₹2600 / Quintal"
        elif crop == "rice":
            price = "₹3000 / Quintal"
        else:
            price = "Price Not Available"

    return render_template(
        'prices.html',
        price=price
    )


if __name__ == '__main__':
    app.run(debug=True)
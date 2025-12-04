from flask import Flask, request, render_template, abort
import pickle
import numpy as np
import time
import os

app = Flask(__name__)

# Labels required by your unit test
weather_classes = ['clear', 'rainy', 'cloudy', 'foggy']

# ----------------------------
# FIX 1: SAFELY LOAD MODEL
# ----------------------------
def load_model(model_path=None):
    if model_path is None:
        model_path = os.path.join(os.path.dirname(__file__), 'model', 'model.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

# ----------------------------
# FIX 2: ENSURE classify_weather MATCHES UNIT TEST
# ----------------------------
def classify_weather(features):
    model = load_model()

    start = time.time()
    label = model.predict(features)[0]   # this is the class label
    latency = round((time.time() - start) * 1000, 2)

    return label, latency
# ----------------------------
# FIX 3: HANDLE MISSING FIELDS → RETURN 400 
# Required by unit test "test_post_missing_field"
# ----------------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        required_fields = ['temperature', 'pressure', 'humidity', 
                           'wind_speed', 'wind_deg', 'rain_1h', 
                           'rain_3h', 'snow', 'clouds']

        # Check if all required fields exist
        for field in required_fields:
            if field not in request.form or request.form[field] == "":
                abort(400, description=f"Missing field: {field}")

        # Convert input to floats
        try:
            features = np.array([
                float(request.form['temperature']),
                float(request.form['pressure']),
                float(request.form['humidity']),
                float(request.form['wind_speed']),
                float(request.form['wind_deg']),
                float(request.form['rain_1h']),
                float(request.form['rain_3h']),
                float(request.form['snow']),
                float(request.form['clouds'])
            ]).reshape(1, -1)
        except ValueError:
            abort(400, description="Invalid input")

        # Predict class
        prediction = classify_weather(features)

        # Integration test expects HTML to contain the prediction word
        return render_template("result.html", prediction=prediction)

    return render_template("form.html")
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


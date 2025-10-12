import joblib
import os
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# --- ENHANCED MODEL LOADING ---
def load_model_safely():
    """Attempt to load model with multiple fallback options"""
    possible_paths = [
        'model.joblib',
        './model.joblib', 
        'model.pkl',
        './model.pkl',
        'model.sav',
        './model.sav',
        '/app/model.joblib',  # Common in Docker deployments
    ]
    
    for model_path in possible_paths:
        try:
            if os.path.exists(model_path):
                print(f"🔄 Attempting to load model from: {model_path}")
                model = joblib.load(model_path)
                print(f"✅ Model loaded successfully from: {model_path}")
                print(f"   Model type: {type(model)}")
                return model
        except Exception as e:
            print(f"❌ Failed to load from {model_path}: {e}")
            continue
    
    print("❌ CRITICAL: Could not load model from any known path!")
    print("📁 Current directory files:")
    for file in os.listdir('.'):
        print(f"   - {file}")
    return None

# Load the model
loaded_model = load_model_safely()

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    error = None 

    if request.method == 'POST':
        if loaded_model is None:
            error = "Prediction model is unavailable. Check the server console for the critical loading error."
            return render_template('index.html', prediction=None, error=error)

        try:
            # Data retrieval and type conversion
            lead_time = int(request.form["lead_time"])
            no_of_special_requests = int(request.form["no_of_special_requests"])
            avg_price_per_room = float(request.form["avg_price_per_room"])
            arrival_month = int(request.form["arrival_month"])
            arrival_date = int(request.form["arrival_date"])
            market_segment_type = int(request.form["market_segment_type"])
            no_of_week_nights = int(request.form["no_of_week_nights"])
            no_of_weekend_nights = int(request.form["no_of_weekend_nights"])
            type_of_meal_plan = int(request.form["type_of_meal_plan"])
            room_type_reserved = int(request.form["room_type_reserved"])

            # Create the feature array
            features = np.array([[lead_time, no_of_special_requests, avg_price_per_room,
                                arrival_month, arrival_date, market_segment_type,
                                no_of_week_nights, no_of_weekend_nights,
                                type_of_meal_plan, room_type_reserved]])
            
            # Predict
            raw_prediction = loaded_model.predict(features)
            prediction = int(raw_prediction[0])

        except ValueError as e:
            error = f"Invalid input. Please ensure all fields are correctly filled. Detail: {e}"
            print(f"❌ Input Error: {e}")
        except Exception as e:
            error = f"An internal error occurred during prediction. Detail: {e}"
            print(f"❌ Prediction Runtime Error: {e}")

    return render_template('index.html', prediction=prediction, error=error)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
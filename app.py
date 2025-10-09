import joblib
import numpy as np
from flask import Flask, render_template, request

# --- CRITICAL CONFIGURATION SECTION ---
# 1. Attempt to import your path configuration
try:
    from config.paths_config import MODEL_OUTPUT_PATH
except ImportError:
    # 2. FALLBACK: Change this path to match where your model file is located!
    MODEL_OUTPUT_PATH = 'model.joblib' 
    print(f"⚠️ Warning: Could not import MODEL_OUTPUT_PATH. Using fallback: {MODEL_OUTPUT_PATH}")
# --------------------------------------

app = Flask(__name__)

# Load the model globally with error handling
loaded_model = None
try:
    loaded_model = joblib.load(MODEL_OUTPUT_PATH)
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ CRITICAL ERROR: Model failed to load from {MODEL_OUTPUT_PATH}. Detail: {e}")

@app.route('/',methods=['GET','POST'])
def index():
    prediction = None
    error = None 

    if request.method=='POST':
        if loaded_model is None:
            error = "Prediction model is unavailable. Check the server console for the critical loading error."
            return render_template('index.html', prediction=None, error=error)

        try:
            # Data retrieval and type conversion
            lead_time = int(request.form["lead_time"])
            no_of_special_requests = int(request.form["no_of_special_requests"])
            # Use float() for avg_price_per_room
            avg_price_per_room = float(request.form["avg_price_per_room"])
            arrival_month = int(request.form["arrival_month"])
            arrival_date = int(request.form["arrival_date"])

            market_segment_type = int(request.form["market_segment_type"])
            no_of_week_nights = int(request.form["no_of_week_nights"])
            no_of_weekend_nights = int(request.form["no_of_weekend_nights"])

            type_of_meal_plan = int(request.form["type_of_meal_plan"])
            room_type_reserved = int(request.form["room_type_reserved"])

            # Create the feature array (10 features)
            features = np.array([[lead_time, no_of_special_requests, avg_price_per_room,
                                  arrival_month, arrival_date, market_segment_type,
                                  no_of_week_nights, no_of_weekend_nights,
                                  type_of_meal_plan, room_type_reserved]])
            
            # Predict
            raw_prediction = loaded_model.predict(features)
            
            # Convert prediction to standard Python integer
            prediction = int(raw_prediction[0])

        except ValueError as e:
            # Handles errors due to empty or non-numeric input
            error = f"Invalid input. Please ensure all fields are correctly filled (especially the number fields). Detail: {e}"
            print(f"❌ Input Error: {e}")
        except Exception as e:
            # Handles errors during model prediction (e.g., wrong number of features)
            error = f"An internal error occurred during prediction. Detail: {e}"
            print(f"❌ Prediction Runtime Error: {e}")

        # Render the template with the prediction or the error
        return render_template('index.html', prediction=prediction, error=error)
    
    # Render the template for GET requests
    return render_template("index.html" , prediction=None)

if __name__=="__main__":
    # Note: host='0.0.0.0' makes it externally accessible (useful for deployment/VMs)
    # Use debug=True for local development to see code changes instantly
    app.run(host='0.0.0.0' , port=8080, debug=True)
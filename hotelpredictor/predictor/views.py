from django.shortcuts import render
import joblib
import numpy as np
from predictor.models import PredictionLog
from predictor.modelforms import PredictionModelForm
from config.paths_config import MODEL_OUTPUT_PATH
# Create your views here.


# Load model

try:
    loaded_model = joblib.load(MODEL_OUTPUT_PATH)
    print("✅ Model loaded successfully.")


except Exception as e:
    loaded_model = None
    print(f'❌ Model load error: {e}')
    

def index(request):
    prediction = None
    error = None
    
    form = PredictionModelForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        if loaded_model is None:
            error = 'Prediction model is not available.'
        
        else:
            try:
                data = form.cleaned_data
                features = np.array([[
                    data['lead_time'], data['no_of_special_requests'], data['avg_price_per_room'],
                    data['arrival_month'], data['arrival_date'], data['market_segment_type'],
                    data['no_of_week_nights'], data['no_of_weekend_nights'], data['type_of_meal_plan'],
                    data['room_type_reserved']
                ]])
                
                prediction = int(loaded_model.predict(features)[0])
                
                PredictionLog.objects.create(**data, prediction_result = prediction)
                
            except Exception as e:
                error = f'Prediction error: {e}'

    dict = {
        'form': form,
        'prediction': prediction,
        'error': error
    }
    return render(request, 'predictor/index.html', context=dict)


    
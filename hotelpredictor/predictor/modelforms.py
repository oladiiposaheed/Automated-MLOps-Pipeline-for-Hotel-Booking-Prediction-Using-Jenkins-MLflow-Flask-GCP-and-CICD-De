from django import forms
from .models import PredictionLog

class PredictionModelForm(forms.ModelForm):
    
    class Meta:
        model = PredictionLog
        exclude = ['timestamp', 'prediction_result']
        
        widgets = {
            'lead_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'no_of_special_requests': forms.NumberInput(attrs={'class': 'form-control'}),
            'avg_price_per_room': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'arrival_month': forms.Select(attrs={'class': 'form-select'}),
            'arrival_date': forms.Select(attrs={'class': 'form-select'}),
            'market_segment_type': forms.Select(attrs={'class': 'form-select'}),
            'no_of_week_nights': forms.NumberInput(attrs={'class': 'form-control'}),
            'no_of_weekend_nights': forms.NumberInput(attrs={'class': 'form-control'}),
            'type_of_meal_plan': forms.Select(attrs={'class': 'form-select'}),
            'room_type_reserved': forms.Select(attrs={'class': 'form-select'}),
        }
  
        help_texts = {
            'lead_time': "Number of days between booking and arrival",
            'no_of_special_requests': "Total number of special requests made",
            'avg_price_per_room': "Average daily rate for the room",
            'no_of_week_nights': "Number of nights stayed during the week",
            'no_of_weekend_nights': "Number of nights stayed during the weekend",
        }


    
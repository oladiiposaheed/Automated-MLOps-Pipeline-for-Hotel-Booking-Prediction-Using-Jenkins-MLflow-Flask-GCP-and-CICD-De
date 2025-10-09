from django.db import models
from .choices import MONTH_CHOICES, DATE_CHOICES, MARKET_SEGMENT_CHOICES,MEAL_PLAN_CHOICES, ROOM_TYPE_CHOICES
# Create your models here.

class PredictionLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    lead_time = models.IntegerField()
    no_of_special_requests = models.IntegerField()
    avg_price_per_room = models.FloatField()
    arrival_month = models.IntegerField(choices=MONTH_CHOICES)
    arrival_date = models.IntegerField(choices=DATE_CHOICES)
    market_segment_type = models.IntegerField(choices=MARKET_SEGMENT_CHOICES)
    no_of_week_nights = models.IntegerField()
    no_of_weekend_nights = models.IntegerField()
    type_of_meal_plan = models.IntegerField(choices=MEAL_PLAN_CHOICES)
    room_type_reserved = models.IntegerField(choices=ROOM_TYPE_CHOICES)
    prediction_result = models.IntegerField()
    
    def __str__(self):
        return f'Prediction on {self.timestamp} -> {self.prediction_result}'
    
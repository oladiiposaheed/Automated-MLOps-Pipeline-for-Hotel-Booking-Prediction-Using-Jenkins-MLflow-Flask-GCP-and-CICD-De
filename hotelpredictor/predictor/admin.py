from django.contrib import admin
from predictor.models import PredictionLog
# Register your models here.

@admin.register(PredictionLog)
class PredictionLogAdmin(admin.ModelAdmin):
    
    list_display = ('timestamp', 'lead_time', 'avg_price_per_room', 'prediction_result')
    list_filter = ('prediction_result', 'arrival_month')
    search_fields = ('lead_time', 'avg_price_per_room')
    
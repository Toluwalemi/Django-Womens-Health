from rest_framework import serializers

from .models import PeriodCycle

from datetime import datetime


class PeriodCycleSerializer(serializers.ModelSerializer):

    class Meta:
        last_period_date = serializers.DateField(format=['%Y-%m-%d'], input_formats=['%Y-%m-%d'])
        start_date = serializers.DateField(input_formats=['%Y%m%d'])
        end_date = serializers.DateField(input_formats=['%Y%m%d'])
        model = PeriodCycle
        fields = ('last_period_date', 'cycle_average', 'period_average',
                  'start_date', 'end_date',)

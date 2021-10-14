from django.db import models


# Create your models here.

class PeriodCycle(models.Model):
    """
    Model to store a lady's period cycle data.
    """
    last_period_date = models.DateField(help_text="Enter your last period date")
    cycle_average = models.IntegerField()
    period_average = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Period Cycles"
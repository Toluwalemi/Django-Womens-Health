import pytest

from api.models import PeriodCycle


@pytest.fixture(scope='function')
def add_period_data():
    def _add_period_data(last_period_date, cycle_average, period_average, start_date, end_date):
        period_cycle = PeriodCycle.objects.create(last_period_date=last_period_date,
                                                  cycle_average=cycle_average,
                                                  period_average=period_average,
                                                  start_date=start_date,
                                                  end_date=end_date)
        return period_cycle

    return _add_period_data

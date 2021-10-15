import pytest


@pytest.mark.django_db
def test_cycle_event_with_no_date(client, add_period_data):
    """Test cycle event event with no date as pararmeter"""
    add_period_data(
        last_period_date="2020-06-20",
        cycle_average=25,
        period_average=5,
        start_date="2020-07-25",
        end_date="2021-07-25"
    )
    resp = client.get('/womens-health/api/cycle-event/')
    assert resp.status_code == 400


@pytest.mark.django_db
def test_cycle_event_with_date(client, add_period_data):
    """Test cycle event endpoint with date given as parameter"""
    add_period_data(
        last_period_date="2020-06-20",
        cycle_average=25,
        period_average=5,
        start_date="2020-07-25",
        end_date="2021-07-25"
    )
    resp = client.get('/womens-health/api/cycle-event/?date=2020-09-15')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_cycle_event_correct_period_start_date(client, add_period_data):
    """Test to print out the correct even for period start date."""
    add_period_data(
        last_period_date="2020-06-20",
        cycle_average=25,
        period_average=5,
        start_date="2020-07-25",
        end_date="2021-07-25"
    )
    resp = client.get('/womens-health/api/cycle-event/?date=2020-07-15')
    assert resp.status_code == 200
    assert resp.data["event"] == "period_start_date"
    assert resp.data["date"] == "2020-07-15"


@pytest.mark.django_db
def test_cycle_event_correct_period_end_date(client, add_period_data):
    """Test to print out the correct even for period end date."""
    add_period_data(
        last_period_date="2020-06-20",
        cycle_average=25,
        period_average=5,
        start_date="2020-07-25",
        end_date="2021-07-25"
    )
    resp = client.get('/womens-health/api/cycle-event/?date=2020-07-20')
    assert resp.status_code == 200
    assert resp.data["event"] == "period_end_date"
    assert resp.data["date"] == "2020-07-20"


@pytest.mark.django_db
def test_cycle_event_correct_ovulation_date(client, add_period_data):
    """Test to print out the correct even for ovulation date."""
    add_period_data(
        last_period_date="2020-06-20",
        cycle_average=25,
        period_average=5,
        start_date="2020-07-25",
        end_date="2021-07-25"
    )
    resp = client.get('/womens-health/api/cycle-event/?date=2020-09-15')
    assert resp.status_code == 200
    assert resp.data["event"] == "ovulation_date"
    assert resp.data["date"] == "2020-09-15"


@pytest.mark.django_db
def test_cycle_event_correct_fertility_window(client, add_period_data):
    """Test to print out the correct even for fertility window."""
    add_period_data(
        last_period_date="2020-06-20",
        cycle_average=25,
        period_average=5,
        start_date="2020-07-25",
        end_date="2021-07-25"
    )
    resp = client.get('/womens-health/api/cycle-event/?date=2020-07-31')
    assert resp.status_code == 200
    assert resp.data["event"] == "fertility_window"
    assert resp.data["date"] == "2020-07-31"


@pytest.mark.django_db
def test_cycle_event_incorrect_cycle_even_date(client, add_period_data):
    """Test to return empty dict for a wrong date"""
    add_period_data(
        last_period_date="2020-06-20",
        cycle_average=25,
        period_average=5,
        start_date="2020-07-25",
        end_date="2021-07-25"
    )
    resp = client.get('/womens-health/api/cycle-event/?date=2022-07-20')
    assert resp.status_code == 200
    assert resp.data == {}

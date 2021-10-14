import pytest

from api.models import PeriodCycle


@pytest.mark.django_db
def test_add_period_cycle(client):
    period_cycle = PeriodCycle.objects.all()
    assert len(period_cycle) == 0

    resp = client.post(
        "/womens-health/api/create-cycle/",
        {
            "last_period_date": "2020-06-06",
            "cycle_average": 25,
            "period_average": 5,
            "start_date": "2020-07-25",
            "end_date": "2021-10-25"
        },
        content_type="application/json"
    )
    assert resp.status_code == 201
    assert resp.data["total_created_cycles"] == 18

    period_cycle = PeriodCycle.objects.all()
    assert len(period_cycle) == 1


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    period_cycle = PeriodCycle.objects.all()
    assert len(period_cycle) == 0

    resp = client.post(
        "/womens-health/api/create-cycle/",
        {},
        content_type="application/json"
    )
    assert resp.status_code == 400

    period_cycle = PeriodCycle.objects.all()
    assert len(period_cycle) == 0


@pytest.mark.django_db
def test_add_period_cycle_invalid_json_keys(client):
    period_cycle = PeriodCycle.objects.all()
    assert len(period_cycle) == 0

    resp = client.post(
        "/womens-health/api/create-cycle/",
        {
            "last_period_date": "2020-06-06",
            "cycle_average": 25,
        },
        content_type="application/json"
    )
    assert resp.status_code == 400

    period_cycle = PeriodCycle.objects.all()
    assert len(period_cycle) == 0


@pytest.mark.django_db
def test_add_period_cycle_to_return_zero(client):
    period_cycle = PeriodCycle.objects.all()
    assert len(period_cycle) == 0

    resp = client.post(
        "/womens-health/api/create-cycle/",
        {
            "last_period_date": "2020-06-06",
            "cycle_average": 25,
            "period_average": 5,
            "start_date": "2021-10-25",
            "end_date":  "2020-07-25"
        },
        content_type="application/json"
    )
    assert resp.status_code == 201
    assert resp.data["total_created_cycles"] == 0

    period_cycle = PeriodCycle.objects.all()
    assert len(period_cycle) == 1

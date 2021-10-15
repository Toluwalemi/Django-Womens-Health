import pytest

from api.models import PeriodCycle


@pytest.mark.django_db
def test_add_period_cycle(client):
    """Ensure the period cycle details entered returns the total created cycle"""
    period_cycle = PeriodCycle.objects.all()
    assert len(period_cycle) == 0

    resp = client.post(
        "/womens-health/api/create-cycle/",
        {
            "last_period_date": "2020-06-06",
            "cycle_average": 25,
            "period_average": 5,
            "start_date": "2020-07-25",
            "end_date": "2021-07-25"
        },
        content_type="application/json"
    )
    assert resp.status_code == 201
    assert resp.data["total_created_cycles"] == 14

    period_cycle = PeriodCycle.objects.all()
    assert len(period_cycle) == 1


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    """Test if an empty json is provided"""
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
    """Test if all the details are not provided"""
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
    """Ensure that create-cycle endpoint returns zero"""
    period_cycle = PeriodCycle.objects.all()
    assert len(period_cycle) == 0

    resp = client.post(
        "/womens-health/api/create-cycle/",
        {
            "last_period_date": "2020-06-06",
            "cycle_average": 25,
            "period_average": 5,
            "start_date": "2021-10-25",
            "end_date": "2020-07-25"
        },
        content_type="application/json"
    )
    assert resp.status_code == 201
    assert resp.data["total_created_cycles"] == 0

    period_cycle = PeriodCycle.objects.all()
    assert len(period_cycle) == 1


@pytest.mark.django_db
def test_update_period_cycle(client, add_period_data):
    """Test to ensure a user can update period details"""
    period_cycle = add_period_data(
        last_period_date="2020-06-20",
        cycle_average=25,
        period_average=5,
        start_date="2020-07-25",
        end_date="2021-07-25"
    )

    resp = client.put(f"/womens-health/api/create-cycle/{period_cycle.id}/",
                      {
                          "last_period_date": "2020-06-20",
                          "cycle_average": 25,
                          "period_average": 5,
                          "start_date": "2020-07-25",
                          "end_date": "2021-07-25"
                      },
                      content_type="application/json"
                      )
    assert resp.status_code == 200
    assert resp.data["total_created_cycles"] == 14


@pytest.mark.django_db
def test_update_period_cycle_invalid_json(client, add_period_data):
    """Test to return 404 for an invalid json"""
    period_cycle = add_period_data(
        last_period_date="2020-06-20",
        cycle_average=25,
        period_average=5,
        start_date="2020-07-25",
        end_date="2021-07-25"
    )
    resp = client.put(f"/womens-health/api/create-cycle/{period_cycle.id}/", {}, content_type="application/json")
    assert resp.status_code == 400


@pytest.mark.django_db
def test_update_period_cycle_invalid_json_keys(client, add_period_data):
    """Test to return 400 in the full data is not provided"""
    period_cycle = add_period_data(
        last_period_date="2020-06-20",
        cycle_average=25,
        period_average=5,
        start_date="2020-07-25",
        end_date="2021-07-25"
    )

    resp = client.put(
        f"/womens-health/api/create-cycle/{period_cycle.id}/",
        {"last_period_date": "2020-06-20", "cycle_average": 25},
        content_type="application/json", )
    assert resp.status_code == 400

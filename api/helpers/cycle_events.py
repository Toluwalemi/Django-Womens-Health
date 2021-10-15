import math
from datetime import datetime, timedelta

from api.helpers.helpers import calculate_no_of_days


def fetch_serialized_data(queryset) -> dict:
    """
    Get serialized data
    """
    return {'last_period_date': queryset['last_period_date'],
            'start_date': queryset['start_date'],
            'end_date': queryset['end_date'],
            'period_average': queryset['period_average'],
            'cycle_average': queryset['cycle_average']}


def get_period_start_date_lst(strp_lpd: datetime, cycle_lst: list) -> list:
    """
    Helper function to get the period start date
    """
    date_format_full = "%Y-%m-%d %H:%M:%S"
    period_start_date_lst = []
    for i in cycle_lst:
        add_date = str(strp_lpd + timedelta(days=i))
        dates_strp = datetime.strptime(str(add_date), date_format_full)
        dates_strf = dates_strp.strftime("%Y-%m-%d")
        period_start_date_lst.append(dates_strf)

    return period_start_date_lst


def get_period_end_date(period_start_date_lst: list, period_average: int) -> list:
    """
    Helper function to get the period end date
    """
    date_format = "%Y-%m-%d"
    date_format_full = "%Y-%m-%d %H:%M:%S"
    period_end_date_lst = []
    for ed in period_start_date_lst:
        get_date = datetime.strptime(str(ed), date_format)
        add_date = str(get_date + timedelta(days=period_average))
        ed_strp = datetime.strptime(str(add_date), date_format_full)
        ed_strf = ed_strp.strftime("%Y-%m-%d")
        period_end_date_lst.append(ed_strf)

    return period_end_date_lst


def get_ovulation_dates(period_start_date_lst: list, new_cycle_average: int) -> list:
    """
    Helper function to get the list of ovulation dates
    """
    date_format = "%Y-%m-%d"
    date_format_full = "%Y-%m-%d %H:%M:%S"
    ovulation_date_lst = []
    for i in period_start_date_lst:
        get_date = datetime.strptime(str(i), date_format)
        add_date = str(get_date + timedelta(days=new_cycle_average))
        ovu_strp = datetime.strptime(str(add_date), date_format_full)
        ovu_strf = ovu_strp.strftime("%Y-%m-%d")
        ovulation_date_lst.append(ovu_strf)

    return ovulation_date_lst


def get_fertility_dates(ovulation_date_lst: list) -> list:
    date_format = "%Y-%m-%d"
    date_format_full = "%Y-%m-%d %H:%M:%S"
    fertility_window_lst = []
    for ovu in ovulation_date_lst:
        get_date = datetime.strptime(str(ovu), date_format)
        add_to = str(get_date + timedelta(days=4))
        sub_from = str(get_date - timedelta(days=4))
        fert_add_strp = datetime.strptime(str(add_to), date_format_full)
        fert_add_strf = fert_add_strp.strftime("%Y-%m-%d")
        fert_sub_strp = datetime.strptime(str(sub_from), date_format_full)
        fert_sub_strf = fert_sub_strp.strftime("%Y-%m-%d")
        fertility_window_lst.append(fert_add_strf)
        fertility_window_lst.append(fert_sub_strf)

    return fertility_window_lst


def helper_cycle_event(queryset_params: dict, date) -> dict:
    """
    Helper function to get the cycle event response
    """
    date_format = "%Y-%m-%d"
    no_of_days = calculate_no_of_days(queryset_params["start_date"].value,
                                      queryset_params["end_date"].value)
    cycle_lst = [
        day
        for day in range(1, no_of_days + 1)
        if day % queryset_params["cycle_average"].value == 0
    ]
    new_cycle_average = math.floor(queryset_params["cycle_average"].value / 2)
    strp_lpd = datetime.strptime(str(queryset_params["last_period_date"].value), date_format)

    # get period start date
    period_start_date_lst = get_period_start_date_lst(strp_lpd, cycle_lst)
    # get period end date
    period_end_date_lst = get_period_end_date(period_start_date_lst, queryset_params["period_average"].value)
    # get ovulation dates
    ovulation_date_lst = get_ovulation_dates(period_start_date_lst, new_cycle_average)
    # get fertility window
    fertility_window_lst = get_fertility_dates(ovulation_date_lst)

    answer_dict = {}
    if date in period_start_date_lst:
        answer_dict['event'] = "period_start_date"
        answer_dict["date"] = date
    elif date in period_end_date_lst:
        answer_dict['event'] = "period_end_date"
        answer_dict["date"] = date
    elif date in ovulation_date_lst:
        answer_dict['event'] = "ovulation_date"
        answer_dict["date"] = date
    elif date in fertility_window_lst:
        answer_dict['event'] = "fertility_window"
        answer_dict["date"] = date

    return answer_dict

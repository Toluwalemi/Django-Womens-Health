import math
from datetime import datetime, timedelta


def calculate_total_created_cycle(cycle_average: int, no_of_days: int) -> int:
    """
    Helper function to calculate total created cycle.
    """
    if cycle_average < no_of_days:
        total_cycle = no_of_days / cycle_average
        return math.floor(total_cycle)
    elif no_of_days < 0:
        return 0


def fetch_serialized_validated_data(serializer) -> dict:
    """
    Helper function to get the serialized validated data
    """
    return {'last_period_date': serializer.validated_data['last_period_date'],
            'start_date': serializer.validated_data['start_date'],
            'end_date': serializer.validated_data['end_date'],
            'period_average': serializer.validated_data['period_average'],
            'cycle_average': serializer.validated_data['cycle_average']}


def calculate_no_of_days(start_date, end_date) -> int:
    """
    Helper function to calculate the no of days between end date and start date
    """
    date_format = "%Y-%m-%d"
    start_date_time_obj = datetime.strptime(str(start_date), date_format)
    end_date_time_obj = datetime.strptime(str(end_date), date_format)
    result = end_date_time_obj - start_date_time_obj

    return result.days


def response_helper(serializer) -> int:
    """
    Helper function that handles finally gets the total created data
    after the serializer has been validated
    """
    serialized_data = fetch_serialized_validated_data(serializer)
    get_difference = calculate_no_of_days(serialized_data["start_date"], serialized_data["end_date"])
    total_created_cycles = calculate_total_created_cycle(serialized_data["cycle_average"], get_difference)
    serializer.save()

    return total_created_cycles


def fetch_serialized_data(queryset) -> dict:
    """
    Get serialized data
    """
    return {'last_period_date': queryset['last_period_date'],
            'start_date': queryset['start_date'],
            'end_date': queryset['end_date'],
            'period_average': queryset['period_average'],
            'cycle_average': queryset['cycle_average']}


def get_period_start_date_lst(strp_lpd, cycle_lst):
    date_format_full = "%Y-%m-%d %H:%M:%S"
    period_start_date_lst = []
    for i in cycle_lst:
        add_date = str(strp_lpd + timedelta(days=i))
        dates_strp = datetime.strptime(str(add_date), date_format_full)
        dates_strf = dates_strp.strftime("%Y-%m-%d")
        period_start_date_lst.append(dates_strf)
    return period_start_date_lst


def get_ovulation_dates(period_start_date_lst, new_cycle_average):
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


def get_fertility_dates(ovulation_date_lst):
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


def helper_cycle_event(queryset_params, date) -> dict:
    """
    Helper function to get the cycle event
    """
    date_format = "%Y-%m-%d"
    no_of_days = calculate_no_of_days(queryset_params["start_date"].value,
                                      queryset_params["end_date"].value)
    cycle_lst = [
        day
        for day in range(1, no_of_days + 1)
        if day % queryset_params["cycle_average"].value == 0
    ]
    last_period_date = queryset_params["last_period_date"].value
    cycle_average = queryset_params["cycle_average"].value
    new_cycle_average = math.floor(cycle_average / 2)
    strp_lpd = datetime.strptime(str(last_period_date), date_format)

    # get period start date
    period_start_date_lst = get_period_start_date_lst(strp_lpd, cycle_lst)
    # get ovulation dates
    ovulation_date_lst = get_ovulation_dates(period_start_date_lst, new_cycle_average)
    # get fertility window
    fertility_window_lst = get_fertility_dates(ovulation_date_lst)

    answer_dict = {}
    if date in period_start_date_lst:
        answer_dict['event'] = "period_start_date"
        answer_dict["date"] = date
    elif date in ovulation_date_lst:
        answer_dict['event'] = "ovulation-date"
        answer_dict["date"] = date
    elif date in fertility_window_lst:
        answer_dict['event'] = "fertility_window"
        answer_dict["date"] = date

    return answer_dict

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


def helper_cycle_event(queryset_params, date) -> dict:
    """
    Helper function to get the cycle event
    """
    date_format = "%Y-%m-%d"
    date_format_full = "%Y-%m-%d %H:%M:%S"
    no_of_days = calculate_no_of_days(queryset_params["start_date"].value,
                                      queryset_params["end_date"].value)
    cycle_lst = [
        day
        for day in range(1, no_of_days + 1)
        if day % queryset_params["cycle_average"].value == 0
    ]
    last_period_date = queryset_params["last_period_date"].value

    strp_lpd = datetime.strptime(str(last_period_date), date_format)
    period_start_date_lst = []
    for i in cycle_lst:
        add_date = str(strp_lpd + timedelta(days=i))
        dates_strp = datetime.strptime(str(add_date), date_format_full)
        dates_strf = dates_strp.strftime("%Y-%m-%d")
        period_start_date_lst.append(dates_strf)

    answer_dict = {}
    if date in period_start_date_lst:
        answer_dict['event'] = "period_start_date"
        answer_dict["date"] = date

    return answer_dict

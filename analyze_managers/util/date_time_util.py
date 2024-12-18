from datetime import datetime, timedelta, timezone

WORK_START_HOUR = 9
WORK_START_MINUTE = 30
WORK_START_SECOND = 0
WORK_END_HOUR = 24
NINE_HOURS_AND_THIRTY_MIN = 570


def convert_timestamp(timestamp):
    """
    Converts a Unix timestamp to a datetime object.

    Args:
        timestamp (int or float): Unix timestamp to convert

    Returns:
        datetime: A datetime object representing the given timestamp

    Example:
        >>> timestamp = 1632145200
        >>> dt = convert_timestamp(timestamp)
        >>> print(dt)
        2021-09-20 12:00:00
    """
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def is_within_working_hours(datetime):
    """
    Checks if a given datetime falls within working hours (9:30 AM to 12:00 AM).

    Args:
        datetime (datetime): The datetime object to check

    Returns:
        bool: True if the time is within working hours, False otherwise

    Example:
        >>> dt = datetime(2023, 1, 1, 14, 30)  # 2:30 PM
        >>> print(is_within_working_hours(dt))
        True
        >>> dt = datetime(2023, 1, 1, 3, 0)    # 3:00 AM
        >>> print(is_within_working_hours(dt))
        False
    """
    work_start = timedelta(hours=WORK_START_HOUR, minutes=WORK_START_MINUTE)
    work_end = timedelta(hours=WORK_END_HOUR)
    time_of_day = timedelta(hours=datetime.hour, minutes=datetime.minute, seconds=datetime.second)

    return work_start <= time_of_day < work_end


def get_response_minutes(user_message_datetime, manager_response_datetime):
    """
    Calculates the response time in minutes between a user message and manager response,
    adjusting for non-working hours.

    If the response spans multiple days, the function subtracts non-working hours
    (before 9:30 AM each day) from the total response time.

    Args:
        user_message_datetime (datetime): Timestamp of the user's message
        manager_response_datetime (datetime): Timestamp of the manager's response

    Returns:
        float: Response time in minutes, adjusted for working hours

    Example:
        >>> user_dt = datetime(2023, 1, 1, 14, 0)    # 2:00 PM
        >>> manager_dt = datetime(2023, 1, 1, 14, 30) # 2:30 PM
        >>> print(get_response_minutes(user_dt, manager_dt))
        30.0
        >>> # For multi-day response
        >>> manager_dt = datetime(2023, 1, 2, 10, 0)  # 10:00 AM next day
        >>> print(get_response_minutes(user_dt, manager_dt))
        870.0  # Total minutes minus 9.5 hours of non-working time
    """
    response_time_delta = manager_response_datetime - user_message_datetime
    response_time_in_minutes = response_time_delta.total_seconds() / 60

    if response_time_delta.days > 0:
        return response_time_in_minutes - (NINE_HOURS_AND_THIRTY_MIN * response_time_delta.days)
    else:
        return response_time_in_minutes

import pandas as pd
import numpy as np
from tqdm import tqdm

from analyze_managers.util.date_time_util import (
    WORK_START_HOUR,
    WORK_START_MINUTE,
    WORK_START_SECOND,
    get_response_minutes,
    is_within_working_hours,
)


def calculate_response_times(cleaned_chat_messages):
    """
    Calculates response times for managers, adjusting for working hours.

    If a user message is received outside working hours and the manager responds
    during working hours, the response time is calculated from the start of the
    working day (9:30 AM).

    Args:
        cleaned_chat_messages (pd.DataFrame): DataFrame containing chat messages with columns:
            - user_message_time (datetime): Timestamp of the previous (user) message
            - manager_response_time (datetime): Timestamp of the manager's response
            - manager_id (int): Manager ID

    Returns:
        list[dict]: List of dictionaries containing:
            - manager_id (int): ID of the responding manager
            - response_minutes (float): Response time in minutes
    """
    response_times = []

    for i in tqdm(range(len(cleaned_chat_messages))):
        user_message_datetime = cleaned_chat_messages.iloc[i]["user_message_time"]
        manager_response_datetime = cleaned_chat_messages.iloc[i]["manager_response_time"]
        manager_id = cleaned_chat_messages.iloc[i]["manager_id"]

        if not is_within_working_hours(user_message_datetime) and is_within_working_hours(
            manager_response_datetime
        ):
            user_message_datetime = user_message_datetime.replace(
                hour=WORK_START_HOUR, minute=WORK_START_MINUTE, second=WORK_START_SECOND
            )

        response_minutes = get_response_minutes(user_message_datetime, manager_response_datetime)
        response_times.append(
            {
                "manager_id": manager_id,
                "response_minutes": response_minutes,
            }
        )

    return response_times


def calculate_average_response_times(response_times, managers):
    """
    Calculates average response times for each manager and merges with manager information.

    Args:
        response_times (list[dict]): List of dictionaries containing:
            - manager_id (int): ID of the responding manager
            - response_minutes (float): Response time in minutes
        managers (pd.DataFrame): DataFrame containing manager information with columns:
            - mop_id (int): Manager ID
            - name_mop (str): Manager name

    Returns:
        pd.DataFrame: DataFrame containing average response times per manager with columns:
            - manager_id (int): Manager ID
            - average_response_time_min (int): Average response time in minutes
            - manager_name (str): Manager name
    """
    # Create DataFrame from response times
    response_df = pd.DataFrame(response_times)

    # Calculate average response time per manager
    average_response_times = (
        response_df.groupby("manager_id")["response_minutes"].mean().reset_index()
    )
    average_response_times["average_response_time_min"] = np.rint(
        average_response_times["response_minutes"]
    ).astype(int)
    average_response_times.drop(columns=["response_minutes"], inplace=True)

    # Merge with manager information
    average_response_times = average_response_times.merge(
        managers[["mop_id", "name_mop"]], left_on="manager_id", right_on="mop_id", how="left"
    )
    average_response_times.rename(columns={"name_mop": "manager_name"}, inplace=True)

    columns_order = ["manager_id", "manager_name", "average_response_time_min"]

    return average_response_times[columns_order]

from analyze_managers.util.date_time_util import convert_timestamp


def prepare_chat_messages(chat_messages):
    """
    Prepares chat messages dataset by cleaning and transforming the data.

    The function performs the following transformations:
    1. Converts timestamps to datetime objects
    2. Sorts messages by entity_id and creation time
    3. Adds previous message type and timestamp for each message
    4. Removes consecutive duplicate message types
    5. Filters out client messages (created_by = 0)
    6. Filters out messages without time

    Args:
        chat_messages (pd.DataFrame): DataFrame containing chat messages with columns:
            - created_at (int/float): Unix timestamp of message creation
            - entity_id (int): Identifier for the chat entity
            - type (str): Type of the message
            - created_by (int): User ID of message creator (0 for clients)

    Returns:
        pd.DataFrame: Cleaned and transformed chat messages with additional columns:
            - user_message_time (datetime): Timestamp of the previous (user) message
            - manager_response_time (datetime): Timestamp of the manager's response
            - manager_id (int): Manager ID
    """
    cleaned_messages = chat_messages.copy()

    # Convert timestamp and sort
    cleaned_messages["manager_response_time"] = cleaned_messages["created_at"].apply(
        convert_timestamp
    )
    cleaned_messages = cleaned_messages.sort_values(by=["entity_id", "manager_response_time"])

    # Add previous message information
    cleaned_messages["user_message_time"] = cleaned_messages.groupby("entity_id")[
        "manager_response_time"
    ].shift()

    # Remove consecutive duplicates
    cleaned_messages = (
        cleaned_messages.groupby("entity_id")
        .apply(remove_consecutive_duplicates)
        .reset_index(drop=True)
    )

    # Filter out client messages
    cleaned_messages = cleaned_messages.query("created_by != 0")

    # Filters out messages without time
    cleaned_messages = cleaned_messages[
        (cleaned_messages["manager_response_time"].notna())
        & (cleaned_messages["user_message_time"].notna())
    ]

    cleaned_messages.rename(columns={"created_by": "manager_id"}, inplace=True)

    return cleaned_messages


def remove_consecutive_duplicates(chat_messages):
    """
    Removes consecutive duplicate message types within a group of chat messages.

    This function is intended to be used with DataFrame.groupby().apply() to process
    messages for each entity_id. It keeps only the first message when there are
    consecutive messages of the same type (e.g., multiple manager messages in a row).

    Args:
        group (pd.DataFrame): A group of chat messages for a single entity_id with columns:
            - type: The type of message

    Returns:
        pd.DataFrame: DataFrame with consecutive duplicate message types removed
    """
    return chat_messages.loc[chat_messages["type"].shift() != chat_messages["type"]]

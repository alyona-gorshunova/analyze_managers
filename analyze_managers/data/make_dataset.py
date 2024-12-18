import pandas as pd


def get_chat_messages(connection):
    """
    Retrieves chat messages data from the database.

    Args:
        connection: Database connection object

    Returns:
        pandas.DataFrame: Chat messages data
    """
    query = """
        SELECT
            *
        FROM
            test.chat_messages
    """
    return pd.read_sql_query(query, connection)


def get_managers(connection):
    """
    Retrieves managers data from the database.

    Args:
        connection: Database connection object

    Returns:
        pandas.DataFrame: Managers data
    """
    query = """
        SELECT
            *
        FROM
            test.managers
    """
    return pd.read_sql_query(query, connection)


def get_rops(connection):
    """
    Retrieves rops data from the database.

    Args:
        connection: Database connection object

    Returns:
        pandas.DataFrame: Rops data
    """
    query = """
        SELECT
            *
        FROM
            test.rops
    """
    return pd.read_sql_query(query, connection)

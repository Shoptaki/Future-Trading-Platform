def check_date_format(date):
    """
    Check if the date is in the correct format YYYY-MM-DD.

    Args:
        date (str): Date to check the format of.

    Returns:
        bool: True if the date is in the correct format, False otherwise
    """
    date_split = date.split("-")

    # Check if the date is in the correct format for year YYYY.
    if len(date_split) != 3 or len(date_split[0]) != 4:
        return False

    # Checks if start and end date have correct month and day formatting MM-DD.
    for i in range(1, len(date_split)):
        if len(date_split[i]) != 2:
            return False

    return True

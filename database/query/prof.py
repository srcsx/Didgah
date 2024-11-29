from database.models import Prof
from database.db_utils import closeDb, connectDb


def createProf(name: str) -> int:
    """This function receives the professor's name and saves it in the database

    Args:
        name (str): professor's name

    Returns:
        int: The output of this function is the professor's column ID or -1,
            where -1 indicates that the operation has encountered an error.
    """
    connectDb()
    
    try:
        res = Prof.insert(name=name).execute() # execute() will return column ID
    except Exception as e:
        # TODO: logging
        res = -1
    
    closeDb()
    return res

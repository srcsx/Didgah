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


def deleteProf(prof_id: int) -> int:
    """This function receives the professor's column ID and delete it from the database

    Args:
        prof_id (int): professor's column ID

    Returns:
        int: Number of deleted columns
    """
    connectDb()
    res = Prof.delete_by_id(prof_id)
    closeDb()
    return res


def deleteAllProfs() -> int:
    """This function will delete all professors from the database

    Returns:
        int: Number of deleted columns
    """
    connectDb()
    res = Prof.delete().execute()
    closeDb()
    return res


def findById(prof_id: int) -> Prof:
    """Retrieve saved information of a professor based on their ID

    Args:
        prof_id (int): professor's column ID


    Returns:
        Prof: Prof object or None
    """
    connectDb()
    prof = Prof.get_or_none(id=prof_id)
    closeDb()
    return prof

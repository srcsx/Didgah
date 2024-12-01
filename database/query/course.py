from typing import List

from database.models import Course
from database.db_utils import closeDb, connectDb


def createCourse(name: str) -> int:
    """This function receives the course name and saves it in the database

    Args:
        name (str): Course name

    Returns:
        int: The output of this function is the course column ID or -1,
            where -1 indicates that the operation has encountered an error.
    """
    connectDb()
    
    try:
        res = Course.insert(name=name).execute() # execute() will return column ID
    except Exception as e:
        # TODO: logging
        res = -1
    
    closeDb()
    return res


def deleteCourse(course_id: int) -> int:
    """This function receives the course column ID and delete it from the database

    Args:
        course_id (int): course column ID

    Returns:
        int: Number of deleted columns
    """
    connectDb()
    res = Course.delete_by_id(course_id)
    closeDb()
    return res


def deleteAllCourses() -> int:
    """This function will delete all courses from the database

    Returns:
        int: Number of deleted columns
    """
    connectDb()
    res = Course.delete().execute()
    closeDb()
    return res


def selectAllCourses() -> List[Course]:
    """This function will return all saved courses in database
    """
    return Course.select().execute()


def findCourseById(course_id: int) -> Course:
    """Retrieve saved information of a courses based on their ID

    Args:
        course_id (int): course column ID


    Returns:
        Course: Course object or None
    """
    connectDb()
    course = Course.get_or_none(id=course_id)
    closeDb()
    return course

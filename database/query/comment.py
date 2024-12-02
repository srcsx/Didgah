from hashlib import sha256
from typing import List

from database.models import Comment


def createComment(prof: str, course: str, text: str, user: int) -> int:
    """This function receives the (prof_id, course_id, text, user) and saves it in the database

    Args:
        prof (str): professor's ID stored in the database
        course (str): course ID stored in the database
        text (str): comment text
        user (int): Telegram user id

    Returns:
        int: The output of this function is the comment's column ID or -1,
            where -1 indicates that the operation has encountered an error.
    """
    
    data = {
        'prof': prof,
        'course': course,
        'text': text,
        'user': sha256(str(user).encode()).hexdigest()  # hash Telegram user id
    }
    
    try:
        res = Comment.insert(**data).execute() # execute() will return column ID
    except Exception as e:
        # TODO: logging
        res = -1
    
    return res


def deleteComment(comment_id: int) -> int:
    """This function receives the comment's column ID and delete it from the database

    Args:
        comment_id (int): comment's column ID

    Returns:
        int: Number of deleted columns
    """
    res = Comment.delete_by_id(comment_id)
    return res


def deleteAllComments() -> int:
    """This function will delete all comments from the database

    Returns:
        int: Number of deleted columns
    """
    res = Comment.delete().execute()
    return res


def selectAllComments() -> List[Comment]:
    """This function will return all saved comments in database
    """
    return Comment.select().execute()


def findCommentById(comment_id: int) -> Comment:
    """Retrieve saved information of a comment based on their ID

    Args:
        comment_id (int): comment's column ID


    Returns:
        Comment: Comment object or None
    """
    comment = Comment.get_or_none(id=comment_id)
    return comment

from operator import itemgetter
from utils.logger import create_logger
import os
LOGGER = create_logger(os.path.basename(__file__))

def get_name_parts(name: str, which:int) -> str:
    """
    Returns part of name that is needed

    Args:
        name (str): whole name path
        which (int): index which we want name

    Returns:
        str: name part at index which
    """
    LOGGER.debug("Getting %s index  of the %s", which, name)
    return name.split(".")[which]

def get_multiple_parts(name:str, indices: list[int], join_with: str=None) -> list:
    """
    Provide indices list that you want from whole name path

    Args:
        name (str): whole name path
        indices (list[int]): list of index you want

    Returns:
        list: names from name path
    """
    LOGGER.debug("Getting %s indices from the %s", indices, name)
    getter = itemgetter(*indices)
    names = getter(name.split("."))
    return names if not join_with else join_with.join(names)

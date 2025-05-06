from enum import Enum

class ErrorCode(Enum):
    ERROR_SECTION_OVERRIGHT = 1
    ERROR_SECTION_NOT_FOUND = 2

VERBOS_MESSAGE = {
    1: "Unable to create section, {} is already there",
    2: "{} Section not found"
}
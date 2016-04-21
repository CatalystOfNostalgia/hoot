from enum import Enum
from enum import unique


@unique
class EmotionQualifier(Enum):
    """
    Represents all possible qualifiers for emotions.
    """
    weak = 1
    moderate = 2
    strong = 3

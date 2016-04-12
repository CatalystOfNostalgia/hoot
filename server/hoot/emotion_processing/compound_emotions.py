from enum import Enum
from enum import unique


@unique
class CompoundEmotion(Enum):
    """
    Represents all possible compound emotions.
    """
    optimism = 1
    frustration = 2
    aggressiveness = 3
    anxiety = 4

    frivolity = 5
    disapproval = 6
    rejection = 7
    awe = 8

    love = 9
    envy = 10
    rivalry = 11
    submission = 12

    gloat = 13
    remorse = 14
    contempt = 15
    coercion = 16

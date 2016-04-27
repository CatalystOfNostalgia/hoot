from enum import Enum
from enum import unique


@unique
class SenticValue(Enum):
    """
    Enum class that represents all possible sentic values.
    """
    # pleasantness values
    grief = 1
    sadness = 2
    pensiveness = 3
    serenity = 4
    joy = 5
    ecstasy = 6

    # attention values
    amazement = 7
    surprise = 8
    distraction = 9
    interest = 10
    anticipation = 11
    vigilance = 12

    # sensitivity values
    terror = 13
    fear = 14
    apprehension = 15
    annoyance = 16
    anger = 17
    rage = 18

    # aptitude values
    loathing = 19
    disgust = 20
    boredom = 21
    acceptance = 22
    trust = 23
    admiration = 24

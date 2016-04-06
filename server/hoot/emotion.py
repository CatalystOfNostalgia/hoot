from sentic_values import SenticValue


interval_maps = {
    'pleasantness': {
        -2/3: SenticValue.grief,
        -1/3: SenticValue.sadness,
        0:    SenticValue.pensiveness,
        1/3:  SenticValue.serenity,
        2/3:  SenticValue.joy,
        1:    SenticValue.ecstasy
    },
    'attention': {
        -2/3: SenticValue.amazement,
        -1/3: SenticValue.surprise,
        0:    SenticValue.distraction,
        1/3:  SenticValue.interest,
        2/3:  SenticValue.anticipation,
        1:    SenticValue.vigilance
    },
    'sensitivity': {
        -2/3: SenticValue.terror,
        -1/3: SenticValue.fear,
        0:    SenticValue.apprehension,
        1/3:  SenticValue.annoyance,
        2/3:  SenticValue.anger,
        1:    SenticValue.rage
    },
    'aptitude': {
        -2/3: SenticValue.loathing,
        -1/3: SenticValue.disgust,
        0:    SenticValue.boredom,
        1/3:  SenticValue.acceptance,
        2/3:  SenticValue.trust,
        1:    SenticValue.admiration
    }
}


class Emotion:

    def __init__(self, emotion_vector):
        self.emotion_vector = emotion_vector

    def get_all_sentic_values(self):
        """
        Uses the emotion vector to find each corresponding sentic value.
        Returns a list containing the sentic value, or none if the value is 0,
        with the order [pleasantness, attention, sensitivity, aptitude].
        """
        sentic_values = []
        for dimension in interval_maps.keys():
            value = self.emotion_vector[dimension]
            sentic_values.append(
                self.get_sentic_value(value, interval_maps[dimension])
            )

        return sentic_values

    def get_sentic_value(self, value, interval_map):
        """
        Returns the specific sentic value for the given value.
        """
        if value == 0:
            return None

        intervals = [-2/3, -1/3, 0, 1/3, 2/3, 1]
        for i in intervals:
            if value <= i:
                return interval_map[i]

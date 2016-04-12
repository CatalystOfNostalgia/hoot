from sentic_values import SenticValue
from compound_emotions import CompoundEmotion

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
        """
        emotion_vector: a dict in the following format:
            {
                'pleasantness': value,
                'attention'   : value,
                'sensitivity' : value,
                'aptitude'    : value
            }
        """
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

    def get_compound_emotion(self):
        """
        Finds and returns any compound emotions associated with the vector.
        """
        pleasantness = self.emotion_vector['pleasantness']
        sensitivity = self.emotion_vector['sensitivity']
        attention = self.emotion_vector['attention']
        aptitude = self.emotion_vector['aptitude']

        emotions = []

        first_emotion = None
        second_emotion = None

        if pleasantness > 0:
            first_emotion = self.get_compound_emotion_from_value(
                attention,
                CompoundEmotion.optimism,
                CompoundEmotion.frivolity
            )
            second_emotion = self.get_compound_emotion_from_value(
                aptitude,
                CompoundEmotion.love,
                CompoundEmotion.gloat
            )
        elif pleasantness < 0:
            first_emotion = self.get_compound_emotion_from_value(
                attention,
                CompoundEmotion.frustration,
                CompoundEmotion.disapproval
            )
            second_emotion = self.get_compound_emotion_from_value(
                aptitude,
                CompoundEmotion.envy,
                CompoundEmotion.remorse
            )

        if first_emotion:
            emotions.append(first_emotion)
        if second_emotion:
            emotions.append(second_emotion)

        third_emotion = None
        fourth_emotion = None

        if sensitivity > 0:
            third_emotion = self.get_compound_emotion_from_value(
                attention,
                CompoundEmotion.aggressiveness,
                CompoundEmotion.rejection
            )
            fourth_emotion = self.get_compound_emotion_from_value(
                aptitude,
                CompoundEmotion.rivalry,
                CompoundEmotion.contempt
            )
        elif sensitivity < 0:
            third_emotion = self.get_compound_emotion_from_value(
                attention,
                CompoundEmotion.anxiety,
                CompoundEmotion.awe
            )
            fourth_emotion = self.get_compound_emotion_from_value(
                aptitude,
                CompoundEmotion.submission,
                CompoundEmotion.coercion
            )

        if third_emotion:
            emotions.append(third_emotion)
        if fourth_emotion:
            emotions.append(fourth_emotion)

        return emotions

    def get_compound_emotion_from_value(self, value, pos_emotion, neg_emotion):
        if value > 0:
            return pos_emotion
        elif value < 0:
            return neg_emotion

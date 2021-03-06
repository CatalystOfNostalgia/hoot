import unittest, string, rdflib, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import queries
from emotion_processing.emotion import Emotion
from emotion_processing.comment_emotions import *
from sqlalchemy import create_engine
from sqlalchemy.schema import Table
from sqlalchemy import MetaData

class TestQueries(unittest.TestCase):
    """ Tester for the queries file 
    Database tests WILL FAIL if run independently of the Makefile
    """
    
    @classmethod
    def setUpClass(self):
        """ inserts test data """

        queries.insert_media('Batman: The Return of the Force', 'Dario', \
                             'A really cool movie', 'Film', '0440419395', 11)

    def test_insert_media(self):
        """ Tests if media is inserted and retrieved correctly """

        # can we find the movie?
        bat = queries.find_media_by_asin('0440419395')
        self.is_batman_movie(bat)

        bat = queries.find_media_by_title('Batman: The Return of the Force')
        self.is_batman_movie(bat[0])

        bat = queries.find_media_by_creator('Dario')
        self.is_batman_movie(bat[0])


    def test_updating_media(self):
        """ Tests updating media and media emotions """

        bat = queries.find_media_by_asin('0440419395')

        # testing updating the emotions
        queries.insert_media_emotion(bat.media_id, 'cool')
        queries.insert_media_emotion(bat.media_id, 'dark')

        emotions = queries.find_emotions_for_media(bat.media_id)

        self.assertTrue('dark' in emotions, \
                        "Didn't find all emotions for media")
        self.assertTrue('cool' in emotions, \
                        "Didn't find all emotions for media")

        # test updating the last_updated column
        queries.update_media(bat.media_id, 20)

        self.assertEqual(bat.last_updated, 20, \
                         'Did not updated date properly')
        
    def test_clean(self):
        """ Tests cleaning the database of comments and emotions """

        bat = queries.find_media_by_asin('0440419395')
        queries.insert_comment(bat.media_id, 11, 7, 0.9, 0.4, -0.5, 0.6, 0.3)

        queries.clean_media(bat.media_id)

        comments = queries.find_comments_for_media(bat.media_id)
        emotions = queries.find_emotions_for_media(bat.media_id)

        self.assertEqual(len(comments), 0)
        self.assertEqual(len(emotions), 0)


    def test_comments(self):
        """ Tests the insertion and deletion of comments """

        bat = queries.find_media_by_creator('Dario')
        queries.insert_comment(bat[0].media_id, 11, 7, 0.9, 0.4, -0.5, 0.6, 0.3)
        comments = queries.find_comments_for_media(bat[0].media_id)

        # can we find the comments?
        self.assertEqual(comments[0].item_id, bat[0].media_id, \
                    'Retrieved incorrect id')
        self.assertEqual(comments[0].relevancy, 7, \
                    msg='Retrieved incorrect relevancy')
        self.assertAlmostEqual(float(comments[0].pleasantness), 0.9, \
                    msg='Retrieved incorrect pleasantness')
        self.assertAlmostEqual(float(comments[0].attention), 0.4, \
                    msg='Retrieved incorrect attention')
        self.assertAlmostEqual(float(comments[0].sensitivity), -0.5, \
                    msg='Retrieved incorrect sensitivity')
        self.assertAlmostEqual(float(comments[0].aptitude), 0.6, \
                    msg='Retrieved incorrect aptitude')
        self.assertAlmostEqual(float(comments[0].polarity), 0.3, \
                    msg='Retrieved incorrect polarity')

        # is the number of comments incremented
        bat = queries.find_media_by_creator('Dario')

        self.assertEqual(bat[0].number_of_comments, 1, 
                        'Retrieved incorrect number of comments')

    def is_batman_movie(self, movie):

        self.assertEqual(movie.title, 'Batman: The Return of the Force', \
                         'Retrieved incorrect title')
        self.assertEqual(movie.creator, 'Dario', \
                         'Retrieved incorrect creator')
        self.assertEqual(movie.description, 'A really cool movie', \
                         'Retrieved incorrect descriptiom')
        self.assertEqual(movie.media_type, 'Film', \
                         'Retrieved incorrect media type')
        self.assertEqual(movie.asin, '0440419395', \
                         'Retrieved incorrect asin')

class TestCommentEmotions(unittest.TestCase):

    def test_find_concepts(self):
        """ Tests finding all concepts for a string """

        none = ''
        one  = 'dark'
        many = """Sitting in the theater, I watched my 6 1/2 year old nephew eat
                up the bright colors and classic sight gags, while I watched  
                my 25 year old fiancee almost spill his popcorn laughing at 
                the exact same joke. What I really liked about this movies was 
                that duality-that one set of lines can be almost making me wet 
                my pants while the more innocent version is keeping the little 
                guys and gals glued to the screen. I found it to be reminiscent
                of the first Toy Story and the underlying message is easy for 
                kids of all shapes and sizes to understand without being so 
                cookie cutter sweet and sappy. Score for the big green guy. 
                I'd take him home."""

        with self.assertRaises(ConceptError):
            find_concepts(none, 0)

        one_concepts  = find_concepts(one, 0)
        many_concepts = find_concepts(many, 0)
        many_concepts_true = ['year', 'old', 'eat', 'bright', 'classic', \
                              'year', 'old', 'spill', 'popcorn', 'exact', \
                              'one', 'set', 'can', 'wet', 'pants', 'innocent', \
                              'keeping', 'little', 'glued', 'first', 'message',\
                              'easy', 'understand', 'cookie', 'sweet', 'big', \
                              'green', 'take']

        self.assertEqual(one_concepts[0], 'dark', 'Did not find proper concept')
        self.assertEqual(many_concepts, many_concepts_true, \
                         'Did not find all concepts')

    def test_calculate_average(self):
        """ Tests getting emotional scores from a comment """

        test = """What has been said about the Dark Knight cannot be 
                    elaborated on - so I won't. The film is muscling its way 
                    into my #1 favorite comic movie adaptation of all time. The 
                    reason for my review is in hopes of saving you some money. 
                    This double disc Special Edition doesn't deliver the price 
                    you pay for it. There isn't even deleted scenes!!! I would 
                    save your very hard earned dollars and buy the single disc 
                    version and wait for the inevitable ULTIMATE re-release that
                    will come later on down the road. But nonetheless, a great 
                    film - you will not be dissapointed; I just wish the studio 
                    would have given a better Special Edition release than what
                    we have here. So enjoy!"""

        test = test.translate(str.maketrans('', '', string.punctuation))
        test = test.lower()

        golden = {'sensitivity': -0.3454, 'aptitude': 0.7312, \
                  'polarity': 0.1983, 'pleasantness': 0.5074, \
                  'attention': 0.1225}

        print ('starting up db')
        f = open('senticnet3.rdf.xml')
        g = rdflib.Graph()
        g.parse(f)
        print ('db started')

        concepts = find_concepts(test, 2)
        scores = get_emotional_scores(concepts, g)
        average = calculate_average(scores)

        self.assertAlmostEqual(average['sensitivity'], golden['sensitivity'],\
                                msg='got different sensitivity', places=3)
        self.assertAlmostEqual(average['aptitude'], golden['aptitude'],\
                                msg='got different aptitude', places=3)
        self.assertAlmostEqual(average['polarity'], golden['polarity'],\
                                msg='got different polarity', places=3)
        self.assertAlmostEqual(average['pleasantness'], golden['pleasantness'],\
                                msg='got different pleasantness', places=3)
        self.assertAlmostEqual(average['attention'], golden['attention'],\
                                msg='got different attention', places=3)

        
if __name__ == '__main__':
    unittest.main()

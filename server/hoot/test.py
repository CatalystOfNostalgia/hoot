import queries
import unittest
import subprocess
from sqlalchemy import create_engine
from sqlalchemy.schema import Table
from sqlalchemy import MetaData

class TestQueries(unittest.TestCase):
    ''' Tester for the queries file 
    Database tests WILL FAIL if run independently of the Makefile
    '''
    
    @classmethod
    def setUpClass(self):
        ''' inserts test data '''

        queries.insert_media('Batman: The Return of the Force', 'Dario', \
                             'A really cool movie', 'Film', 'Romance', \
                             '0440419395')

    def test_insert_media(self):
        ''' Tests if media is inserted and retrieved correctly '''

        # can we find the movie?
        bat = queries.find_media_by_asin('0440419395')
        self.is_batman_movie(bat[0])

        bat = queries.find_media_by_title('Batman: The Return of the Force')
        self.is_batman_movie(bat[0])

        bat = queries.find_media_by_creator('Dario')
        self.is_batman_movie(bat[0])

        # is the emotions entry inserted?

    def test_comments(self):
        ''' Tests the insertion and deletion of comments '''

        bat = queries.find_media_by_creator('Dario')
        queries.insert_comment(bat[0].media_id, 7, 0.9, 0.4, -0.5, 0.6, 0.3)
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

    def is_batman_movie(self, movie):

        self.assertEqual(movie.title, 'Batman: The Return of the Force', \
                         'Retrieved incorrect title')
        self.assertEqual(movie.creator, 'Dario', \
                         'Retrieved incorrect creator')
        self.assertEqual(movie.description, 'A really cool movie', \
                         'Retrieved incorrect descriptiom')
        self.assertEqual(movie.media_type, 'Film', \
                         'Retrieved incorrect media type')
        self.assertEqual(movie.genre, 'Romance', \
                         'Retrieved incorrect genre')
        self.assertEqual(movie.asin, '0440419395', \
                         'Retrieved incorrect asin')



if __name__ == '__main__':
    unittest.main()

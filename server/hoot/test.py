import queries
import unittest
from sqlalchemy import create_engine
from sqlalchemy import MetaData

class TestQueries(unittest.TestCase):
    ''' Tester for the queries file '''
    
    def setUp(self):
        ''' clear the database before testing '''
        engine = create_engine('mysql+pymysql://root@localhost:3306/hoot')

        meta = MetaData()
        meta.drop_all(engine)
        meta.create_all(engine)

    def test_insert_media(self):
        ''' Tests if media is inserted and retrieved correctly '''
        queries.insert_media('Batman: The Return of the Force', 'Dario', \
                             'A really cool movie', 'Film', 'Romance', \
                             '0440419395')

        bat = queries.find_media_by_asin('0440419395')
        self.is_batman_movie(bat)

        bat = queries.find_media_by_title('Batman: The Return of the Force')
        self.is_batman_movie(bat)

        bat = queries.find_media_by_creator('Dario')
        self.is_batman_movie(bat)

    def is_batman_movie(self, movie):

        self.assertEqual(movie[0].title,       'Batman: The Return of the Force')
        self.assertEqual(movie[0].creator,     'Dario')
        self.assertEqual(movie[0].description, 'A really cool movie')
        self.assertEqual(movie[0].media_type,  'Film')
        self.assertEqual(movie[0].genre,       'Romance')
        self.assertEqual(movie[0].asin,        '0440419395')

if __name__ == '__main__':
    unittest.main()

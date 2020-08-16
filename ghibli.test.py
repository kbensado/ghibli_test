import unittest
from ghibli import app

class BasicTestCase(unittest.TestCase):
    def test_movies(self):
        tester = app.test_client(self)
        response = tester.get('/movies', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data, b'Hello World!')

    def test_other(self):
        tester = app.test_client(self)
        response = tester.get('aasdasd', content_type='html/text')
        self.assertEqual(response.status_code, 404)


    # add mock for testing 500 http error code

if __name__ == '__main__':
    unittest.main()

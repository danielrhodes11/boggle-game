from unittest import TestCase
from app import app



class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        """set up the environment before each test"""
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        self.client = app.test_client()
        

    def test_home_page(self):
        """Test the home page"""
        with self.client as client:
            res = client.get('/')
            session = res.get_data(as_text=True)
             
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Boggle</h1>', session)

            
    def test_check_word(self):
        """test checking a word"""
        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [
                ['b', 'a', 'g', 's', 's'],
                ['b', 'a', 'g', 's', 's'],
                ['b', 'a', 'g', 's', 's'],
                ['b', 'a', 'g', 's', 's'],
                ['b', 'a', 'g', 's', 's']
            ]

        res = client.post('/check-word', json={'word': 'word'})
        self.assertEqual(res.status_code, 200)

    def test_valid_word(self):
      """Test if word is valid or invalid by modifying the board in the session"""

      with self.client as client:
        with client.session_transaction() as session:
            session['board'] = [
                ["C", "A", "T", "T", "T"],
                ["C", "A", "T", "T", "T"],
                ["C", "A", "T", "T", "T"],
                ["C", "A", "T", "T", "T"],
                ["C", "A", "T", "T", "T"]
            ]

        # test a valid word
        response = self.client.post('/check-word', json={'word': 'cat'})
        self.assertEqual(response.json['result'], 'ok')

        # test an invalid word

        response = self.client.post('/check-word', json={'word':'rock'})
        self.assertEqual(response.json['result'], 'not-on-board')

        # Test a word that is not a valid dictionary word
        response = self.client.post('/check-word', json={'word': 'zzz'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 'not-word')

    def test_post_score(self):
        """test for posting a score and broken record"""
        with self.client as client: 
            with client.session_transaction() as session:
               session['highscore'] = 100
            score = 120
            data = {'score' : score}

            res = client.post('/post-score', json=data)
            response_data = res.get_json()

            self.assertEqual(res.status_code, 200)
            self.assertTrue(response_data['brokeRecord'])

                

        






               



    
    


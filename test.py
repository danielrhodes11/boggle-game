from unittest import TestCase
from app import app



class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        self.client = app.test_client()

    def test_home_page(self):
        with self.client as client:
            res = client.get('/')
            session = res.get_data(as_text=True)
             
            self.assertEqual(res.status_code, 200)
            self.assertIn('Board:', session)

            
    def test_check_word(self):
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
        with client.session_transaction() as sess:
            sess['board'] = [
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
        






               



    
    


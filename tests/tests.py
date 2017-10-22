import unittest
import json

from wc import app

class TestWC(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.good_key = 'good-key'
        app.config['wc_secret_key'] = self.good_key
        self.app = app.test_client()

    def test_401_authentication_error_if_bad_key_provided(self):
        response = self.app.post(
            'wc',
            data={
                'text': 'This text is the text to count.',
                'wc_secret_key': 'bad-key'
            }
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['text'], 'Bad authorization')

    def test_401_authentication_error_if_no_key_provided(self):
        response = self.app.post(
            'wc',
            data={
                'text': 'This text is the text to count.',
            }
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['text'], 'Bad authorization')

    def test_provides_word_count_with_text_provided(self):
        response = self.app.post(
            'wc',
            data={
                'text': 'This text is the text to count.',
                'wc_secret_key': self.good_key
            }
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['word_count'], 7)

    def test_provides_most_used_word_and_usage_amount(self):
        response = self.app.post(
            'wc',
            data={
                'text': 'This text is the text to count.',
                'wc_secret_key': self.good_key
            }
        )

        data = json.loads(response.data)
        self.assertEqual(data['most_common']['word'], 'text')
        self.assertEqual(data['most_common']['count'], 2)

    def test_422_error_with_informative_text_if_no_text_given(self):
        response = self.app.post(
            'wc',
            data={
                'wc_secret_key': self.good_key
            }
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['text'], 'The `text` body parameter is required.')

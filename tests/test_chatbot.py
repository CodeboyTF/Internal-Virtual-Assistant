import unittest
from app import preprocess_text, find_best_response

class TestChatbot(unittest.TestCase):
    def test_preprocess_text(self):
        self.assertEqual(preprocess_text("Hello, World!"), ['hello', 'world'])

    def test_find_best_response(self):
        response = find_best_response("What are your services?")
        self.assertIn("service", response.lower())

if __name__ == '__main__':
    unittest.main()

# to run the unit test
# python -m unittest discover -s tests

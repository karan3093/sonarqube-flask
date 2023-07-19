import unittest
from my_app import app

class MyAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_login_route_get(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Login via the login Form")

    def test_login_route_post_success(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone number': '1234567890',
            'experience': '5 years',
            'notice period': '30 days',
            'skillset': 'Python, JavaScript'
        }
        response = self.app.post('/login', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Done!")

    def test_login_route_post_invalid_data(self):
        data = {
            'name': '',
            'email': '',
            'phone number': '',
            'experience': '',
            'notice period': '',
            'skillset': ''
        }
        response = self.app.post('/login', data=data)
        self.assertEqual(response.status_code, 400)

    def test_search_route_post_existing_data(self):
        data = {
            'search': 'John Doe'
        }
        response = self.app.post('/search', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)
        self.assertIn(b'john@example.com', response.data)
        self.assertIn(b'5 years', response.data)
        self.assertIn(b'Python, JavaScript', response.data)

    def test_search_route_post_non_existing_data(self):
        data = {
            'search': 'Jane Smith'
        }
        response = self.app.post('/search', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "NO DETAILS FOUND")

if __name__ == '__main__':
    unittest.main()

"""This code shows some output"""
import asyncio
import time
from random import randint
from httpx import AsyncClient
from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
import unittest
from unittest import mock

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'username'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'database_name'

mysql = MySQL(app)

users = {
    "user1": {
        "username": "user1",
        "password": "password1"
    },
    "user2": {
        "username": "user2",
        "password": "password2"
    }
}

async def get_xkcd_image(session: AsyncClient) -> any:
    """Get a random XKCD comic image URL asynchronously.

    :param session: httpx.AsyncClient session to connect to the server
    :type session: httpx.AsyncClient
    :return: URL of the XKCD image
    :rtype: any
    """
    random = randint(0, 300)
    async with session:
        result = await session.get(f'http://xkcd.com/{random}/info.0.json')
    return result.json()['img']

async def get_multiple_images(number: int) -> any:
    """Get multiple XKCD comic image URLs asynchronously.

    :param number: Number of comic images to fetch
    :type number: int
    :return: List of image URLs
    :rtype: any
    """
    async with AsyncClient() as session:
        tasks = [get_xkcd_image(session) for _ in range(number)]
        result = await asyncio.gather(*tasks, return_exceptions=True)
    return result

@app.get('/comic')
async def get_comic_images() -> any:
    """Get multiple XKCD comic images and display them.

    :return: Markup containing comic images and time taken
    :rtype: any
    """
    start = time.perf_counter()
    urls = await get_multiple_images(5)
    end = time.perf_counter()
    markup = f"Time taken: {end-start}<br><br>"
    for url in urls:
        markup += f'<img src="{url}"></img><br><br>'
    return markup

@app.post('/login')
def login() -> any:
    """API endpoint for user login.

    :return: JSON response with login status
    :rtype: any
    """
    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        if username in users and users[username]['password'] == password:
            return jsonify({'status': 'success', 'message': 'Login successful'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401
    else:
        return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400

@app.get('/data')
def get_data() -> any:
    """API endpoint to retrieve data.

    :return: JSON response with data
    :rtype: any
    """
    data = {
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3'
    }
    return jsonify(data)

@app.post('/data')
def create_data() -> any:
    """API endpoint to create data.

    :return: JSON response with creation status
    :rtype: any
    """
    # Process the request and create the data
    # ...
    return jsonify({'status': 'success', 'message': 'Data created'}), 201

@app.put('/data/<id>')
def update_data(id: str) -> any:
    """API endpoint to update data.

    :param id: ID of the data to update
    :type id: str
    :return: JSON response with update status
    :rtype: any
    """
    # Process the request and update the data with the given ID
    # ...
    return jsonify({'status': 'success', 'message': f'Data with ID {id} updated'}), 200

@app.route('/search', methods=['POST'])
def search():
    """API endpoint to search for user details.
    """
    if request.method == "POST":
        group = request.form['search']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT Name, Email, Experience, Skill_Set FROM details WHERE Name = %s', [group])
        data = cursor.fetchone()
        cursor.close()
        if data is None:
            return "NO DETAILS FOUND", 404
        dic = {
            'Name': data[0],
            'Email': data[1],
            'Experience': data[2],
            'Skills': data[3]
        }
        return render_template('search.html', dic=dic)

class AppTestCase(unittest.TestCase):
    """Method for APP Test Case"""

    def setUp(self) -> any:
        """Method to setup

        :return: JSON response or rendered HTML template with user details
        :rtype: any
        """
        self.app = app.test_client()
        # Add any setup actions here, such as creating a test database or test data.
        return True

    def tearDown(self) -> any:
        """Method to teardown

        :return: JSON response or rendered HTML template with user details
        :rtype: any
        """
        # Add any cleanup actions here, such as closing the test database connection.
        return True

    def test_comic_route(self) -> any:
        """Method to test comic route

        :return: JSON response or rendered HTML template with user details
        :rtype: any
        """
        response = self.app.get('/comic')
        self.assertEqual(response.status_code, 200)
        # Add more specific assertions for the content of the response.
        return response

    def test_login_route(self) -> any:
        """Test the login route for user login.

        :return: JSON response or rendered HTML template with user details
        :rtype: any
        """
        data={'username': 'user1', 'password': 'password1'}
        response = self.app.post('/login', data)
        self.assertEqual(response.status_code, 200)
        # Add more specific assertions for the JSON response.

        response = self.app.post('/login', data={'username': 'user1', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 401)
        # Test for invalid password

        response = self.app.post('/login', data={'username': 'non_existent_user', 'password': 'password'})
        self.assertEqual(response.status_code, 401)
        # Test for non-existent user

    def test_get_xkcd_image(self) -> any:
        """Test the get_xkcd_image function to retrieve a random XKCD comic image URL.

        :return: JSON response or rendered HTML template with user details
        :rtype: any
        """
        random_number = 42
        # Replace with any desired random number
        _ = f'http://xkcd.com/{random_number}/info.0.json'
        json_response = {'img': 'https://example.com/comic.png'}

        async def mock_get(*args, **kwargs) -> any:
            """Test the get_xkcd_image function to retrieve a random XKCD comic image URL.

            :param *args: ID of the data to update
            :type *args: any
            :param **kwargs: ID of the data to update
            :type **kwargs: any
            :return: JSON response with update status
            :rtype: any
            """
            response = mock.Mock()
            response.json.return_value = json_response
            return response

        with mock.patch.object(AsyncClient, 'get', side_effect=mock_get):
            result = asyncio.run(get_multiple_images(1))
            self.assertEqual(result[0], json_response['img'])

    def test_search_route(self) -> any:
        """Test the /search route to search for user details.

        :return: JSON response or rendered HTML template with user details
        :rtype: any
        """
        with app.test_client() as client:
            response = client.post('/search', data={'search': 'John Doe'})
            self.assertEqual(response.status_code, 404)
            # Add more specific assertions for the JSON response.
            # Test for a user that does not exist in the database.

            # Add more test cases for the 'search' route as needed.
            return response

if __name__ == '__main__':
    unittest.main()

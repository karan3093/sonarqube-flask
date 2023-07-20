"""This code gives some output"""
import asyncio
import time
from random import randint
from httpx import AsyncClient
from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL

 

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

 

async def get_xkcd_image(session: AsyncClient) -> str:
    """Get a random XKCD comic image URL asynchronously.

 

    :param session: httpx.AsyncClient session to connect to the server
    :type session: httpx.AsyncClient
    :return: URL of the XKCD image
    :rtype: str
    """
    random = randint(0, 300)
    async with session:
        result = await session.get(f'http://xkcd.com/{random}/info.0.json')
    return result.json()['img']

 

async def get_multiple_images(number: int) -> list:
    """Get multiple XKCD comic image URLs asynchronously.

 

    :param number: Number of comic images to fetch
    :type number: int
    :return: List of image URLs
    :rtype: list
    """
    async with AsyncClient() as session:
        tasks = [get_xkcd_image(session) for _ in range(number)]
        result = await asyncio.gather(*tasks, return_exceptions=True)
    return result

 

@app.get('/comic')
async def get_comic_images() -> str:
    """Get multiple XKCD comic images and display them.

 

    :return: Markup containing comic images and time taken
    :rtype: str
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
def get_data() -> str:
    """API endpoint to retrieve data.

 

    :return: JSON response with data
    :rtype: str
    """
    data = {
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3'
    }
    return jsonify(data)

 

@app.post('/data')
def create_data() -> str:
    """API endpoint to create data.

 

    :return: JSON response with creation status
    :rtype: str
    """
    # Process the request and create the data
    # ...
    return jsonify({'status': 'success', 'message': 'Data created'}), 201

 

@app.put('/data/<id>')
def update_data(id: str) -> str:
    """API endpoint to update data.

 

    :param id: ID of the data to update
    :type id: str
    :return: JSON response with update status
    :rtype: str
    """
    # Process the request and update the data with the given ID
    # ...
    return jsonify({'status': 'success', 'message': f'Data with ID {id} updated'}), 200

 

@app.route('/search', methods=['POST'])
def search() -> any:
    """API endpoint to search for user details.

 

    :return: JSON response or rendered HTML template with user details
    :rtype: any
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

 

if __name__ == '__main__':
    app.run(debug=True)

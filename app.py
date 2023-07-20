from flask import Flask, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'username'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'database_name'

mysql = MySQL(app)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone number']
        experience = request.form['experience']
        notice_period = request.form['notice period']
        skill_set = request.form['skillset']
        
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('INSERT INTO details (Name, Email, Phone_Number, Notice_Period, Experience, Skill_Set) VALUES (%s, %s, %s, %s, %s, %s)',
                           (name, email, phone_number, notice_period, experience, skill_set))
            mysql.connection.commit()
            cursor.close()
            return "Done!"
        except Exception as e:
            return f"Error: {str(e)}"

@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        group = request.form['search']
        cursor = mysql.connection.cursor()
        
        cursor.execute('SELECT Name, Email, Experience, Skill_Set FROM details WHERE Name = %s', [group])
        data = cursor.fetchone()
        
        if data is None:
            return "NO DETAILS FOUND"
        
        dic = {
            'Name': data[0],
            'Email': data[1],
            'Experience': data[2],
            'Skills': data[3]
        }
        
        return render_template('search.html', dic=dic)

if __name__ == '__main__':
    app.run(debug=True)

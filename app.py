from flask import Flask
import datetime
app = Flask(__name__)

@app.route('/')
def hello_world():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'Hello from Jenkins! The current time is {current_time}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

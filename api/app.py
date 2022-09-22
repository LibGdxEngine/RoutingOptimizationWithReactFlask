from flask import Flask, request
from flask_restful import Resource, Api
app = Flask(__name__)


@app.route('/points', methods=['GET', 'POST'])
def points():
    # request_data = request.get_json()
    # print(request_data, type(request_data))
    print(request)
    return {
        'Name': "geek",
        "Age": "22",
        "Date": 12,
        "programming": "python"
    }


if __name__ == '__main__':
    app.run()

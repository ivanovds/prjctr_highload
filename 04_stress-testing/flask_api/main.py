from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask import request
import datetime
import random

import config

app = Flask(__name__)
app.config.from_object(config.StagingConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/headers', methods=['GET'])
def headers():
    if request.method == 'GET':
        user_agent = request.headers.get('User-Agent')
        new_header = HTTPHeaders(name=user_agent, timestamp=datetime.datetime.now())
        db.session.add(new_header)
        db.session.commit()

        return f'Your User-Agent header: {user_agent}'


@app.route('/random_row', methods=['GET'])
@config.region.cache_on_arguments()
def random_row():
    if request.method == 'GET':
        max_id = db.session.query(func.max(HTTPHeaders.id)).scalar()
        r_row = None
        r_id = random.randint(1, max_id)
        try:
            r_row = db.session.query(HTTPHeaders).get(r_id)
        except Exception as err:
            print(err)

        if r_row:
            response = str(r_row.id) + ' - ' + r_row.name
        else:
            response = f'Not found row with id {r_id}'

        return f'Random row from DB: {response}'


if __name__ == '__main__':
    app.run()


class HTTPHeaders(db.Model):
    __tablename__ = 'http_headers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    timestamp = db.Column(db.DateTime())

    def __init__(self, name, timestamp):
        self.name = name
        self.timestamp = timestamp

    def __repr__(self):
        return f'<id {self.id}>'

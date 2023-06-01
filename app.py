from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:matt@localhost:5432/trello'

db = SQLAlchemy(app)

class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    status = db.Column(db.String(30))
    date_created = db.Column(db.Date())

@app.cli.command('create')
def create_db():
    db.drop_all()
    db.create_all()
    print('Tables Created Successfully')

@app.cli.command('seed')
def seed_db():
    # Create an instance of the Card model in memory
    cards = [
        Card(
            title = 'Start the project',
            description = 'Stage 1 - Create ERD',
            status = 'Done',
            date_created = date.today()
    ),
        Card(
            title = 'ORM Queries',
            description = 'Stage 2 - Implement several queries',
            status = 'In Progress',
            date_created = date.today()
    ),
        Card(
            title = 'Marshmallow',
            description = 'Stage 3 - Implement jsonify of models',
            status = 'In Progress',
            date_created = date.today()
    )
    ]
    # Truncate the Card table (clear out table)
    db.session.query(Card).delete()

    #  Add the card to the sessions (transaction)
    db.session.add_all(cards)

    # Commit the transaction to the database
    db.session.commit()
    print('Models seeded')

@app.route('/cards')
def all_cards():
    # select * from cards; (stmt is statement)
    #(db.or_(Card.status != 'Done', Card.id > 2)) - or function card status is not Done or card ID greater than 2
    stmt = db.select(Card).order_by(Card.status.desc())
    cards = db.session.scalars(stmt).all()
    return json.dumps(cards)
    # for card in cards:
    #     print(card.__dict__)

@app.route('/')
def index():
    return "Hello, world!"

if __name__ == '__main__':
    app.run(debug=True)
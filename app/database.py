from app import app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager, prompt_bool
from datetime import datetime

db = SQLAlchemy(app)

manager = Manager(usage="Manage the database")

@manager.command
def create():
    """Create the database"""
    db.create_all()

@manager.command
def drop():
    """Empty the database"""
    if prompt_bool("Are you sure you want to drop all tables from the database?"):
        db.drop_all()

@manager.command
def recreate():
    """Recreate the database"""
    drop()
    create()

class Spam(db.Model):
    """
    A list of received Spam messages
    """

    __tablename__ = 'spam'

    id = db.Column(db.Integer, primary_key=True)
    to_header = db.Column(db.Text)
    from_header = db.Column(db.Text)
    subject_header = db.Column(db.Text)
    text_body = db.Column(db.Text)
    html_body = db.Column(db.Text)
    spam_score = db.Column(db.Float)
    created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, to_header, from_header, subject_header, text_body, html_body, spam_score):
        self.to_header = to_header
        self.from_header = from_header
        self.subject_header = subject_header
        self.text_body = text_body
        self.html_body = html_body
        self.spam_score = spam_score

    def getTextBody(self):
        return self.text_body

    def getHtmlBody(self):
        return self.html_body

    def toObject(self):
        return {
            "id": self.id,
            "to_header": self.to_header,
            "from_header": self.from_header,
            "subject_header": self.subject_header,
            "spam_score": self.spam_score,
            "created": self.created.strftime('%Y-%m-%d %H:%M:%S')
        }

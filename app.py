from textadventure import app, db
from textadventure.models import StoryHead, StoryBody, Option

with app.app_context():
    db.create_all()


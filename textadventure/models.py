from datetime import datetime
from textadventure import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(20), nullable = False)
    profile_pic = db.Column(db.String(20), nullable = False, default = "default.jpg")
    stories = db.relationship('StoryHead', backref = 'writer', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', {self.profile_pic})"


class StoryHead(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable = False)
    theme = db.Column(db.Text, nullable = False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    next = db.Column(db.Integer, db.ForeignKey('story_body.id'), nullable = False)

    def __repr__(self):
        return f"Story Head('{self.id}', '{self.title}', '{self.theme}', '{self.next}', '{self.date_created}')"
    
class StoryBody(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    prev_id = db.Column(db.Integer, db.ForeignKey('option.id', use_alter=True), nullable = True)
    # prev = db.relationship('Option', backref = 'next', lazy=True, foreign_keys = 'Option.next_id')
    story = db.Column(db.Text, nullable = False, default = "Story in progress...")
    options = db.relationship('Option', backref = 'story', lazy=True, foreign_keys = 'Option.story_id', cascade = 'all, delete, delete-orphan')
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    is_win = db.Column(db.Boolean, nullable = False, default = False)
    is_lose = db.Column(db.Boolean, nullable = False, default = False)
    def __repr__(self):
        return f"(' Story : {self.story}', Options : {self.options})"

class Option(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    option = db.Column(db.Text, nullable = False)
    story_id = db.Column(db.Integer, db.ForeignKey('story_body.id', use_alter=True), nullable = False)
    next = db.relationship('StoryBody', backref = 'prev', lazy=True, foreign_keys = 'StoryBody.prev_id', cascade = 'all, delete, delete-orphan')
    #next_id = db.Column(db.Integer, db.ForeignKey('story_body.id'), nullable = True)
    
    def __repr__(self):
        return f"Option('{self.id}', '{self.option}', '{self.story_id}', '{self.next}')"
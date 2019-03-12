from flask import Flask
from flask_login import UserMixin, LoginManager, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/house?charset=utf8mb4'
db = SQLAlchemy(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    last_seen = db.Column(db.String(120))
    ip = db.Column(db.String(50))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):  # line 37
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    # def __init__(self, username, email):
    #     self.username = username
    #     self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(120))
    keywords = db.Column(db.String(200))
    wx_user_id = db.Column(db.String(200))
    city = db.Column(db.String(50))
    status = db.Column(db.String(10))
    frequency = db.Column(db.Integer)
    job_id = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    user = db.relationship('User',
                           backref=db.backref('jobs', lazy=True))


class House(db.Model):
    __tablename__ = 'house'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150),unique=True)
    text = db.Column(db.Text())
    city = db.Column(db.String(20))
    location = db.Column(db.String(100))
    longitude = db.Column(db.String(30))
    latitude = db.Column(db.String(30))
    rentType = db.Column(db.String(10))
    tags = db.Column(db.String(50))
    labels = db.Column(db.String(50))
    pubTime = db.Column(db.String(50))
    status = db.Column(db.String(10))
    onlineURL = db.Column(db.String(100))
    pictures = db.Column(db.Text)
    price = db.Column(db.String(20))
    source = db.Column(db.String(30))
    displaySource = db.Column(db.String(39))
    detail_id = db.Column(db.String(200))
    is_sended = db.Column(db.Integer, default=0)
    user_ids = db.Column(db.String(200), default='')

    # __table_args__ = (
    #     db.UniqueConstraint('title', 'pubTime', name='title_pubTime'),
    #     # db.Index('pubTime')
    # )


class HouseSource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    city = db.Column(db.String(50))
    group = db.Column(db.String(50), unique=True)
    source = db.Column(db.String(50))


db.create_all()
db.init_app(app)

# admin = User(username='franky', email='franky.xu@qibaozz.com', password='123456')
# db.session.add(admin)
# db.session.commit()

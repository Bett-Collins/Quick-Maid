from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Model, UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    profile_pic_path = db.Column(db.String())
    booking_id = db.relationship('Booking', backref='author', lazy=True)
    pass_secure = db.Column(db.String(255))
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

        
    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


        
    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)



    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Booking(db.Model):
    __tablename__="booking"
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Text, nullable=False)
    book = db.Column(db.String(255))
    service_needed = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)
    day = db.Column(db.Text, nullable=False)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def save_booking(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_booking(self):
        db.session.remove(self)
        db.session.commit()
        
    @classmethod
    def getBookId(cls, id):
        booking = Booking.query.filter_by(id=id).first()
        return booking

    @classmethod
    def get_bookings(self, id):
        booking = Booking.query.order_by(Booking.posted_date.desc()).filter_by(user_id=id).all()
        return booking

    
    
    
class Post(db.Model):
    __tablename__="post"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    bio = db.Column(db.String(100), nullable=False)
    age =db.Column(db.Integer, nullable=False)
    profile_image = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.name}', '{self.age}','{self.bio}','{self.profile_image}')"

class Comment(db.Model):
    """
    User comment model for each blog 
    """
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    comment_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.remove(self)
        db.session.commit()

    @classmethod
    def getCommentId(cls, id):
        comment = Comment.query.filter_by(id=id).first()
        return comment

    @classmethod
    def get_comments(self, id):
        comment = Comment.query.order_by(Comment.comment_date.desc()).filter_by(post_id=id).all()
        return comment
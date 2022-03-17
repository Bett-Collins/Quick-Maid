from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,TextAreaField, SelectField, DateField, TimeField
from wtforms.validators import Required,Email,EqualTo
from flask_wtf.file import FileField, FileAllowed
from ..models import User, Booking, Post
from wtforms import ValidationError

class BookingForm(FlaskForm):
    location = SelectField('Categories', choices = [('Nairobi', 'Nairobi'),('Roysambu','Roysambu'),('Langata','Langata')('South C','South C')('Umoja','Umoja')], validators=[Required()])
    service = SelectField('Categories', choices = [('Laundery', 'Laundery'),('Baby-Sitting','Baby-Sitting'),('Gardening', 'Gardening')], validators=[Required()])
    date = DateField('Service_Date', format='%m/%d/%Y', validators=[Required()])
    time = TimeField('Serve_at', validators=[Required()])
    extra = BooleanField('Categories', choices = [('Ironing', ' Ironing'),('Cooking','Cooking'),('Interior wall cleaning','Interior wall cleaning')('Interior window cleaning','Interior window cleaning')])
    checkout = SubmitField('Booking')
    
class PostForm(FlaskForm):
    picture = FileField('Profile_picture', validators=[FileAllowed(['jpg', 'png'])])
    name = StringField('Maid Name', validators=[Required()])
    bio = TextAreaField('Write a brief description of yourself', validators=[Required()])
    submit = SubmitField('Profile')

class CommentForm(FlaskForm):
    """
        form for creating a blog comment
    """
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit')
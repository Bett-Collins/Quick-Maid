from flask import render_template,flash,redirect,url_for,abort,request
from . import main
from ..models import Post, User, Booking, Comment
from .forms import BookingForm, PostForm, CommentForm
from ..auth.forms import RegistrationForm, LoginForm
from flask_login import login_required,current_user
from .. import db,photos

# Views

@main.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.posted_date.desc()).all()
    return render_template('index.html', item=posts,page=page)


@main.route("/about")
@login_required
def about():
    return render_template('about.html', title='About')


@main.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
        
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Register'
    return render_template('register.html' ,title=title,form = form)


@main.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Login'
    return render_template('login.html' ,title=title,form = form )

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(name):
    form = PostForm
    user = User.query.filter_by(username = name).first()
    if user is None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save()
        return redirect(url_for('.profile', name=name))
    return render_template('profile/updateprofile.html', form=form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    form = PostForm
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    if form.validate_on_submit():
        filename = form.picture.data
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))



@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your pitch has been updated!', 'success')
        return redirect(url_for('.new_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('new_post.html', title='Update Post', form=form, legend='Update Post')


@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your pitch has been deleted!', 'success')
    return redirect(url_for('main.home'))


@main.route("/post/<string:category>")
def category_post(category):
    
    post = Post.query.filter_by(category=category).all()
    print("..............", post)
    return render_template('category.html', post=post, category=category) 

@main.route("/user/<int:booking_id>/booking", methods=['GET'])
@login_required
def new_book(booking_id):
    user = User.query.filter_by(username = booking_id).first()
    form = BookingForm
    if form.validate_on_submit():
        new_book = Booking(booking=form.service.data, author=current_user, booking_id = booking_id)
        new_book.save_booking()
        db.session.add(new_book)
        db.session.commit()
        flash('You have successfully!', 'success')
        return redirect(url_for('main.bookings', booking_id=booking_id))
    else:
        booking=Booking.query.order_by(Booking.time).all()
    return render_template('new-booking.html', title='New Booking', user=user, booking=booking, form=form, legend='New Booking')

@main.route("/post/<int:post_id>/comment", methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
    post = Post.query.get_or_404(post_id)
    
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(comment=form.comment.data, author=current_user, post_id = post_id )
        new_comment.save_comment()
        db.session.add(new_comment)
        db.session.commit()
       
        flash('You comment has been created!', 'success')
        return redirect(url_for('main.posts', post_id=post.id))
    else:
        comments=Comment.query.order_by(Comment.comment).all()
    return render_template('new-comment.html', title='New Comment',post=post,comments=comments,form=form, legend='New Comment')

@main.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.posted_date.desc()).paginate(page=page, per_page=10)
    return render_template('userpost.html', posts=posts, user=user)

@main.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)
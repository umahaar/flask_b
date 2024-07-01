import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Post
from . import db

views = Blueprint("views", __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/uploads/'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route("/")
def index():
    query = request.args.get("q")
    if query:
        posts = Post.query.filter(
            Post.title.contains(query) 
        ).all()
    else:
        posts = Post.query.all()
    return render_template("index.html", posts=posts)

@views.route("/home")
@login_required
def home():
    query = request.args.get("q")
    if query:
        posts = Post.query.filter(
            Post.title.contains(query) 
        ).all()
    else:
        posts = Post.query.all()
    return render_template("home.html", name=current_user.username, posts=posts)

@views.route("/post/<int:post_id>")
@login_required # I have to deletethis line
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)

@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        image = request.files.get("image")

        if not title or not body:
            flash("Title and body are required!", category='error')
        else:
            filename = None
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(UPLOAD_FOLDER, filename))
                print(f"Image saved to: {os.path.join(UPLOAD_FOLDER, filename)}")  # Debug statement



            new_post = Post(title=title, body=body,image=filename, author=current_user)
            db.session.add(new_post)
            db.session.commit()
            flash("Post created as you wanted it to!", category='success')
            return redirect(url_for("views.home"))

    return render_template("create_post.html")
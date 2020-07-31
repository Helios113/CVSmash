from flask import flash, jsonify, redirect, render_template, request, session, url_for
from app.helpers import login_required
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UploadForm, DeleteForm, SmashForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
import random
from pdf2image import convert_from_bytes
@app.route('/me', methods=["GET", "POST"])
@login_required
def me():
    post = Post.query.filter_by(user_id = current_user.id).first()
    if post:
        allowed = False
        smash = int(post.smash)
        passs = int(post.passs)
        if smash != 0 or passs != 0:
            sm = 100* smash/max(smash,passs)
            ps = 100* passs/max(smash,passs)
        else:
            sm = 0
            ps = 0

        return render_template("me.html" , title = "Me", post = post, allowed = allowed , sm = sm, ps = ps, sma = smash, pas = passs)
    else:
        allowed = True
        form = UploadForm()
        if request.method == "POST":
            if form.validate_on_submit():
                if form.cv.data:
                    img_path = save_cv(form.cv.data)
                    post = Post(content = img_path, user_id = current_user.id)
                    db.session.add(post)
                    db.session.commit()
                    flash("File uploaded successfuly", "success")
                    allowed = False
                    return redirect(url_for('me'))

            else:
                flash("File cannot be uploaded, please upload a valid pdf", "danger")
        return render_template("me.html" , title = "Me", form = form, post = post, allowed = allowed)

@app.route('/me/delete')
@login_required
def delete():
    post = Post.query.filter_by(user_id = current_user.id).first()
    os.remove(os.path.join(app.root_path, 'static/', post.content))
    db.session.delete(post)
    db.session.commit()
    flash("File deleted successfuly", "success")
    return redirect(url_for('me'))





def save_cv(form_cv):
    random_hex = secrets.token_hex(8)
    f_ext = '.png'
    images = convert_from_bytes(form_cv.read(), fmt="png", dpi = 300, size=(1000, None))
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/cvs', picture_fn)
    for image in images:
        image.save(picture_path, 'PNG')
    return 'cvs/'+picture_fn

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('me'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created, you can now log in", "success")
        return redirect(url_for('login'))
    return render_template("register.html", title = "Register" , form = form)

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('me'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('me'))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title = "Log In" , form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/smash', methods=["GET", "POST"])
@login_required
def smash():
    form = SmashForm()
    img = Post.query.all()
    img = img[random.randint(0,len(img)-1)]
    if form.data['smash'] == True:
        img.smash +=1
        db.session.commit()
    elif form.data['pas'] == True:
        img.passs +=1
        db.session.commit()
    return render_template("smash.html" , title = "Smash",img = img ,form = form)

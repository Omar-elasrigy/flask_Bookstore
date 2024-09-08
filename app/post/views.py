from app.models import Post,db
from app.post import post_blueprint
from flask import render_template,request,redirect,url_for
from app.post.forms import PostForm,EditForm
import os
from werkzeug.utils import secure_filename
from flask_login import current_user
@post_blueprint.route("", endpoint="index")
def post_index():
    posts = Post.query.filter_by(user_id=current_user.id).all()  
    return render_template("post/index.html", posts=posts)


@post_blueprint.route("<int:id>/show", endpoint="show")
def post_show(id):
    post = db.get_or_404(Post, id)
    return render_template ("post/show.html",post=post)


@post_blueprint.route("<int:id>/delete", endpoint="delete")
def post_delete(id):
    post = db.get_or_404(Post, id)
    db.session.delete(post)
    db.session.commit()
    return redirect (url_for("post.index"))

@post_blueprint.route("create", endpoint="create", methods=["GET", "POST"])
def post_create():
    if request.method=="POST":
        post=Post(name=request.form["name"],image=request.form["image"],description=request.form["description"])
        db.session.add(post)
        db.session.commit()

        return redirect (url_for("post.index"))
    return render_template("post/create.html")

@post_blueprint.route("<int:id>/edit", endpoint="edit", methods=["GET", "POST"])
def post_edit(id):
    post = db.get_or_404(Post, id)
    if post.user_id != current_user.id:
        abort(403) 
    if request.method=="POST":
        post.image = request.form["image"]
        post.name=request.form["name"]
        post.description=request.form["description"]
        db.session.commit()

        return redirect (url_for("post.index"))
    return render_template("post/edit.html",post=post)

@post_blueprint.route("/form/create", endpoint="create_form", methods=["POST", "GET"])
def create():
    form =PostForm()
    if request.method=='POST':
        if form.validate_on_submit():
            if request.files.get("image"):
                image=form.image.data
                image_name =secure_filename(image.filename)
                image.save(os.path.join('static/posts/images/', image_name))
            data=dict(request.form)
            del data['csrf_token']
            del data['submit']
            data["image"]=image_name
            data["user_id"] = current_user.id 

            post= Post(**data)
            db.session.add(post)
            db.session.commit()
            return redirect(post.show_url)
            
        
    return render_template("post/forms/createform.html",form=form)

@post_blueprint.route("<int:id>/form/edit", endpoint="edit_form", methods=["POST", "GET"])
def edit(id):
    post = db.get_or_404(Post, id)
    form = EditForm(obj=post) 

    if request.method == "POST":
        if form.validate_on_submit():
            post.name = form.name.data
            post.description = form.description.data

            if request.files.get("image"):
                image = form.image.data
                image_name = secure_filename(image.filename)
                image.save(os.path.join('static/posts/images/', image_name))
                post.image = image_name
            else:
                post.image = post.image

            db.session.commit()
            return redirect(url_for("post.index"))

    return render_template("post/forms/editform.html", form=form)
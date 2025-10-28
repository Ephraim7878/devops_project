from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")

posts = []
_next_id = 1

def get_next_id():
    global _next_id
    val = _next_id
    _next_id += 1
    return val

@app.route("/")
def index():
    return render_template("index.html", posts=sorted(posts, key=lambda p: p["created"], reverse=True))

@app.route("/post/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        if not title:
            flash("Title cannot be empty", "danger")
            return redirect(url_for("create"))
        post = {"id": get_next_id(), "title": title, "content": content, "created": datetime.utcnow()}
        posts.append(post)
        flash("Post created successfully!", "success")
        return redirect(url_for("index"))
    return render_template("create.html")

@app.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
def edit(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        flash("Post not found", "danger")
        return redirect(url_for("index"))
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        post["title"], post["content"] = title, content
        flash("Post updated!", "success")
        return redirect(url_for("index"))
    return render_template("edit.html", post=post)

@app.route("/post/<int:post_id>/delete", methods=["POST"])
def delete(post_id):
    global posts
    posts = [p for p in posts if p["id"] != post_id]
    flash("Post deleted!", "warning")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

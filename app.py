from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# Path to the JSON file to store blog posts
DATA_FILE = "data/posts.json"

# Load existing posts from the JSON file
def load_posts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Save posts to the JSON file
def save_posts(posts):
    with open(DATA_FILE, "w") as file:
        json.dump(posts, file, indent=4)

# Route for the homepage
@app.route("/")
def index():
    posts = load_posts()
    return render_template("index.html", posts=posts)

# Route to display a single post
@app.route("/post/<int:post_id>")
def post(post_id):
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return "Post not found", 404
    return render_template("post.html", post=post)

# Route to create a new post
@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        posts = load_posts()
        new_post = {
            "id": len(posts) + 1,
            "title": request.form["title"],
            "content": request.form["content"],
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for("index"))
    return render_template("new_post.html")

if __name__ == "__main__":
    app.run(debug=True, port=5002)  # Change the port to 5001 or any other number


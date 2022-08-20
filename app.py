#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for, abort, request
import random

from .decorators import welcome_screen
from .post_models import create_post_table, get_posts, find_post, random_post, insert_post

app = Flask(__name__)

######## SET THE SECRET KEY ###############
# You can write random letters yourself or 
# Go to https://randomkeygen.com/ and select a 
# random secret key
####################
app.secret_key = 'Oleot40'

with app.app_context():
    create_post_table()

@app.route('/')
@welcome_screen
def home_page():
    return render_template('page.html', posts=get_posts())

@app.route('/welcome')
def welcome_page():
    return render_template('welcome.html')

@app.route('/<post_link>')
@welcome_screen
def post_page(post_link):
    post = find_post(post_link)
    if post:
        return render_template('post.html', post=post)
    else:
        abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.route('/random')
def random_post_page():
    post = random_post()
    return redirect(url_for('post_page', post_link=post['permalink']))

@app.route('/new-post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template('newpost.html')
    else:
        post_data = {
            'title': request.form['post-title'],
            'author': request.form['post-author'],
            'content': request.form['post-content'],
            'permalink': request.form['post-title'].replace(" ", "-"),
            'tags:': request.form['post-tags']
        }
        existing_post = find_post(post_data['permalink'])
        if existing_post:
            return render_template('newpost.html', error="There's already a similar post, maybe use a different title")
        else:
            insert_post(post_data) 
            return redirect(url_for('post_page', post_link=post_data['permalink']))

##### E X E R C I S E S #######
# Exercise 1: Add a page where we can publish new posts.
# Exercise 2: Create a Bootstrap form to add new blog posts.
# Exercise 3: Get the post content from the Quill editor.
# Exercise 4: Save the new blog post in the database.
# Bonus 1: Sort the posts by newest first.
# Bonus 2: Beautify the post URL.
#
# Homework 1: Make sure every post has a unique permalink.
#            Inside new_post()
#             - Inside the else statement, Call the find_post function and send permalink from post_data as parameter
#             - Add an if statement to check if it returns any post.
#             - Inside if render the template newpost.html and send a template variable error with the some message.
#             - Add an else statement to the above if.
#             - Move the insert_post and redirect code inside else.
#            In file newpost.html
#             - Before the form tag, add an if statement to check if there's any value in error template variable
#             - Inside above if, add a error alert as per the Bootstrap documentation.
#
# Homework 2: Add a input field for the post author.
#            In file newpost.html
#             - Inside the form tag
#             - Add another text input field for post author.
#             - Set its name to post-author.
#            Inside app.py
#             - In post_data dictionary, use the value of post-author from request.form instead of manually writing any name.
##############################

from flask import Flask, request, redirect
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

app = Flask(__name__)

# Makes the static folder the image upload folder
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Stores the blog data
blog_text = []
blog_images = []

# This route shows the form
@app.route('/blog/post', methods=['GET', 'POST'])
def blog_form():
    # If doing a get request, we show a form
    if request.method == 'GET':
        return """<h2>Make a post!</h2>
            <form action="/blog/post" method="POST">
                <input type="text" name="image-url" placeholder="Image url"/>
                <br><br>
                <textarea name = "blog-text" rows="3" cols="50" placeholder="Enter your long and thoughtful post!"></textarea>
                <br><br>
                <input type="submit"/>
            </form>"""
    # If doing a post request, we add data to our lists
    if request.method == 'POST':
        # Get the file out of the object
        blog_images.append(request.form['image-url'])
        blog_text.append(request.form['blog-text'])
    return redirect('/blog')

# This route shows the browsing page
@app.route('/', methods=['GET'])
@app.route('/blog', methods=['GET'])
def blog():
    rhtml = "<h1>McNeilogram!</h1>"

    if (len(blog_images) == 0):
        return rhtml + "<p>There are no posts :(</p>"

    # Go through every blog image
    for x in range(0, len(blog_images)):
        # Adds an html row with blog text and an image
        rhtml += '<img src="' + blog_images[x] + '" /><h3>' + blog_text[x] + '</h3>' 
    return rhtml

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
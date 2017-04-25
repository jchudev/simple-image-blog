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

# Turns an image green
def blue_image_filter(imagefile):
    img = mpimg.imread('static/' + imagefile.filename)
    height = len(img)
    width = len(img[0]) # Uses a row to compute width
    # Simple way to go through every pixel of an image
    for y in range(0, height):
        for x in range(0, width):
            # At this iteration, you have access to the RGB levels of each pixel as a 3 element array [R, G, B]
            img[y, x, 0] = 0    # Decreasing R value to 0
            img[y, x, 1] = 0    # Decreasing G value to 0
    mpimg.imsave(os.path.join(app.config['UPLOAD_FOLDER'], imagefile.filename),img)

# This route shows the form
@app.route('/blog/post', methods=['GET', 'POST'])
def blog_form():
    # If doing a get request, we show a form
    if request.method == 'GET':
        return '<form action="/blog/post" method="POST" enctype = "multipart/form-data"><input type="file" name="file" accept="image/*"><input name ="blog_text" type="text"><input type="submit"></form>'
    # If doing a post request, we add data to our lists
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect('/blog')
        # Get the file out of the object
        file = request.files['file']
        # Save the file to our upload folder first so image filter can read it
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        # Append the file name and the blog text to the lists
        blog_images.append(file.filename)
        blog_text.append(request.form['blog_text'])
        blue_image_filter(file)
    return redirect('/blog')

# This route shows the browsing page
@app.route('/blog', methods=['GET'])
def blog():
    rhtml = ""
    # Go through every blog image
    for x in range(0, len(blog_images)):
        # Adds an html row with blog text and an image
        rhtml += '<img src="static/' + blog_images[x] + '" /><h3>' + blog_text[x] + '</h3>' 
    return rhtml

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
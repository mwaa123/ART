from flask import render_template
from app import app

# Views
@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'ART'
    return render_template('index.html',title=title)


@app.route('/about.html')
def about():

    '''
    View root page function that returns the about  page and its data
    '''
    title = 'ART'
    return render_template('about.html',title=title)


# @app.route('/applied.html')
# def applied():

#     '''
#     View root page function that returns the applied page and its data
#     '''
#     title = 'ART'
#     return render_template('applied.html',title=title)

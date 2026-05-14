# Food Delivery Analytics Platform — Complete Flask Project Code

from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os

from sympy import python
from utils.preprocessing import preprocess_data
from utils.visualization import generate_charts
from models.recommendation import recommend_restaurants

app = Flask(__name__)
app.secret_key = 'food_delivery_secret_key'

UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            preprocess_data(filepath)
            generate_charts(filepath)

            flash('Dataset uploaded successfully!')
            return redirect(url_for('dashboard', filename=file.filename))

    return render_template('upload.html')


@app.route('/dashboard/<filename>')
def dashboard(filename):

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    df = pd.read_csv(filepath)

    total_restaurants = len(df)

    avg_rating = round(df['rate'].mean(), 2) if 'rate' in df.columns else 0

    max_votes = df['votes'].max() if 'votes' in df.columns else 0

    top_restaurant = 'N/A'

    if 'votes' in df.columns and 'name' in df.columns:
        top_restaurant = df.loc[df['votes'].idxmax(), 'name']

    return render_template(
        'dashboard.html',
        total_restaurants=total_restaurants,
        avg_rating=avg_rating,
        max_votes=max_votes,
        top_restaurant=top_restaurant,
        filename=filename
    )


@app.route('/search/<filename>', methods=['GET', 'POST'])
def search(filename):

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(filepath)

    results = []

    if request.method == 'POST':
        restaurant_name = request.form['restaurant']

        if 'name' in df.columns:
            results = df[df['name'].str.contains(restaurant_name, case=False, na=False)]

            results = results[['name', 'rate', 'votes']].head(10)

    return render_template('search.html', tables=[results.to_html(classes='table table-striped')] if len(results) > 0 else None, filename=filename)


@app.route('/recommend/<filename>', methods=['GET', 'POST'])
def recommend(filename):

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    recommendations = None

    if request.method == 'POST':
        cuisine = request.form['cuisine']
        recommendations = recommend_restaurants(filepath, cuisine)

    return render_template('recommendations.html', recommendations=recommendations, filename=filename)


if __name__ == '__main__':
    app.run(debug=True)



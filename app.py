from flask import Flask, render_template, request
import os
import pickle
import numpy as np

# Get the directory of the currently executing script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Set the absolute file paths for the .pkl files
popular_pkl_path = os.path.join(current_dir, 'popular.pkl')
pt_pkl_path = os.path.join(current_dir, 'pt.pkl')
books_pkl_path = os.path.join(current_dir, 'books.pkl')
similarity_scores_pkl_path = os.path.join(current_dir, 'similarity_scores.pkl')

# Load the .pkl files
popular_df = pickle.load(open(popular_pkl_path, 'rb'))
pt = pickle.load(open(pt_pkl_path, 'rb'))
books = pickle.load(open(books_pkl_path, 'rb'))
similarity_scores = pickle.load(open(similarity_scores_pkl_path, 'rb'))

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    
    return render_template('index.html',book_name = list(popular_df['Book-Title'].values),author = list(popular_df['Book-Author'].values),image = list(popular_df['Image-URL-M'].values),votes = list(popular_df['Num-Ratings'].values),rating = list(popular_df['Avg-Ratings'].values))

@app.route('/top')
def topten():
    return render_template('top.html',book_name = list(popular_df['Book-Title'].values),author = list(popular_df['Book-Author'].values),image = list(popular_df['Image-URL-M'].values),votes = list(popular_df['Num-Ratings'].values),rating = list(popular_df['Avg-Ratings'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    data = []
    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:11]

        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)
    except IndexError:
        return render_template('error.html')  # Render error page

    return render_template('recommend.html', data=data)


fictionimages = [
    "https://m.media-amazon.com/images/I/41j-s9fHJcL.jpg",
    "https://m.media-amazon.com/images/I/81QuEGw8VPL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/612ADI+BVlL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/8125BDk3l9L._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71Q1tPupKjL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/41XVNoRN3dL.jpg",
    "https://m.media-amazon.com/images/I/41j-s9fHJcL.jpg",
    "https://m.media-amazon.com/images/I/81QuEGw8VPL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/612ADI+BVlL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/8125BDk3l9L._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71Q1tPupKjL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/41XVNoRN3dL.jpg"
]
scifiimages = [
    "https://m.media-amazon.com/images/I/A1u+2fY5yTL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/81m-rJnUdRL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/51i+R7TVLBL.jpg",
    "https://m.media-amazon.com/images/I/91ZYBjR+gYL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/81+Tcrv-ikL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71XqE4caMNL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/A1u+2fY5yTL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/81m-rJnUdRL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/51i+R7TVLBL.jpg",
    "https://m.media-amazon.com/images/I/91ZYBjR+gYL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/81+Tcrv-ikL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71XqE4caMNL._AC_UF1000,1000_QL80_.jpg"
]
mysteryimages=[
    "https://m.media-amazon.com/images/I/61AC3ZUWHQL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71+khXHbe5L._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/517brh4+tIL.jpg",
    "https://rukminim2.flixcart.com/image/850/1000/kjym9ow0/book/q/9/p/and-then-there-were-none-original-imafze8vegpbdkqc.jpeg?q=90&crop=false",
    "https://m.media-amazon.com/images/I/71y4X5150dL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71+yoBE7xfL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/61AC3ZUWHQL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71+khXHbe5L._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/517brh4+tIL.jpg",
    "https://rukminim2.flixcart.com/image/850/1000/kjym9ow0/book/q/9/p/and-then-there-were-none-original-imafze8vegpbdkqc.jpeg?q=90&crop=false",
    "https://m.media-amazon.com/images/I/71y4X5150dL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71+yoBE7xfL._AC_UF1000,1000_QL80_.jpg"
]
horrorimages=[
    "https://m.media-amazon.com/images/I/81ESc05qN5L._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/815Uhzxve5L._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/810pcXb+l3L._AC_UF1000,1000_QL80_.jpg",
    "https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9781982146177/frankenstein-9781982146177_hr.jpg",
    "https://m.media-amazon.com/images/I/81FMksyikrL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71oWFPril4L._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/81ESc05qN5L._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/815Uhzxve5L._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/810pcXb+l3L._AC_UF1000,1000_QL80_.jpg",
    "https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9781982146177/frankenstein-9781982146177_hr.jpg",
    "https://m.media-amazon.com/images/I/81FMksyikrL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71oWFPril4L._AC_UF1000,1000_QL80_.jpg"

]
rimages=[
    "https://m.media-amazon.com/images/I/71Q1tPupKjL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/61RmfGsyCrL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71omNKSfqEL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/81RgYxE272L._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/41cUfnlPHEL.jpg",
    "https://m.media-amazon.com/images/I/71O6xhMdryL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71Q1tPupKjL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/61RmfGsyCrL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71omNKSfqEL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/81RgYxE272L._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/41cUfnlPHEL.jpg",
    "https://m.media-amazon.com/images/I/71O6xhMdryL._AC_UF1000,1000_QL80_.jpg"
]
graphicimages=[
    "https://m.media-amazon.com/images/I/81nqASLZU5L._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/81rV+xVfJAL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/81qjOno3wIL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/A1LEz-p12TL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71qsDiT8ioL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71lBTGxPOOL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/81nqASLZU5L._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/81rV+xVfJAL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/81qjOno3wIL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/A1LEz-p12TL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71qsDiT8ioL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71lBTGxPOOL._AC_UF1000,1000_QL80_.jpg"
]
nonimages=[
    "https://jamesclear.com/wp-content/uploads/2016/06/sapiens-by-yuval-noah-harari.jpg",
    "https://m.media-amazon.com/images/I/91sSklCppdL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/81jaN0aJ+jL._AC_UF1000,1000_QL80_.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1560816565l/48855.jpg",
    "https://m.media-amazon.com/images/I/81pplpQ4JDL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/811HumtGpTL._AC_UF1000,1000_QL80_.jpg",
    "https://jamesclear.com/wp-content/uploads/2016/06/sapiens-by-yuval-noah-harari.jpg",
    "https://m.media-amazon.com/images/I/91sSklCppdL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/81jaN0aJ+jL._AC_UF1000,1000_QL80_.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1560816565l/48855.jpg",
    "https://m.media-amazon.com/images/I/81pplpQ4JDL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/811HumtGpTL._AC_UF1000,1000_QL80_.jpg"
]

@app.route('/genre')
def genre():
    return render_template('genre.html',fictionimages=fictionimages,scifiimages=scifiimages,mysteryimages=mysteryimages,horrorimages=horrorimages,rimages=rimages, graphicimages=graphicimages,nonimages=nonimages)

if __name__== '__main__':
    app.run()
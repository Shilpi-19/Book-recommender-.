from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)


popular_df = pd.read_pickle(open('popular.pkl', 'rb'))
pt = pd.read_pickle(open('pt.pkl', 'rb'))
books = pd.read_pickle(open('books.pkl', 'rb'))
similarity_scores = pd.read_pickle(open('similarity_scores.pkl', 'rb'))
# df = np.array(pickle.load(open('popular.pkl', 'rb')))
# popular_df=pd.DataFrame(df)


@app.route('/')
def index():
    avg_ratings = [round(rating, 2) for rating in popular_df['avg_rating'].values]

    return render_template('index.html',
                           book_name =list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=avg_ratings
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:4]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    print(data)
    return render_template('recommend.html', data=data)


if __name__ == '_main_':
    app.run(debug=True)
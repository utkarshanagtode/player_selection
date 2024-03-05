from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

# Load the pickled model
with open('pt.pkl', 'rb') as f:
    pt = pickle.load(f)

recommend_batsman_df = pickle.load(open('recommend_batsman_df.pkl', '+rb'))
combined_df = pickle.load(open('combined_df.pkl', '+rb'))
similarity_scores = pickle.load(open('similarity_score.pkl', '+rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_batsman', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:16]

    data = []
    for i in similar_items:
        item = []
        temp_df = recommend_batsman_df[recommend_batsman_df['batsman'] == pt.index[i[0]]]
        item.extend(temp_df.drop_duplicates('batsman')['batsman'].to_list())
        item.extend(temp_df.drop_duplicates('batsman')['batting_average'].to_list())
        item.extend(temp_df.drop_duplicates('batsman')['batting_strike_rate'].to_list())
        item.extend(temp_df.drop_duplicates('batsman')['batting_rating'].to_list())

        data.append(item)

    print(data)
    return str(user_input)
    #return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
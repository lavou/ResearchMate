import pandas as pd

similarity_path = './similarity.csv'
similarity_df = pd.read_csv(similarity_path, index_col=0)

topics_path = './topics.csv'
topics_df = pd.read_csv(topics_path, index_col=0)

def get_similarity_percentage(author1, author2, similarity_df):
    similarity = similarity_df.loc[author1, author2] * 100
    return round(similarity, 2)

# def get_topics(author, topics_df):
#     similarity = similarity_df.loc[author1, author2] * 100
#     return round(similarity, 2)

def recommend_collaborators(author, similarity_df, num_recommendations=5):
    sorted_similarities = similarity_df[author].sort_values(ascending=False)
    top_recommendations = sorted_similarities.head(num_recommendations + 1).index.tolist()
    top_recommendations.remove(author)  # remove the input author from the recommendations
    return top_recommendations

def get_topics(author, topics_df):
    topics = topics_df.loc[author].tolist()
    return topics

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/similarity', methods=['POST'])
def similarity():
    author1 = request.form['author1']
    author2 = request.form['author2']
    similarity = get_similarity_percentage(author1, author2, similarity_df)
    return f"The similarity percentage between {author1} and {author2} is {similarity}%."

@app.route('/recommend', methods=['POST'])
def recommend():
    author = request.form['author']
    recommendations = recommend_collaborators(author, similarity_df)
    topics = get_topics(author, topics_df)
    return render_template("recommend.html",
                           recommendations=recommendations,
                           topics=topics,
                           author=author)

if __name__ == '__main__':
    app.run()
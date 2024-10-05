# import pickle
# from flask import Flask, request, jsonify

# # Load the movie and similarity data
# movies = pickle.load(open('movies.pkl', 'rb'))
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# app = Flask(__name__)

# @app.route('/recommend', methods=['GET'])
# def recommend():
#     movie_name = request.args.get('movie').strip().lower()
#     print(f"Received request for movie: '{movie_name}'")  # Debugging output

#     # Ensure to check the titles in a case-insensitive manner
#     if movie_name not in movies['title'].str.lower().values:
#         print("Movie not found in titles.")  # More debug info
#         return jsonify({'error': 'Movie not found'})

#     # Get the movie index
#     movie_idx = movies[movies['title'].str.lower() == movie_name].index[0]
#     similar_movies = list(enumerate(similarity[movie_idx]))
#     sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:6]

#     recommended_movie_titles = [movies.iloc[i[0]].title for i in sorted_similar_movies]

#     return jsonify({'recommendations': recommended_movie_titles})

# if __name__ == '__main__':
#     app.run(debug=True)





import pickle
import requests
from flask import Flask, request, jsonify

# Load the movie and similarity data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

app = Flask(__name__)

# Function to fetch poster image from TMDb API
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=15a72db1be97275cbf691a462784938a&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/original" + data['poster_path'] if 'poster_path' in data else None

@app.route('/recommend', methods=['GET'])
def recommend():
    movie_name = request.args.get('movie').strip().lower()
    print(f"Received request for movie: '{movie_name}'")  # Debugging output

    # Ensure to check the titles in a case-insensitive manner
    if movie_name not in movies['title'].str.lower().values:
        print("Movie not found in titles.")  # More debug info
        return jsonify({'error': 'Movie not found'})

    # Get the movie index
    movie_idx = movies[movies['title'].str.lower() == movie_name].index[0]
    similar_movies = list(enumerate(similarity[movie_idx]))
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:6]

    # Prepare recommendations with titles and poster URLs
    recommendations = []
    for i in sorted_similar_movies:
        movie_id = movies.iloc[i[0]].movie_id  # Assuming you have a 'movie_id' column in your movies DataFrame
        movie_title = movies.iloc[i[0]].title
        poster_url = fetch_poster(movie_id)  # Fetch the poster using the function

        recommendations.append({
            'title': movie_title,
            'poster_url': poster_url  # Add the poster URL to the response
        })

    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)

#Importing the required libaries
import numpy as np
import pandas as pd
import streamlit as st
import sklearn 
import pickle
import requests
import bs4 as bs
import urllib.request
import json

#Sidebar Heading
st.sidebar.title('Based on your Favorite Movie...!')
st.sidebar.write('Recommend Movies to Yourself')

#Site Heading
st.header("Recommend Movies to Yourself")


recommended_movie_imdb_id = []
selected_movie_imdb_id = []

# load Models
movies = pickle.load(open('movies_list.pkl','rb'))
recommand = pickle.load(open('recommand.pkl','rb'))
clf = pickle.load(open('sentiment.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl','rb'))


#User Input
movie_list = movies['title'].values
selected_movie = st.sidebar.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

#To Fetch imdb_id
def fetch_imdb_id(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=eab26b9d5f2cc3ad149a18a460342632&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()

    imdb_id = data['imdb_id']
    link = 'https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)
    return link

#To fetch Reviews
def reviews(k,f,l):
    for link in k[f:l]:
        sauce = urllib.request.urlopen(link).read()
        soup = bs.BeautifulSoup(sauce,'lxml')
        soup_result = soup.find_all("div",{"class":"text show-more__control"})
        reviews_list = [] # list of reviews
        reviews_status = [] # list of comments (good or bad)
        per = 0
        for reviews in soup_result:
            if reviews.string:
                reviews_list.append(reviews.string)
                # passing the review to our model
                movie_review_list = np.array([reviews.string])
                movie_vector = vectorizer.transform(movie_review_list)
                pred = clf.predict(movie_vector)
                reviews_status.append('Good' if pred else 'Bad')
                cntg = reviews_status.count("Good") 
                cnt = len(reviews_status)
                if ((cntg & cnt) > 0):
                    per = cntg / cnt * 100
                else:
                    per = 0
        return round(per,2)

#To Fetch Genres
def get_genre(movie_id):
    genres = [] 
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=eab26b9d5f2cc3ad149a18a460342632&language=en-US'.format(movie_id))
    data_json = response.json()
    response.close()
    if data_json['genres']:
        genre_str = " " 
        for i in range(0,len(data_json['genres'])):
            genres.append(data_json['genres'][i]['name'])
            st = genre_str.join(genres[0:2])
            gt = st.replace(" ",", ")
        return gt

#To Fetch Runtime
def get_runtime(movie_id):
    runtime = [] 
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=eab26b9d5f2cc3ad149a18a460342632&language=en-US'.format(movie_id))
    data_json = response.json()
    response.close()
    if data_json['runtime']:
        runtime.append(data_json['runtime'])
        time = ''.join(str(i) for i in runtime)
        return time

#To fetch Actors
def fetch_actor(movie_id):
    actors = []
    response = requests.get('https://api.themoviedb.org/3/movie/{}/credits?api_key=eab26b9d5f2cc3ad149a18a460342632&language=en-US'.format(movie_id))
    data_json = response.json()
    response.close()
    actor_str = " "
    for i in data_json['cast']:
        if i["known_for_department"] == "Acting":
            actors.append(i["original_name"])
    cast = [i.replace(" ","")for i in actors]
    actor = actor_str.join(cast[0:3])
    act = actor.replace(" ",",")
    new_text = ''
    for i, letter in enumerate(act):
        if i and letter.isupper():
            new_text += ' '
        new_text += letter

    return new_text

#To Fetch Director
def fetch_Director(movie_id):
    crew = []
    response = requests.get('https://api.themoviedb.org/3/movie/{}/credits?api_key=eab26b9d5f2cc3ad149a18a460342632&language=en-US'.format(movie_id))
    data_json = response.json()
    response.close()
    dir_str = " "
    for i in data_json['crew']:
        if i['job'] == "Director":
            crew.append(i["original_name"])
        Director = dir_str.join(crew)
    return Director

#To fetch Rating
def get_rating(movie_id):
    rating = [] 
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=eab26b9d5f2cc3ad149a18a460342632'.format(movie_id))
    data_json = response.json()
    response.close()
    if data_json['vote_average']:
        rating.append(data_json['vote_average'])
        rate = ''.join(str(i) for i in rating)
        return rate

#To Fetch Movies Poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=eab26b9d5f2cc3ad149a18a460342632&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()

    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

#Recommendation Function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(recommand[index])), reverse=True, key=lambda x: x[1])

    #Selected Movies
    sel_index = list(movies[movies['title'] == movie].index)
    for i in sel_index:
        sel_movie = movies.iloc[i].id
        LinkedIn = 'Owner @ [Akaash](https://www.linkedin.com/in/aakash-rajbhar-084a92220/)'
        selected_movie_names = []
        selected_movie_posters = []
        selected_movie_genres = []
        selected_movie_runtime = []
        selected_movie_actors = []
        selected_movie_Director = []
        selected_movie_rating = []
        selected_movie_reviews = []
        selected_movie_posters.append(fetch_poster(sel_movie))
        selected_movie_names.append(movie)
        selected_movie_genres.append(get_genre(sel_movie))
        selected_movie_runtime.append(get_runtime(sel_movie))
        selected_movie_actors.append(fetch_actor(sel_movie))
        selected_movie_Director.append(fetch_Director(sel_movie))
        selected_movie_rating.append(get_rating(sel_movie))
        selected_movie_imdb_id.append(fetch_imdb_id(sel_movie))
        selected_movie_reviews.append(reviews(selected_movie_imdb_id,0,1))

    #Recommend Movies
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_reviews = []
    recommended_movie_genres = []
    recommended_movie_runtime = []
    recommended_movie_actors = []
    recommended_movie_Director = []
    recommended_movie_rating = []
    for i in distances[1:7]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_imdb_id.append(fetch_imdb_id(movie_id))
        recommended_movie_reviews.append(reviews(recommended_movie_imdb_id,0,1))
        recommended_movie_reviews.append(reviews(recommended_movie_imdb_id,1,2))
        recommended_movie_reviews.append(reviews(recommended_movie_imdb_id,2,3))
        recommended_movie_reviews.append(reviews(recommended_movie_imdb_id,3,4))
        recommended_movie_reviews.append(reviews(recommended_movie_imdb_id,4,5))
        recommended_movie_reviews.append(reviews(recommended_movie_imdb_id,5,6))
        recommended_movie_genres.append(get_genre(movie_id))
        recommended_movie_runtime.append(get_runtime(movie_id))
        recommended_movie_actors.append(fetch_actor(movie_id))
        recommended_movie_Director.append(fetch_Director(movie_id))
        recommended_movie_rating.append(get_rating(movie_id))
        
    return selected_movie_names,selected_movie_posters,selected_movie_genres,selected_movie_runtime,selected_movie_actors,selected_movie_Director,selected_movie_rating,selected_movie_reviews,recommended_movie_names,recommended_movie_posters,recommended_movie_reviews,recommended_movie_genres,recommended_movie_runtime,recommended_movie_actors,recommended_movie_Director,recommended_movie_rating,LinkedIn

#Button
if st.sidebar.button('Show Recommendation'):

    selected_movie_names,selected_movie_posters,selected_movie_genres,selected_movie_runtime,selected_movie_actors,selected_movie_Director,selected_movie_rating,selected_movie_reviews,recommended_movie_names,recommended_movie_posters,recommended_movie_reviews,recommended_movie_genres,recommended_movie_runtime,recommended_movie_actors,recommended_movie_Director,recommended_movie_rating,LinkedIn = recommend(selected_movie)

    st.sidebar.write("Your Selected Movie: {}".format(selected_movie_names[0]))
    st.sidebar.caption("Genres: {}".format(selected_movie_genres[0]))
    st.sidebar.caption("Runtime: {} mins".format(selected_movie_runtime[0]))
    st.sidebar.caption("Cast: {} ".format(selected_movie_actors[0]))
    st.sidebar.caption("Director: {}".format(selected_movie_Director[0]))
    st.sidebar.caption("IMDb Rating: {}/10".format(selected_movie_rating[0]))
    st.sidebar.caption("Public (+) Reviews: {} ".format("%s%%"%selected_movie_reviews[0]))
    st.sidebar.image(selected_movie_posters[0],width = 250)
    st.sidebar.markdown(LinkedIn,unsafe_allow_html=True)

    st.subheader("Movies Recommended to You are:")

    col1, col2 = st.columns(2)
    with col1:
        st.write(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
        st.caption("Genres: {} ".format(recommended_movie_genres[0]))
        st.caption("Runtime: {} mins".format(recommended_movie_runtime[0]))
        st.caption("Cast: {} ".format(recommended_movie_actors[0]))
        st.caption("Director: {}".format(recommended_movie_Director[0]))
        st.caption("IMDb Rating: {}/10".format(recommended_movie_rating[0]))
        st.caption("Public (+) Reviews: {} ".format("%s%%"%recommended_movie_reviews[0]))
     
    with col2:
        st.write(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
        st.caption("Genres: {} ".format(recommended_movie_genres[1]))
        st.caption("Runtime: {} mins".format(recommended_movie_runtime[1]))
        st.caption("Cast: {} ".format(recommended_movie_actors[1]))
        st.caption("Director: {}".format(recommended_movie_Director[1]))
        st.caption("IMDb Rating: {}/10".format(recommended_movie_rating[1]))
        st.caption("Public (+) Reviews: {}".format("%s%%"%recommended_movie_reviews[7]))

    with col1:
        st.write(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
        st.caption("Genres: {} ".format(recommended_movie_genres[2]))
        st.caption("Runtime: {} mins".format(recommended_movie_runtime[2]))
        st.caption("Cast: {} ".format(recommended_movie_actors[2]))
        st.caption("Director: {}".format(recommended_movie_Director[2]))
        st.caption("IMDb Rating: {}/10".format(recommended_movie_rating[2]))
        st.caption("Public (+) Reviews: {}".format("%s%%"%recommended_movie_reviews[14]))

    with col2:
        st.write(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
        st.caption("Genres: {} ".format(recommended_movie_genres[3]))
        st.caption("Runtime: {} mins".format(recommended_movie_runtime[3]))
        st.caption("Cast: {} ".format(recommended_movie_actors[3]))
        st.caption("Director: {}".format(recommended_movie_Director[3]))
        st.caption("IMDb Rating: {}/10".format(recommended_movie_rating[3]))
        st.caption("Public (+) Reviews: {}".format("%s%%"%recommended_movie_reviews[21]))

    with col1:
        st.write(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
        st.caption("Genres: {} ".format(recommended_movie_genres[4]))
        st.caption("Runtime: {} mins".format(recommended_movie_runtime[4]))
        st.caption("Cast: {} ".format(recommended_movie_actors[4]))
        st.caption("Director: {}".format(recommended_movie_Director[4]))
        st.caption("IMDb Rating: {}/10".format(recommended_movie_rating[4]))
        st.caption("Public (+) Reviews: {}".format("%s%%"%recommended_movie_reviews[28]))

    with col2:
        st.write(recommended_movie_names[5])
        st.image(recommended_movie_posters[5])
        st.caption("Genres: {} ".format(recommended_movie_genres[5]))
        st.caption("Runtime: {} mins".format(recommended_movie_runtime[5]))
        st.caption("Cast: {} ".format(recommended_movie_actors[5]))
        st.caption("Director: {}".format(recommended_movie_Director[5]))
        st.caption("IMDb Rating: {}/10".format(recommended_movie_rating[5]))
        st.caption("Public (+) Reviews: {}".format("%s%%"%recommended_movie_reviews[35]))
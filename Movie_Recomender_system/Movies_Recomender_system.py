import streamlit as st 
import pandas as pd 
import pickle
import requests


def fetching_posters(movieid):
    response=requests.get(f'https://api.themoviedb.org/3/movie/{movieid}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
    data=response.json()
    return'https://image.tmdb.org/t/p/w500/'+ data['poster_path']


# Now fetching the top most matching movies from the similarities 
def fetching_movies(movie):
   index= data[data['title']==movie].index[0]
   distance=similarity[index]
   nearest_movies=sorted(enumerate(distance),reverse=True,key=lambda x:x[1])[1:6]
   recommended_movie=[]
   recommended_movies_poster=[]
   
   for i in nearest_movies:
       recommended_movie.append(data.iloc[i[0]].title)
       recommended_movies_poster.append(fetching_posters(data.iloc[i[0]].id))
   return recommended_movie,recommended_movies_poster
    
    
similarity=pickle.load(open('similarity_matrices.pkl','rb'))
st.title("Movies Recomender System")
data=pd.read_csv('Filtered_data.csv')
selected_movie=st.selectbox('According to which movie you want to recommendation ?',data['title'])
if  st.button('Recommend'):
    recommended_movies,recommended_movies_posters=fetching_movies(selected_movie)
    st.write('Here are Recommended Movies')
    cols = st.columns(len(recommended_movies))

    # Iterate over the columns, headers, and image URLs
    for col, header, url in zip(cols, recommended_movies, recommended_movies_posters):
       with col:
          st.text(header)
          st.image(url)
    
    

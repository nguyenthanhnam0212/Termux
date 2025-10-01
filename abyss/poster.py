import requests
import urllib.parse

class POSTER:
    def get_poster(name_movie_en):
        url_search = f'https://api.themoviedb.org/3/search/movie?api_key=58b5020e2f049f687252256dcd63c5f1&include_adult=true&query={urllib.parse.quote(name_movie_en)}'
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1OGI1MDIwZTJmMDQ5ZjY4NzI1MjI1NmRjZDYzYzVmMSIsInN1YiI6IjY1MWEzODdkOTY3Y2M3MzQyNjA5YjYxZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.cJt8xqD-6hLCjIr6uPSaGCl4NlYsWb5Fe6O1_an8loA"
        }
        
        response = requests.get(url_search, headers=headers)
        data = response.json()
        id_movie = ''

        if data['total_results'] == 1:
            id_movie = data['results'][0]['id']
         
        if id_movie != "":
            url_detail = f'https://api.themoviedb.org/3/movie/{id_movie}'
            response = requests.get(url_detail, headers=headers)
            detail = response.json()

            poster = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{detail['poster_path']}"

        else:
            poster = ""
            
        return poster
    
    def get_actor(name_movie_en):
        url = f'http://www.omdbapi.com/?apikey=c8490f5a&t={urllib.parse.quote(name_movie_en)}'
        response = requests.get(url)
        data = response.json()

        if data['Response'] == 'False':
            actor = ""
        else:
            actor = ""
            actor_str = data['Actors']
            actor_arr = actor_str.split(",")
            for i in actor_arr:
                ac = i.replace(" ","")
                actor = actor + f"#{ac}   "
        return actor.strip()
#Vaishnavi Manthena (vm504)
#Kruti Shah (ks1511)

from collections import defaultdict

#TASK 1 : READING DATA

#input: ratings file
#output: dictionary; key = movie; value = corresponding list of ratings
def read_ratings_data(f):
    file = open(f)
    d = defaultdict(list)
    for line in file:
        movie, rating, user_id = line.split('|')
        d[movie.strip()].append(float(rating.strip()))
    file.close()
    return dict(d)



#input: movies file
#output: dictionary; key = movie; value = genre
def read_movie_genre(f):
    file = open(f)
    d = {}
    for line in file:
        genre, movie_id, movie = line.split('|')
        d[movie.strip()] = genre.strip()
       
    file.close()
    return d


#TASK 2 : PROCESSING DATA

#input: movie to genre dictionary
#output: dictionary; key = genre; value = list of movies in this genre
def create_genre_dict(movie_to_genre):
    d = defaultdict(list)
    for key, value in movie_to_genre.items():
        d[value].append(key)
    return dict(d)


#input: movie to ratings dictionary
#output: dictionary; key = movie; value = average rating
def calculate_average_rating(movie_to_ratings):
    d = {}
    for key, value in movie_to_ratings.items():
        avg = sum(value)/len(value)
        avg_s = f'{avg:.4f}'
        avg_f = float(avg_s)
        d[key] = avg_f
    return d


#TASK 3: RECOMMENDATION

#1
#input: movie to average ratings dictionary, n
#output: dictionary of same structure but only with top n movies rating wise
def get_popular_movies(movie_to_avg_rating, n=10):
    
    #gives a list sorted in descending order based on value
    d = sorted(movie_to_avg_rating.items(), key = lambda x: x[1], reverse = True)
    
    if len(d) < n:
        n = len(d)
        
    d_final = d[:n]
    
    #create a dictionary from this truncated list
    
    return dict(d_final)


#2
#input: movie to average ratings dictionary, t
#output: dictionary of the same form but only including those items with value >= t
def filter_movies(movie_to_avg_rating, t=3):
    
    d = {}
    for key, value in movie_to_avg_rating.items():
        if value >= t:
            d[key] = value
            
            
    return d


#3
#input: genre, a genre-to-movies dictionary, a dictionary of movie:average rating, n 
#output: n most popular movies in that genre based on average ratings
def get_popular_in_genre(genre, genre_to_movies, movie_to_avg, n=5):
    
    value = genre_to_movies[genre]
    #value is the list of movies in this particular genre
    
    #create a list of tuples. tuple: (movie, avg rating) such that movie is in the value list
    d = [(x,y) for x,y in movie_to_avg.items() if x in value]
    
    if len(d) < n:
        n=len(d)
        
    d.sort(key = lambda x : x[1], reverse = True)
    
    d_final = d[:n]
    
    return dict(d_final)



#4
#input: genre, a genre-to-movies dictionary, a dictionary of movie:average rating
#output: average rating of movies in the given genre
def get_genre_rating(genre, genre_to_movies, movie_to_avg):
    
    value = genre_to_movies[genre]
    #value is the list of movies in this particular genre
    
    sum = 0
    count = len(value)
    
    for x,y in movie_to_avg.items():
        if x in value:
            sum+=y
            
    avg = sum/count
    avg_s =  f'{avg:.4f}'
    avg_f = float(avg_s)
    
    return avg_f


#5
#input: genre_to_movies dictionary, movie_to_avgRating dictionary, n
#output: top n rated genres as a dictionary of genre:average rating

def genre_popularity(genre_to_movies, movie_to_avgRating, n=5):
    
    #list of tuples (genre, averageRating)
    l = []
    for x in genre_to_movies.keys():
        avgRating = get_genre_rating(x, genre_to_movies, movie_to_avgRating)
        l.append((x, avgRating))
    
    l.sort(key = lambda x: x[1], reverse = True)
    
    if len(l) < n:
        n = len(l)
        
    return dict(l[0:n])



#TASK 4: USER FOCUSED

#1
def read_user_ratings(ratings):
    f = open(ratings)
    
    d = defaultdict(list)
    
    for line in f:
        
        movie, rating, uid = line.split('|')
        d[uid.strip()].append((movie.strip(), float(rating.strip())))
    
    f.close()
    return dict(d)

#2
#input: user id, the user-to-movies dictionary, and the movie-to-genre dictionary 
#output: top genre the user likes
def get_user_genre(uid, user_to_movies, movie_to_genre):
    
    if uid not in user_to_movies.keys():
        print('Error: User does not exist')
        return
    
    
    #creating a dictionary that is applicable to a particular user
    #key: genre 
    #value: (total rating given, #of movies that this total applies to)
    genre_ratings = {}
    
    value = user_to_movies[uid]
    #value holds [(Movie, rating), ....]
    
  
    #go through each item in value to finally create the dictionary
    
    for movie, rating in value:
        genre = movie_to_genre[movie];
        if genre in genre_ratings:
            totalRating, numMovies = genre_ratings[genre]
            genre_ratings[genre] = (totalRating + rating, numMovies + 1)
        else:
            genre_ratings[genre] = (rating,1)
        
    
    
    #creating a list of tuples. Each tuple: (genre, avgRating by uid)
    
    genre_ratings_list = []
    
    for genre, rating_stats in genre_ratings.items():
        genre_ratings_list.append((genre, rating_stats[0]/rating_stats[1]))
        
    genre_ratings_list.sort(key = lambda x: x[1], reverse = True)
    
    
    a,b = genre_ratings_list[0]
    return a
        
    
def recommend_movies(uid, user_to_rating, movie_to_genre, movie_to_avgRating):
    
    if uid not in user_to_rating.keys():
        print('Error: User does not exist')
        return
    
    top_choice = get_user_genre(uid, user_to_rating, movie_to_genre)
    
    #all the movies in the genre
    movies_in_genre = [x for x,y in movie_to_genre.items() if y == top_choice]
    #all the movies that the user has watched
    movies_watched = [m for m, r in user_to_rating[uid]]
    
    recommend = {}
    for movie in movies_in_genre:
        if movie not in movies_watched:
            recommend[movie] = movie_to_avgRating[movie]

    recommend = sorted(recommend.items(), key=lambda item: item[1], reverse = True)
    
    if len(recommend) <=3:
        n = len(recommend)
        
    return dict(recommend[:n])


#Testing
print("1.1")
movie_to_ratings = read_ratings_data('movieRatingSample.txt')
print(movie_to_ratings)

print("1.2")
movie_to_genre = read_movie_genre('genreMovieSample.txt')
print(movie_to_genre)

print("2.1")
genre_to_movies = create_genre_dict(movie_to_genre)
print(genre_to_movies)

print("2.2")
movie_to_avgRating = calculate_average_rating(movie_to_ratings)
print(movie_to_avgRating)

print("3.1")
print(get_popular_movies(movie_to_avgRating, 3))

print("3.2")
print(filter_movies(movie_to_avgRating, 2))

print("3.3")
print(get_popular_in_genre("Romance", genre_to_movies, movie_to_avgRating))


print("3.4")
print(get_genre_rating("Romance", genre_to_movies, movie_to_avgRating))

print(get_genre_rating("Comedy", genre_to_movies, movie_to_avgRating))


print("3.5")
print(genre_popularity(genre_to_movies, movie_to_avgRating))

print(genre_popularity(genre_to_movies, movie_to_avgRating, 1))

print(genre_popularity(genre_to_movies, movie_to_avgRating, 2))

print("4.1")
user_to_rating = read_user_ratings('movieRatingSample.txt')
print (user_to_rating)

print("4.2")
print(get_user_genre('1', user_to_rating, movie_to_genre ))

print(get_user_genre('18', user_to_rating, movie_to_genre ))

print(get_user_genre('6', user_to_rating, movie_to_genre ))

print(get_user_genre('19', user_to_rating, movie_to_genre ))

print("4.3")
print(recommend_movies('18', user_to_rating, movie_to_genre, movie_to_avgRating))

print(recommend_movies('19', user_to_rating, movie_to_genre, movie_to_avgRating))


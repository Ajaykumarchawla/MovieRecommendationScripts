#Task 1: Reading Data

# Write a function read_ratings_data(f) that takes in a ratings file, and returns a dictionary.
def read_ratings_data(f):
    movieRating = open(f)
    movie_ratings_dict  = {}
    for row in movieRating.read().split('\n'):
        row = row.split('|')
        if len(row) == 3 :
            if row[0] in movie_ratings_dict.keys():
                movie_ratings_dict[row[0]].append(float(row[1]))
            else:
                movie_ratings_dict[row[0]] = [float(row[1])]

    return movie_ratings_dict

ratingFile = "movieRatingSample.txt"
rattings = read_ratings_data(ratingFile)
print(rattings)

# Write a function read_movie_genre(f) that takes in a movies file and returns a dictionary
def read_movie_genre(f):
    movieGenre = open(f)
    movie_genre_dict  = {}
    for row in movieGenre.read().split('\n'):
        row = row.split('|')
        if len(row) == 3 :
            movie_genre_dict[row[2]] = row[0]
    
    return movie_genre_dict


genreFile = "genreMovieSample.txt"
movie_to_genre = read_movie_genre(genreFile)
print(movie_to_genre)
# Task 2: Processing Data

# Genre dictionary
def create_genre_dict(movie_to_genre):
    genre = {}
    for key in movie_to_genre:
        value = movie_to_genre[key]
        if value in genre.keys():
            genre[value].append(key)
        else:
            genre[value] = [key]
        
    return genre
genre_to_movie = create_genre_dict(movie_to_genre)
print(genre_to_movie)

# Average Rating
def calculate_average_rating(ratings):
    average_rating = {}
    for movie in ratings:
        average_rating[movie] = round(sum(rattings[movie])/len(rattings[movie]),1)
    return average_rating

movie_to_average = calculate_average_rating(rattings)
print(movie_to_average)

# Task 3: Recommendation

# Popularity based
def get_popular_movies(movie_to_average):
    return {k: v for k, v in sorted(movie_to_average.items(), key=lambda item: item[1],reverse=True)[0:10]}
    

# Threshold Rating
def filter_movies(movie_to_average, thresholdRatting = 3):
    print(movie_to_average)
    return {k: v for k, v in movie_to_average.items() if v >=thresholdRatting}


# Popularity + Genre based
def get_popular_in_genre(genre,genre_to_movie,movie_to_average,n=5):
    movies={p:q for (p,q) in movie_to_average.items() if p in genre_to_movie[genre]}
    return {k: v for k, v in sorted(movies.items(), key=lambda item: item[1],reverse=True)[0:n]}

# Genre Rating
def get_genre_rating(genre,genre_to_movie,movie_to_average):
    movies={p:q for (p,q) in movie_to_average.items() if p in genre_to_movie[genre]}
    return sum(movies.values())/len(movies)


# Genre Popularity
def genre_popularity(genre_to_movie,movie_to_average,n = 5):
    movies = {k:get_genre_rating(k,genre_to_movie,movie_to_average) for k in [key for key,v in genre_to_movie.items()]}
    return {k: v for k, v in sorted(movies.items(), key=lambda item: item[1],reverse=True)[0:n]}



# Task 4 (User Focused)

# read_user_ratings
def read_user_ratings(f):
    movieRating = open(f)
    movie_ratings_dict  = {}
    for row in movieRating.read().split('\n'):
        row = row.split('|')
        if len(row) == 3 :
            if row[2] in movie_ratings_dict.keys():
                movie_ratings_dict[row[2]].append((row[0],float(row[1])))
            else:
                movie_ratings_dict[row[2]] = [(row[0],float(row[1]))]

    return movie_ratings_dict
    

user_to_movie = read_user_ratings(ratingFile)
print(user_to_movie)

def get_user_genre(user_id,user_to_movie,movie_to_genre):
    genre_rating ={v:[n for (k,n) in user_to_movie[user_id] if movie_to_genre[k] == v] for (k,v) in movie_to_genre.items() if k in [i[0] for i in user_to_movie[user_id]]}
    genre_average ={k:round(sum(v)/len(v),2) for k,v in genre_rating.items()}
    max_key = max(genre_average, key=genre_average.get)
    return max_key
    # print({k:k for k in genre})


# recommend_movies 

def recommend_movies(user_id,user_to_movie,movie_to_genre,movie_to_average):
    genre = get_user_genre('1',user_to_movie,movie_to_genre)

    movies_of_genre = {k:movie_to_average[k] for k,v in movie_to_genre.items() if v == genre and k not in user_to_movie[user_id][0]}
    top_picks = {k: v for k, v in sorted(movies_of_genre.items(), key=lambda item: item[1],reverse=True)[0:3]}
    return top_picks



print(recommend_movies('6',user_to_movie,movie_to_genre,movie_to_average))
# for row in get_user_genre('1',user_to_movie,movie_to_genre).items():
#     print(row)


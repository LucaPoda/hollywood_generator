import random
import psycopg2
from configparser import ConfigParser

spielberg = ("Spielberg", 1946)

def config(filename='connection.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	    # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()

        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def read_file(filename):
    data = []
    with open(filename) as file:
        for l in file.readlines():
            data.append(l.strip('\n'))
    return data


def get_progress_bar(cur, tot):
    length = 100
    if tot == 0:
        percentage = length
    else:
        percentage = cur/tot*length
    bar = ""
    for j in range(0, length):
        if j < percentage:
            bar += "#"
        else:
            bar += " "
    bar += " - " + '{:.2f}%'.format(cur/tot*100 if tot > 0 else 0) + " - " + str(cur) + "/" + str(tot)
    return bar

def random_title(male_names, female_names, objects):
    return random.choice(male_names) + ", " + random.choice(female_names) + " e " + random.choice(objects) + " di " + random.choice(male_names+female_names)

def random_name(male_names, female_names, surnames):
    return random.choice(male_names+female_names) + " " + random.choice(surnames)

def random_director(male_names, female_names, surnames):
    return (random_name(male_names, female_names, surnames), random.randint(1935, 2005))

def random_movie(director, male_names, female_names, objects):
    budget = random.randint(10_000, 500_000_000)
    return (
        random_title(male_names, female_names, objects), 
        random.randint(director[1], 2022), 
        director[0], 
        budget, 
        random.randint(int(budget/4), budget*random.randint(1, 3))
    )

def random_directoraward(director, awards, results):
    return (
        director[0],
        random.randint(director[1], 2022),
        random.choice(awards) + ", best director",
        random.choice(results)
    )

def random_movieaward(movie, awards, results, award_categories):
    return (
        movie[0],
        movie[1],
        random.choice(awards) + ", " + random.choice(award_categories),
        random.choice(results)
    )

def push_data(conn, data, query):
    tot = len(data)
    for i, record in enumerate(data):
        print (record)
        cur.execute(query, record)
        if i > 0:
            print ("\033[A                             \033[A")
        print("Inserting directors:  " + get_progress_bar(i, tot))
    
    conn.commit()
    print ("\033[A                             \033[A")
    print("Inserting directors:  " + get_progress_bar(tot, tot))

def generate_directors(count, male_names, female_names, surnames):
    directors = []
    for i in range(0, count-1):
        found = True
        while (found == True):
            director = random_director(male_names, female_names, surnames)
            found = False
            for d in directors:
                if d[0] == director[0]:
                    found = True
        directors.append(director)
        if i > 0:
            print ("\033[A                             \033[A")
        print("Generating directors: " + get_progress_bar(i, count))
        
    directors.append(spielberg)
    print ("\033[A                             \033[A")
    print("Generating directors: " + get_progress_bar(count, count))
    return directors

def generate_directorawards(directors, count, awards, results):
    directorawards = []
    for i, director in enumerate(directors):
        n = random.randint(0, count)
        for j in range(0, n):
            found = True
            while (found == True):
                award = random_directoraward(director, awards, results)
                found = False
                for a in directorawards:
                    if a[0] == award[0] and a[1] == award[1] and a[2] == award[2]:
                        found = True
            directorawards.append(award)
        if i > 0:
            print ("\033[A                             \033[A")
        print("Generating director awards: " + get_progress_bar(i, len(directors)))

    print ("\033[A                             \033[A")
    print("Generating director awards: " + get_progress_bar(len(directors), len(directors)))
    return directorawards

def generate_movies(directors, count, male_names, female_names, objects):
    movies = []
    for i, director in enumerate(directors):
        if random.randint(0, 3) == 0:
            continue
        n = random.randint(0, count)
        for j in range(0, n):
            found = True
            while (found == True):
                movie = random_movie(director, male_names, female_names, objects)
                found = False
                for m in movies:
                    if m[0] == movie[0] and m[1] == movie[1]:
                        found = True
            movies.append(movie)
        if i > 0:
            print ("\033[A                             \033[A")
        print("Generating movies:  " + get_progress_bar(i, len(movies)))

    for i in range(0, random.randint(10, 40)):
        found = True
        while (found == True):
            movie = random_movie(spielberg, male_names, female_names, objects)
            found = False
            for m in movies:
                if m[0] == movie[0] and m[1] == movie[1]:
                    found = True
        movies.append(movie)
    
    print ("\033[A                             \033[A")
    print("Generating movies:  " + get_progress_bar(len(movies), len(movies)))
    return movies

def generate_movieawards(movies, awards, results, award_categories):
    movieawards = []
    for i, movie in enumerate(movies):
        if random.randint(0, 3) == 0:
            continue
        for j in range(0, random.randint(0, len(awards))):
            found = True
            while (found == True):
                award = random_movieaward(movie, awards, results, award_categories)
                found = False
                for a in movieawards:
                    if a[0] == award[0] and a[1] == award[1] and a[2] == award[2]:
                        found = True
            movieawards.append(award)
        if i > 0:
            print ("\033[A                             \033[A")
        print("Generating movie awards:  " + get_progress_bar(i, len(movies)))
    
    print ("\033[A                             \033[A")
    print("Generating movie awards:  " + get_progress_bar(len(movies), len(movies)))
    return movieawards

def push_directors(conn, directors):
    push_data(conn, directors, "insert into directors values (%s, %s)")

def push_directorawards(conn, directorawards):
    push_data(conn, directorawards, "insert into directorawards values (%s, %s, %s, %s)")

def push_movies(conn, movies):
    push_data(conn, movies, "insert into movies values (%s, %s, %s, %s, %s)")

def push_movieawards(conn, movieawards):
    push_data(conn, movieawards, "insert into movieawards values (%s, %s, %s, %s)")

if __name__ == "__main__":
    conn = connect()
    
    if conn is not None:
        try:
            cur = conn.cursor()
            try:
                confirm = input("Are you sure to start the process? All data in the database will be deleted. [Y, n]")
                print("'" + confirm + "'")
                if (confirm == 'Y' or confirm == ''):
                    print("Deleting movieawards...")
                    cur.execute("delete from movieawards")
                    print("Deleting movies...")
                    cur.execute("delete from movies")
                    print("Deleting direcotrawards...")
                    cur.execute("delete from directorawards")
                    print("Deleting directors...")
                    cur.execute("delete from directors")

                    conn.commit()

                    print("All data had been deleted successfully!")

                    n_directors = input("Number of directors: [200] ")
                    if n_directors == '':
                        n_directors = 200
                    n_d_awards = input("Maximum number of awards for each director? [50] ")
                    if n_d_awards == '':
                        n_d_awards = 50
                    n_movies = input("Maximum number of movies for each director? [40] ")
                    if n_movies == '':
                        n_movies = 40

                    awards = read_file('data/awards.txt')
                    award_categories = read_file('data/award_categories.txt')
                    female_names = read_file('data/male_names.txt')
                    male_names = read_file('data/male_names.txt')
                    objects = read_file('data/objects.txt')
                    results = read_file('data/results.txt')
                    surnames = read_file('data/surnames.txt')
                    

                    directors = generate_directors(int(n_directors), male_names, female_names, surnames)
                    push_directors(conn, directors)

                    directorawards = generate_directorawards(directors, int(n_d_awards), awards, results)
                    push_directorawards(conn, directorawards)

                    movies = generate_movies(directors, int(n_movies), male_names, female_names, objects)
                    push_movies(conn, movies)    
                
                    movieawards = generate_movieawards(movies, awards, results, award_categories)
                    push_movieawards(conn, movieawards)
            finally:
                cur.close()
        finally:
            conn.close()
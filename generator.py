import random
import psycopg2
from configparser import ConfigParser

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

male_names = [
    "Leonardo",
    "Francesco",
    "Alessandro",
    "Lorenzo",
    "Mattia",
    "Tommaso",
    "Gabriele",
    "Andrea",
    "Riccardo",
    "Edoardo"
]

female_names = [
    "Sofia",
    "Giulia",
    "Aurora",
    "Ginevara",
    "Alice",
    "Beatrice",
    "Emma",
    "Giorgia",
    "Vittoria",
    "Matilde"
]

surnames = [
    "Rossi",
    "Ferrari",
    "Russo",
    "Bianchi",
    "Romano",
    "Gallo",
    "Costa",
    "Fontana",
    "Conti",
    "Esposito",
    "Ricci",
    "Bruno",
    "De Luca",
    "Moretti",
    "Marino",
    "Greco",
    "Barbieri",
    "Lombardi",
    "Giordano",
    "Cassano",
    "Colombo",
    "Mancini",
    "Longo",
    "Leone",
    "Martinelli",
    "Marchetti",
    "Martini",
    "Galli",
    "Gatti",
    "Mariani",
    "Ferrara",
    "Santoro",
    "Marini",
    "Bianco",
    "Conte",
    "Serra",
    "Farina",
    "Gentile",
    "Caruso",
    "Morelli",
    "Ferri",
    "Testa",
    "Ferraro",
    "Pellegrini",
    "Grassi",
    "Rossetti",
    "D'Angelo",
    "Bernardi",
    "Mazza",
    "Rizzi",
    "Natale"
]

objects = [
    "il libro",
    "la matita",
    "la gomma",
    "l'album",
    "il computer",
    "lo smartphone",
    "la lavagna",
    "il quaderno",
    "la stoffa",
    "il filo",
    "la cera",
    "la colla",
    "la forbice",
    "il vaso",
    "il piatto",
    "il bicchiere",
    "la forchetta",
    "il cucchiaio",
    "il coltello",
    "la posata",
    "il tegame",
    "la padella",
    "il cucchiaio di legno",
    "il mestolo",
    "la spatola",
    "il pentolino",
    "la tazza",
    "il piattino",
    "il vassoio",
    "il tovagliolo",
    "il tovagliolo di carta",
    "la tovaglia",
    "il tappeto",
    "il divano",
    "la poltrona",
    "il pouf",
    "il letto",
    "la sedia",
    "il tavolo",
    "il cassetto",
    "l'armadio",
    "l'anta",
    "il comò",
    "il comodino",
    "il tavolino",
    "la scrivania",
    "la sedia da ufficio",
    "il computer portatile",
    "la stampante",
    "la fotocopiatrice",
    "la macchina del fax",
    "il telefono",
    "il televisore",
    "il videoregistratore",
    "il DVD player",
    "l'impianto stereo",
    "la cassa acustica",
    "il microfono",
    "il radiomicrofono",
    "il computer fisso",
    "lo schermo del computer",
    "la tastiera",
    "il mouse",
    "la penna",
    "la matita",
    "la gomma",
    "il temperamatite",
    "il righello",
    "la lavagna",
    "la lavagna luminosa",
    "il proiettore",
    "il retroproiettore",
    "l'impianto di illuminazione",
    "il faretto",
    "la lampada",
    "il lampadario",
    "il soffitto",
    "il pavimento",
    "il muro",
    "la porta",
    "la finestra",
    "il cassetto",
    "il lavandino",
    "il lavandino della cucina",
    "il lavabo",
    "il lavabo della cucina",
    "il water",
    "il bidè",
    "la doccia",
    "la vasca da bagno",
    "il lavandino del bagno",
    "il lavabo del bagno",
    "il water del bagno",
    "lo specchio",
    "il lavandino",
    "il lavabo",
    "il water",
    "il bidè",
    "la doccia",
    "la vasca da bagno"
]

awards = [
    "Cannes International Film Festival",
    "Venice International Film Festival",
    "Moscow International Film Festival",
    "Istanbul Animation Festival",
    "BFI London Film Festival",
    "oscar"
]

award_categories = [
    "best director",
    "best visual effects",
    "best sound mixing",
    "best pictures",
    "best original story"
]

results = [
    "won",
    "nominated"
]

spielberg = ("Spielberg", 1946)

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
    bar += " - " + '{:.2f}%'.format(cur/tot*100) + " - " + str(cur) + "/" + str(tot)
    return bar

def random_title():
    return random.choice(male_names) + ", " + random.choice(female_names) + " e " + random.choice(objects) + " di " + random.choice(male_names+female_names)

def random_name():
    return random.choice(male_names+female_names) + " " + random.choice(surnames)

def random_director():
    return (random_name(), random.randint(1935, 2005))

def random_movie(director):
    budget = random.randint(10_000, 500_000_000)
    return (
        random_title(), 
        random.randint(director[1], 2022), 
        director[0], 
        budget, 
        random.randint(int(budget/4), budget*random.randint(1, 3))
    )

def random_directoraward(director):
    return (
        director[0],
        random.randint(director[1], 2022),
        random.choice(awards) + ", best director",
        random.choice(results)
    )

def random_movieaward(movie):
    return (
        movie[0],
        movie[1],
        random.choice(awards) + ", " + random.choice(award_categories),
        random.choice(results)
    )

def generate_directors(count):
    directors = []
    for i in range(0, count-1):
        found = True
        while (found == True):
            director = random_director()
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

def push_directors(conn, directors):
    tot = len(directors)
    for i, director in enumerate(directors):
        cur.execute("insert into directors values (%s, %s)", director)
        if i > 0:
            print ("\033[A                             \033[A")
        print("Inserting directors:  " + get_progress_bar(i, len(directors)))
    
    conn.commit()
    print ("\033[A                             \033[A")
    print("Inserting directors:  " + get_progress_bar(len(directors), len(directors)))

def generate_directorawards(directors, count):
    directorawards = []
    for i, director in enumerate(directors):
        n = random.randint(0, count)
        for j in range(0, n):
            found = True
            while (found == True):
                award = random_directoraward(director)
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

def push_directorawards(conn, directorawards):
    tot = len(directorawards)
    for i, directoraward in enumerate(directorawards):
        cur.execute("insert into directorawards values (%s, %s, %s, %s)", directoraward)
        if i > 0:
            print ("\033[A                             \033[A")
        print("Inserting director awards: " + get_progress_bar(i, len(directorawards)))
    conn.commit()
    print ("\033[A                             \033[A")
    print("Inserting director awards: " + get_progress_bar(len(directorawards), len(directorawards)))

def generate_movies(directors, count):
    movies = []
    for i, director in enumerate(directors):
        if random.randint(0, 3) == 0:
            continue
        n = random.randint(0, count)
        for j in range(0, n):
            found = True
            while (found == True):
                movie = random_movie(director)
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
            movie = random_movie(spielberg)
            found = False
            for m in movies:
                if m[0] == movie[0] and m[1] == movie[1]:
                    found = True
        movies.append(movie)
    
    print ("\033[A                             \033[A")
    print("Generating movies:  " + get_progress_bar(len(movies), len(movies)))
    return movies

def push_movies(conn, movies):
    tot = len(movies)
    for i, movie in enumerate(movies):
        cur.execute("insert into movies values (%s, %s, %s, %s, %s)", movie)
        if i > 0:
            print ("\033[A                             \033[A")
        print("Inserting movies: " + get_progress_bar(i, len(movies)))
    conn.commit()
    print ("\033[A                             \033[A")
    print("Inserting movies: " + get_progress_bar(len(movies), len(movies)))

def generate_movieawards(movies):
    movieawards = []
    for i, movie in enumerate(movies):
        n = random.randint(0, 3)
        for j in range(0, n):
            found = True
            while (found == True):
                award = random_movieaward(movie)
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

def push_movieawards(conn, movieawards):
    tot = len(movieawards)
    for i, movieaward in enumerate(movieawards):
        cur.execute("insert into movieawards values (%s, %s, %s, %s)", movieaward)
        if i > 0:
            print ("\033[A                             \033[A")
        print("Inserting movie awards: " + get_progress_bar(i, len(movieawards)))
    conn.commit()
    print ("\033[A                             \033[A")
    print("Inserting movies awards: " + get_progress_bar(len(movieawards), len(movieawards)))

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

                    directors = generate_directors(int(n_directors))
                    push_directors(conn, directors)

                    directorawards = generate_directorawards(directors, int(n_d_awards))
                    push_directorawards(conn, directorawards)

                    movies = generate_movies(directors, int(n_movies))
                    push_movies(conn, movies)    
                
                    movieawards = generate_movieawards(movies)
                    push_movieawards(conn, movieawards)
            finally:
                cur.close()
        finally:
            conn.close()
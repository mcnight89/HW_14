import sqlite3
import json

import flask


def run_sql(sql_query):
    with sqlite3.connect('netflix.db') as connection:
        connection.row_factory = sqlite3.Row
        result = []
        for item in connection.execute(sql_query).fetchall():
            result.append(dict(item))

        return result


def search_title(user_input):
    """ Поиск по названию фильма"""

    with sqlite3.connect('netflix.db') as connection:
        result = connection.cursor()
        sql_query = """
                        SELECT title, country, release_year, listed_in, description
                        FROM netflix
                        WHERE title = ?
                        ORDER BY release_year DESC
                        LIMIT 1
           """

        result.execute(sql_query, (user_input.title(),))
        movies = result.fetchall()
        chosen_movie = {}
        for item in movies:
            chosen_movie["title"] = item[0]
            chosen_movie["country"] = item[1]
            chosen_movie["release_year"] = item[2]
            chosen_movie["listed_in"] = item[3]
            chosen_movie["description"] = item[4].strip()
        return chosen_movie


def search_by_period(year_one, year_two):
    """Поиск по годам"""

    with sqlite3.connect('netflix.db') as connection:
        result = connection.cursor()
        sql_query = """
                        SELECT title, release_year
                        FROM netflix
                        WHERE release_year BETWEEN ? AND ?
                        ORDER BY release_year DESC
                        LIMIT 30
           """

        result.execute(sql_query, (year_one, year_two))
        movies = result.fetchall()
        movies_by_period = []
        for movie in movies:
            chosen_movie = dict()
            chosen_movie["title"] = movie[0]
            chosen_movie["release_year"] = movies[1]
            movies_by_period.append(chosen_movie)

    return movies_by_period


def search_by_rating(user_rating):
    """ поиск по рейтингу"""

    with sqlite3.connect('netflix.db') as connection:
        result = connection.cursor()
        if user_rating.strip().lower() == "children".strip().lower():
            sql_query = """
                           SELECT title, rating, description
                           FROM netflix
                           WHERE rating = 'G'
                           LIMIT 100
              """

            result.execute(sql_query)
        elif user_rating.strip().lower() == "family".strip().lower():
            sql_query = """
                           SELECT title, rating, description
                           FROM netflix
                           WHERE rating = 'PG-13' OR rating = 'G'
                           LIMIT 100
              """

            result.execute(sql_query)

        elif user_rating.strip().lower() == "adult".strip().lower():
            sql_query = """
                           SELECT title, rating, description
                           FROM netflix
                           WHERE rating = 'NC- 17' OR rating = 'R'
                           LIMIT 100
              """

            result.execute(sql_query)
        movies = result.fetchall()
        movies_by_rating = []
        for movie in movies:
            chosen_movie = dict()
            chosen_movie["title"] = movie[0]
            chosen_movie["rating"] = movie[1]
            chosen_movie["description"] = movie[2].strip()
            movies_by_rating.append(chosen_movie)
    return movies_by_rating


def search_by_genre(genre):
    """  Поиск по жанру"""

    with sqlite3.connect('netflix.db') as connection:
        result = connection.cursor()
        sql_query = """
                    SELECT title, description
                    FROM netflix
                    WHERE listed_in = ?
                    ORDER BY release_year DESC
                    LIMIT 10
        """
        result.execute(sql_query, (genre,))
        movies = result.fetchall()
        chosen_movie_list = []
        for movie in movies:
            chosen_movie = dict()
            chosen_movie["title"] = movie[0]
            chosen_movie["description"] = movie[1].strip()
            chosen_movie_list.append(chosen_movie)
        return chosen_movie_list


def search_by_actors(name1='Rose McIver', name2='Ben Lamb'):
    """  Поиск по актерам   """

    sql_query = f"""
                    SELECT 'cast'
                    FROM netflix
                    WHERE 'cast' LIKE '%{name1}%'
                    AND 'cast' LIKE '%{name2}%'
        """

    result = run_sql(sql_query)

    main_name = {}

    for item in result:
        names = item.get('cast').split(", ")
        for name in names:
            if name in main_name.keys():
                main_name[name] += 1
            else:
                main_name[name] = 1

    for item in main_name:
        if item not in (name1, name2) and main_name[item] >= 2:
            print(item)


print(search_by_actors(name1='Rose McIver', name2='Ben Lamb'))


def search_by_types(types='TV Show', release_year=2021, genre='TV'):
    """ """

    sql_query = f"""
                    SELECT title, description
                    FROM netflix
                    WHERE 'type' = '{types}'
                    AND release_year = '{release_year}'
                    AND listed_in LIKE '%{genre}%'
        """

    return json.dumps(run_sql(sql_query), indent=4)


print(search_by_types(types='TV Show', release_year=2021, genre='TV'))

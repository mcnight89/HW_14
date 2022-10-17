from flask import Flask, jsonify, Flask

import utils

app = Flask(__name__)

# чтение кириллицы
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/movie/<title>', methods=['GET'])
def get_by_title(title):
    movies = utils.search_title(title)
    return jsonify(movies)


@app.route('/movie/<year_one>/to/<year_two>', methods=['GET'])
def get_by_period(year_one, year_two):
    movies = utils.search_by_period(year_one, year_two)
    return jsonify(movies)


@app.route('/movies/<rating>', methods=['GET'])
def get_by_rating(rating):
    movies = utils.search_by_rating(rating)
    return jsonify(movies)


@app.route('/genre/<genre>', methods=['GET'])
def get_by_genre(genre):
    movies = utils.search_by_genre(genre)
    return jsonify(movies)


if __name__ == '__main__':
    app.run(debug=True)

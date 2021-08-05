from flask import Flask
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_scores.db'
db = SQLAlchemy(app)

CORS(app)

class GameScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return 'Game ' + str(self.id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scores', methods=['GET', 'POST'])
def posts():
    all_scores = GameScore.query.order_by(GameScore.score.desc()).all()

    player_name=""
    player_score=""
    if request.method == 'POST':
        player_name = request.form['name']
        player_all_scores = GameScore.query.filter_by(name=player_name).order_by(GameScore.score.desc()).all()
        if len(player_all_scores)>0:
            player_score=player_all_scores[0].score
        else:
            player_name = "player not found"

    return render_template('scores.html', scores=all_scores, player=player_name, highscore = player_score)


@app.route('/post_score', methods=['POST'])
def post_score():
    game_data = request.get_json()
    name = game_data['name']
    score = game_data['score']
    new_game_score = GameScore(name=name, score=score)
    db.session.add(new_game_score)
    db.session.commit()
    return 'Score saved.'


if __name__ == "__main__":
    app.run(debug=True)






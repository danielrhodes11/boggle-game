from boggle import Boggle
from flask import Flask, render_template, session, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.debug=True

toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def home_page():
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    return render_template("home.html", board=board,
                           highscore=highscore,
                           nplays=nplays)


@app.route('/check-word', methods = ['POST'])
def check_word():
    word = request.json.get('word')
    board = session['board']
    res = boggle_game.check_valid_word(board, word)

    return jsonify({'result' : res})


@app.route('/post-score', methods = ['POST'])
def post_score():
    score = request.json['score']
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)




    


    
       



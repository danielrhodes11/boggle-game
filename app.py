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
    """render home page with game board, high score, and n plays"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)
    score = 0

    return render_template("home.html", board=board,
                           highscore=highscore,
                           nplays=nplays,
                           score = score)


@app.route('/check-word', methods = ['POST'])
def check_word():
    """check if word is valid on the game board"""
    word = request.json.get('word')
    board = session['board']
    res = boggle_game.check_valid_word(board, word)

    return jsonify({'result' : res})


@app.route('/post-score', methods = ['POST'])
def post_score():
    """Update highscore and number of plays, and check if the score broke the previous record"""
    score = request.json['score']
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore or score)

    return jsonify(brokeRecord=score > highscore)




    


    
       



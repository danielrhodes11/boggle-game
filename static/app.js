class BoggleGame {
    constructor() {
      this.score = 0;
      this.scoreElement = $('#score');
      this.highscoreElement = $('#highscore');
      this.timer = null;
      this.timerElement = $('#timer');
      this.usedWords = []
  
      this.initialize();
    }
  
    initialize() {
      $('#word-guess-form').submit((e) => {
        e.preventDefault();
        const word = $('input[name=word]').val();
        if (this.usedWords.includes(word)) {
            this.showResultMessage('Word already used!');
        } else {
            this.usedWords.push(word);
            this.sendWordToServer(word);
          }
        });
    
        this.startTimer(61);
      }
  
    sendWordToServer(word) {
      axios.post('/check-word', { word })
        .then((response) => {
          this.handleResponse(response.data.result);
          const score = parseInt(this.scoreElement.text());
          this.postScoreToServer(score);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  
    handleResponse(result) {
      if (result === 'ok') {
        const word = $('input[name=word]').val();
        this.score += word.length;
        this.showResultMessage('Word found!');
        this.updateScoreElement();
      } else if (result === 'not-on-board') {
        this.showResultMessage('Word not on board');
      } else if (result === 'not-a-word') {
        this.showResultMessage('Not a word');
      }
    }
  
    showResultMessage(message) {
      alert(message);
      $('input[name=word]').val('');
    }
  
    updateScoreElement() {
      this.scoreElement.text(this.score);
    }
  
    postScoreToServer(score) {
      axios.post('/post-score', { score })
        .then((response) => {
          const brokeRecord = response.data.brokeRecord;
          if (brokeRecord && !this.roundHighscore) {
            this.roundHighscore = true;
          }

  
          const remainingSeconds = parseInt(this.timerElement.text());
          if (remainingSeconds === 0) {
            this.endGame();
          }
        });
    }
  
    startTimer(seconds) {
      let remainingSeconds = seconds;
  
      this.timer = setInterval(() => {
        remainingSeconds--;
        if (remainingSeconds >= 0) {
          this.displayTimer(remainingSeconds);
        }
        if (remainingSeconds === 0) {
          clearInterval(this.timer);
          this.disableGuessing();
          this.endGame();
          
        }
      }, 1000);
    }
  
    displayTimer(seconds) {
      this.timerElement.text(seconds + 's');
    }
  
    disableGuessing() {
      $('#word-guess-form button').prop('disabled', true);
    }
  
    endGame() {
      const finalScore = parseInt(this.scoreElement.text());
      const currentHighscore = parseInt(this.highscoreElement.text());
      if (finalScore > currentHighscore) {
        this.highscoreElement.text(finalScore);
        alert('Game over! You achieved a new high score!');
      } else {
        alert('Game over!');
      }
    }
  }
  
  $(document).ready(() => {
    new BoggleGame();
  });
  
  






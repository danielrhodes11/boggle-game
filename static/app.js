class BoggleGame {
    constructor() {
      this.score = 0;
      this.scoreElement = $('#score');
      this.highscoreElement = $('#highscore');
      this.timer = null;
      this.timerElement = $('#timer');
      this.usedWords = [];
      this.roundHighscore = false;
  
      this.initialize();
    }
  
    // Initializes the game
  initialize() {
    $('#word-guess-form').submit((e) => {
      e.preventDefault();
      const word = $('input[name=word]').val();
      if (this.usedWords.includes(word) && word.length > 1) {
        this.showResultMessage('Word already used!'); 
      } else {
        this.usedWords.push(word); 
        this.sendWordToServer(word); 
      }
    });

    this.startTimer(11); 
  }

  // Sends the word to the server for validation
  sendWordToServer(word) {
    if (word.length < 2){
      alert('Please enter a word with 2 or more characters')
      return
    }
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

  // Handles the server's response after sending a word
  handleResponse(result) {
    if (result === 'ok') {
      const word = $('input[name=word]').val();
      this.score += word.length; 
      this.showResultMessage('Word found!'); 
      this.updateScoreElement(); 
    } else if (result === 'not-on-board') {
      this.showResultMessage('Word not on board');
    } else if (result === 'not-word') {
      this.showResultMessage('Not a word'); 
    }
  }

  // Displays a message to the player
  showResultMessage(message) {
    alert(message); 
    $('input[name=word]').val(''); 
  }

  // Updates the score element in the HTML
  updateScoreElement() {
    this.scoreElement.text(this.score); 
  }

  // Sends the player's score to the server for recording and checks if it broke the high score
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
  
    // Starts the timer countdown for the specified number of seconds
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

    // Updates the timer element in the HTML with the remaining seconds
    displayTimer(seconds) {
      this.timerElement.text(seconds + 's');
    }

    // Disables the word guessing input and button
    disableGuessing() {
      $('#word-guess-form button').prop('disabled', true);
    }

    // Ends the game
    endGame() {
      const finalScore = parseInt(this.scoreElement.text());
      const currentHighscore = parseInt(this.highscoreElement.text());
      const submitBtn = $('#submit')

      submitBtn.addClass('game-ended')

      if (finalScore > currentHighscore) {
        this.highscoreElement.text(finalScore);
        this.roundHighscore = true;
        alert('Game over! You achieved a new high score!');
      } else {
        alert('Game over!');
      }
    }
  }
  
  $(document).ready(() => { 
    new BoggleGame();
  });
  
  






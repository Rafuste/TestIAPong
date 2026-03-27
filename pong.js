const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const PADDLE_WIDTH = 15;
const PADDLE_HEIGHT = 80;
const BALL_RADIUS = 10;
const PLAYER_PADDLE_SPEED = 6; // Player paddle speed
const AI_PADDLE_SPEED = 4;    // AI paddle speed, slightly slower to be beatable
const INITIAL_BALL_SPEED_X = 5;
const INITIAL_BALL_SPEED_Y = 5;

// Game Modes Configuration
const QUICK_MATCH_SCORE_LIMIT = 5;
const ARCADE_START_LIVES = 5;
const ARCADE_POINTS_PER_GOAL = 100;
const HIGH_SCORES_KEY = 'pongArcadeHighScores';

let player = {
  x: 20,
  y: canvas.height / 2 - PADDLE_HEIGHT / 2,
  width: PADDLE_WIDTH,
  height: PADDLE_HEIGHT,
  score: 0,
  dy: 0 // For keyboard movement
};

let ai = {
  x: canvas.width - PADDLE_WIDTH - 20,
  y: canvas.height / 2 - PADDLE_HEIGHT / 2,
  width: PADDLE_WIDTH,
  height: PADDLE_HEIGHT,
  score: 0
};

let ball = {
  x: canvas.width / 2,
  y: canvas.height / 2,
  radius: BALL_RADIUS,
  dx: INITIAL_BALL_SPEED_X,
  dy: INITIAL_BALL_SPEED_Y
};

let gameMode = 'quick_match'; // 'quick_match' or 'arcade'
let playerLives = ARCADE_START_LIVES;
let playerArcadePoints = 0;
let gameOver = false;

function resetBall() {
  ball.x = canvas.width / 2;
  ball.y = canvas.height / 2;
  ball.dx = (Math.random() > 0.5 ? 1 : -1) * INITIAL_BALL_SPEED_X; // Random initial X direction
  ball.dy = (Math.random() * 2 - 1) * INITIAL_BALL_SPEED_Y; // Random initial Y direction (-INITIAL_BALL_SPEED_Y to +INITIAL_BALL_SPEED_Y)
}

function resetGame(mode) {
  gameMode = mode;
  player.score = 0;
  ai.score = 0;
  playerLives = ARCADE_START_LIVES;
  playerArcadePoints = 0;
  gameOver = false;
  resetBall();
  drawScore(); // Update scoreboard on reset
}

function drawRect(x, y, width, height, color) {
  ctx.fillStyle = color;
  ctx.fillRect(x, y, width, height);
}

function drawCircle(x, y, radius, color) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2, false);
  ctx.closePath();
  ctx.fill();
}

function drawScore() {
  // Scoreboard in the HTML
  if (gameMode === 'quick_match') {
    document.getElementById('player-score').innerText = player.score;
    document.getElementById('ai-score').innerText = ai.score;
  } else { // Arcade Mode
    document.getElementById('player-score').innerText = `Vidas: ${playerLives}`;
    document.getElementById('ai-score').innerText = `Puntos: ${playerArcadePoints}`;
  }
}

function update() {
  if (gameOver) return;

  // Move player paddle (keyboard)
  player.y += player.dy;
  if (player.y < 0) player.y = 0;
  if (player.y + player.height > canvas.height) player.y = canvas.height - player.height;

  // Move AI paddle
  // Simple AI: follow the ball's y position, but slightly slower
  const aiCenter = ai.y + ai.height / 2;
  if (aiCenter < ball.y - AI_PADDLE_SPEED / 2) { // Add a small buffer/delay
    ai.y += AI_PADDLE_SPEED;
  } else if (aiCenter > ball.y + AI_PADDLE_SPEED / 2) { // Add a small buffer/delay
    ai.y -= AI_PADDLE_SPEED;
  }
  // Keep AI paddle within bounds
  if (ai.y < 0) ai.y = 0;
  if (ai.y + ai.height > canvas.height) ai.y = canvas.height - ai.height;

  // Move ball
  ball.x += ball.dx;
  ball.y += ball.dy;

  // Ball collision with top/bottom walls
  if (ball.y + ball.radius > canvas.height || ball.y - ball.radius < 0) {
    ball.dy *= -1;
  }

  // Ball collision with paddles
  let collisionOccured = false;
  if (ball.dx < 0) { // Ball moving left (towards player)
    if (ball.x - ball.radius < player.x + player.width &&
        ball.y > player.y && ball.y < player.y + player.height) {
      collisionOccured = true;
      // Adjust ball direction based on where it hit the paddle
      let collidePoint = ball.y - (player.y + player.height / 2);
      collidePoint = collidePoint / (player.height / 2); // Normalize to -1 to 1
      ball.dx *= -1;
      ball.dy = collidePoint * INITIAL_BALL_SPEED_Y * 1.2; // Increase vertical speed slightly
      ball.dx *= 1.05; // Increase horizontal speed
    }
  } else { // Ball moving right (towards AI)
    if (ball.x + ball.radius > ai.x &&
        ball.y > ai.y && ball.y < ai.y + ai.height) {
      collisionOccured = true;
      // Adjust ball direction based on where it hit the paddle
      let collidePoint = ball.y - (ai.y + ai.height / 2);
      collidePoint = collidePoint / (ai.height / 2); // Normalize to -1 to 1
      ball.dx *= -1;
      ball.dy = collidePoint * INITIAL_BALL_SPEED_Y * 1.2; // Increase vertical speed slightly
      ball.dx *= 1.05; // Increase horizontal speed
    }
  }

  // Scoring
  if (ball.x - ball.radius < 0) { // AI scores
    ai.score++;
    if (gameMode === 'arcade') {
      playerLives--;
      if (playerLives <= 0) {
        gameOver = true;
        checkArcadeHighScore(playerArcadePoints);
      }
    } else if (gameMode === 'quick_match' && ai.score >= QUICK_MATCH_SCORE_LIMIT) {
      gameOver = true;
    }
    resetBall();
  } else if (ball.x + ball.radius > canvas.width) { // Player scores
    player.score++;
    if (gameMode === 'arcade') {
      playerArcadePoints += ARCADE_POINTS_PER_GOAL;
    } else if (gameMode === 'quick_match' && player.score >= QUICK_MATCH_SCORE_LIMIT) {
      gameOver = true;
    }
    resetBall();
  }
  drawScore();
}

function render() {
  // Clear canvas
  drawRect(0, 0, canvas.width, canvas.height, '#222');

  // Draw center line
  for (let i = 0; i < canvas.height; i += 20) {
    drawRect(canvas.width / 2 - 1, i, 2, 10, '#FFF');
  }

  // Draw paddles
  drawRect(player.x, player.y, player.width, player.height, 'white');
  drawRect(ai.x, ai.y, ai.width, ai.height, 'white');

  // Draw ball
  drawCircle(ball.x, ball.y, ball.radius, 'yellow');

  // Game over message
  if (gameOver) {
    ctx.fillStyle = 'red';
    ctx.font = '30px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('¡Juego Terminado!', canvas.width / 2, canvas.height / 2 - 30);

    if (gameMode === 'quick_match') {
      const winner = player.score > ai.score ? 'Jugador' : 'IA';
      ctx.fillText(`Ganador: ${winner}`, canvas.width / 2, canvas.height / 2 + 10);
    } else if (gameMode === 'arcade') {
      ctx.fillText(`Puntuación Final: ${playerArcadePoints}`, canvas.width / 2, canvas.height / 2 + 10);
      ctx.fillText('¡Pulsa R para Reiniciar!', canvas.width / 2, canvas.height / 2 + 50);
    }
  }
}

function gameLoop() {
  update();
  render();
  requestAnimationFrame(gameLoop);
}

// --- High Score Management (Local Storage) ---
function loadHighScores() {
  const scores = JSON.parse(localStorage.getItem(HIGH_SCORES_KEY)) || [];
  return scores;
}

function saveHighScores(scores) {
  localStorage.setItem(HIGH_SCORES_KEY, JSON.stringify(scores));
}

function checkArcadeHighScore(currentScore) {
  let highScores = loadHighScores();
  const minHighScore = highScores.length < 5 ? 0 : highScores[highScores.length - 1].score;

  if (currentScore > minHighScore) {
    let playerName = prompt(`¡Nueva Puntuación Alta (${currentScore})! Introduce tu nombre:`);
    if (playerName) {
      highScores.push({ name: playerName, score: currentScore });
      highScores.sort((a, b) => b.score - a.score);
      highScores = highScores.slice(0, 5); // Keep top 5
      saveHighScores(highScores);
      alert('¡Puntuación guardada!');
      // Optionally, you could try to inform the Streamlit parent frame here,
      // but direct real-time updates are complex with components.html.
      // For now, it's managed locally in the browser.
    } else {
      alert('Puntuación no guardada. Nombre no proporcionado.');
    }
  }
}

// Event Listeners for Player Control
// Mouse movement
canvas.addEventListener('mousemove', e => {
  if (!gameOver) {
    let rect = canvas.getBoundingClientRect();
    player.y = e.clientY - rect.top - player.height / 2;
  }
});

// Keyboard movement
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowUp') {
    player.dy = -PLAYER_PADDLE_SPEED;
  } else if (e.key === 'ArrowDown') {
    player.dy = PLAYER_PADDLE_SPEED;
  } else if (e.key === 'r' || e.key === 'R') { // Restart game
    if (gameOver) {
      // Determine the last played mode to restart in it
      resetGame(gameMode);
    }
  }
});

document.addEventListener('keyup', e => {
  if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
    player.dy = 0;
  }
});

// Initial game setup - default to quick match
resetGame('quick_match');
gameLoop();

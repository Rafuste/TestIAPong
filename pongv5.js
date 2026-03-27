const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const PADDLE_WIDTH = 15;
const PADDLE_HEIGHT = 80;
const BALL_RADIUS = 10;
const PADDLE_SPEED = 6; // Adjusted for smoother AI movement

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
  dx: 5, // Initial speed
  dy: 5
};

function resetBall() {
  ball.x = canvas.width / 2;
  ball.y = canvas.height / 2;
  ball.dx = -ball.dx; // Reverse direction for next serve
  ball.dy = (Math.random() * 10 - 5); // Randomize vertical direction
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
  document.getElementById('player-score').innerText = player.score;
  document.getElementById('ai-score').innerText = ai.score;
}

function update() {
  // Move player paddle (keyboard)
  player.y += player.dy;
  if (player.y < 0) player.y = 0;
  if (player.y + player.height > canvas.height) player.y = canvas.height - player.height;

  // Move AI paddle
  // Simple AI: follow the ball's y position
  if (ai.y + ai.height / 2 < ball.y) {
    ai.y += PADDLE_SPEED;
  } else if (ai.y + ai.height / 2 > ball.y) {
    ai.y -= PADDLE_SPEED;
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
  let playerCollision = ball.x - ball.radius < player.x + player.width &&
                        ball.y > player.y && ball.y < player.y + player.height;
  let aiCollision = ball.x + ball.radius > ai.x &&
                    ball.y > ai.y && ball.y < ai.y + ai.height;

  if (playerCollision) {
    // Adjust ball direction based on where it hit the paddle
    let collidePoint = ball.y - (player.y + player.height / 2);
    collidePoint = collidePoint / (player.height / 2); // Normalize to -1 to 1
    ball.dx *= -1;
    ball.dy = collidePoint * 5; // Give it some vertical speed
  } else if (aiCollision) {
    // Adjust ball direction based on where it hit the paddle
    let collidePoint = ball.y - (ai.y + ai.height / 2);
    collidePoint = collidePoint / (ai.height / 2); // Normalize to -1 to 1
    ball.dx *= -1;
    ball.dy = collidePoint * 5; // Give it some vertical speed
  }

  // Scoring
  if (ball.x - ball.radius < 0) { // AI scores
    ai.score++;
    drawScore();
    resetBall();
  } else if (ball.x + ball.radius > canvas.width) { // Player scores
    player.score++;
    drawScore();
    resetBall();
  }
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
}

function gameLoop() {
  update();
  render();
  requestAnimationFrame(gameLoop);
}

// Event Listeners for Player Control
// Mouse movement
canvas.addEventListener('mousemove', e => {
  let rect = canvas.getBoundingClientRect();
  player.y = e.clientY - rect.top - player.height / 2;
});

// Keyboard movement
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowUp') {
    player.dy = -PADDLE_SPEED;
  } else if (e.key === 'ArrowDown') {
    player.dy = PADDLE_SPEED;
  }
});

document.addEventListener('keyup', e => {
  if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
    player.dy = 0;
  }
});

// Start the game
drawScore();
gameLoop();

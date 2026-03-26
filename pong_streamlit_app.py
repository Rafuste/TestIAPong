
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
import json
import os

# --- Game Constants ---
WIDTH, HEIGHT = 800, 500
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 80
BALL_RADIUS = 10
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
SCORE_LIMIT = 5 # For quick match
LIVES_START = 5 # For arcade mode
HIGH_SCORES_FILE = "pong_highscores.json"

# --- Game Classes ---

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        # Random initial direction
        self.dx = BALL_SPEED_X * (1 if np.random.rand() > 0.5 else -1)
        self.dy = BALL_SPEED_Y * (1 if np.random.rand() > 0.5 else -1)

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def collide_wall(self):
        if self.y - BALL_RADIUS < 0 or self.y + BALL_RADIUS > HEIGHT:
            self.dy *= -1

class Paddle:
    def __init__(self, x, is_ai=False):
        self.x = x
        self.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.is_ai = is_ai

    def move(self, dy):
        self.y += dy
        self.y = max(0, min(self.y, HEIGHT - PADDLE_HEIGHT)) # Keep paddle within bounds

    def move_ai(self, ball_y):
        # Simple AI to follow the ball
        if self.y + PADDLE_HEIGHT / 2 < ball_y:
            self.move(PADDLE_SPEED)
        elif self.y + PADDLE_HEIGHT / 2 > ball_y:
            self.move(-PADDLE_SPEED)

class Game:
    def __init__(self):
        self.player_paddle = Paddle(20) # Left paddle
        self.ai_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, is_ai=True) # Right paddle
        self.ball = Ball()
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.mode = "quick_match" # Can be "quick_match" or "arcade"
        self.player_lives = LIVES_START
        self.player_points = 0 # Points for arcade mode

    def update(self):
        if self.game_over:
            return

        self.ball.move()
        self.ball.collide_wall()
        self.ai_paddle.move_ai(self.ball.y)

        # Ball collision with player paddle
        if (self.ball.x - BALL_RADIUS <= self.player_paddle.x + PADDLE_WIDTH and
            self.player_paddle.y <= self.ball.y <= self.player_paddle.y + PADDLE_HEIGHT):
            self.ball.dx *= -1
            self.ball.x = self.player_paddle.x + PADDLE_WIDTH + BALL_RADIUS # Prevent ball from sticking

        # Ball collision with AI paddle
        if (self.ball.x + BALL_RADIUS >= self.ai_paddle.x and
            self.ai_paddle.y <= self.ball.y <= self.ai_paddle.y + PADDLE_HEIGHT):
            self.ball.dx *= -1
            self.ball.x = self.ai_paddle.x - BALL_RADIUS # Prevent ball from sticking

        # Scoring
        if self.ball.x < 0: # AI scores
            self.ai_score += 1
            if self.mode == "arcade":
                self.player_lives -= 1
                if self.player_lives <= 0:
                    self.game_over = True
            self.ball.reset()
        elif self.ball.x > WIDTH: # Player scores
            self.player_score += 1
            if self.mode == "arcade":
                self.player_points += 100
            self.ball.reset()

        # Check for game over condition
        if self.mode == "quick_match" and (self.player_score >= SCORE_LIMIT or self.ai_score >= SCORE_LIMIT):
            self.game_over = True
        elif self.mode == "arcade" and self.player_lives <= 0:
             self.game_over = True

    def reset_game(self, mode):
        self.player_paddle = Paddle(20)
        self.ai_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, is_ai=True)
        self.ball = Ball()
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.mode = mode
        self.player_lives = LIVES_START
        self.player_points = 0


# --- High Score Management ---
def load_highscores():
    if os.path.exists(HIGH_SCORES_FILE):
        with open(HIGH_SCORES_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return [] # Return empty list if file is corrupted
    return []

def save_highscores(highscores):
    with open(HIGH_SCORES_FILE, 'w') as f:
        json.dump(highscores, f, indent=2)

def add_highscore(name, score, highscores):
    highscores.append({"name": name, "score": score})
    highscores.sort(key=lambda x: x['score'], reverse=True)
    return highscores[:5] # Keep only top 5 entries

# --- Streamlit App ---

st.set_page_config(layout="wide")
st.title("Pong Game (Streamlit Edition)")

# Initialize session state variables
if 'game' not in st.session_state:
    st.session_state.game = Game()
if 'running' not in st.session_state:
    st.session_state.running = False
if 'highscores' not in st.session_state:
    st.session_state.highscores = load_highscores()

# Game Control Panel (Sidebar)
with st.sidebar:
    st.header("Controles del Juego")
    game_mode_selection = st.radio(
        "Selecciona el modo de juego:",
        ("Partido Rápido", "Arcade"),
        key="game_mode_radio"
    )

    if st.button("Iniciar / Reiniciar Juego"): # Start/Reset Button
        st.session_state.game.reset_game("quick_match" if game_mode_selection == "Partido Rápido" else "arcade")
        st.session_state.running = True

    # Player paddle control
    st.subheader("Control del Jugador (Paddle Izquierdo)")
    # Using a slider for Y position (simplest interactive control in Streamlit)
    player_paddle_y_target = st.slider(
        "Posición Vertical del Paddle",
        min_value=0,
        max_value=HEIGHT - PADDLE_HEIGHT,
        value=int(st.session_state.game.player_paddle.y),
        step=PADDLE_SPEED, # Adjust step for smoother movement
        key="player_paddle_slider"
    )
    # Update paddle position based on slider input
    st.session_state.game.player_paddle.y = player_paddle_y_target

    st.markdown("---")
    st.header("Top 5 Puntuaciones (Modo Arcade)")
    if st.session_state.highscores:
        for i, score_entry in enumerate(st.session_state.highscores):
            st.write(f"{i+1}. {score_entry['name']}: {score_entry['score']} puntos")
    else:
        st.write("No hay puntuaciones altas aún.")


# Game Display Area
game_placeholder = st.empty() # Placeholder for the game plot

def draw_game(game_state: Game):
    fig, ax = plt.subplots(figsize=(WIDTH/100, HEIGHT/100), facecolor='#222') # Adjust figsize for game resolution
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.set_aspect('equal') # Maintain aspect ratio
    ax.axis('off') # Hide axes

    # Draw paddles
    ax.add_patch(plt.Rectangle((game_state.player_paddle.x, game_state.player_paddle.y), PADDLE_WIDTH, PADDLE_HEIGHT, color='white'))
    ax.add_patch(plt.Rectangle((game_state.ai_paddle.x, game_state.ai_paddle.y), PADDLE_WIDTH, PADDLE_HEIGHT, color='white'))

    # Draw ball
    ax.add_patch(plt.Circle((game_state.ball.x, game_state.ball.y), BALL_RADIUS, color='yellow'))

    # Draw center line
    ax.plot([WIDTH // 2, WIDTH // 2], [0, HEIGHT], 'w--', linewidth=1)

    # Display scores/lives/points
    if game_state.mode == "quick_match":
        ax.text(WIDTH // 4, HEIGHT - 50, f"{game_state.player_score}", color='white', fontsize=24, ha='center', va='center')
        ax.text(3 * WIDTH // 4, HEIGHT - 50, f"{game_state.ai_score}", color='white', fontsize=24, ha='center', va='center')
    elif game_state.mode == "arcade":
        ax.text(WIDTH // 4, HEIGHT - 50, f"Vidas: {game_state.player_lives}", color='white', fontsize=20, ha='center', va='center')
        ax.text(3 * WIDTH // 4, HEIGHT - 50, f"Puntos: {game_state.player_points}", color='white', fontsize=20, ha='center', va='center')

    # Game over message
    if game_state.game_over:
        if game_state.mode == "quick_match":
            winner = "Jugador" if game_state.player_score > game_state.ai_score else "IA"
            ax.text(WIDTH // 2, HEIGHT // 2, f"¡Juego Terminado! Ganador: {winner}", color='red', fontsize=30, ha='center', va='center')
        elif game_state.mode == "arcade":
            ax.text(WIDTH // 2, HEIGHT // 2 - 30, f"¡Juego Terminado!", color='red', fontsize=30, ha='center', va='center')
            ax.text(WIDTH // 2, HEIGHT // 2 + 10, f"Puntuación Final: {game_state.player_points}", color='red', fontsize=24, ha='center', va='center')
    return fig

# Main game loop simulation in Streamlit
# This loop will run if the game is active.
if st.session_state.running and not st.session_state.game.game_over:
    st.session_state.game.update()
    time.sleep(0.05) # Simulate frame rate (20 FPS)
    st.rerun() # Re-execute the entire script to update the game state and display

# Render the current game state using matplotlib
current_fig = draw_game(st.session_state.game)
game_placeholder.pyplot(current_fig)
plt.close(current_fig) # Close the figure to prevent memory issues

# Handle high score entry after game over in Arcade Mode
if st.session_state.game.game_over and st.session_state.game.mode == "arcade":
    st.subheader("¡Has perdido todas tus vidas!")
    player_name = st.text_input("Introduce tu nombre para guardar tu puntuación:", key="player_name_input_widget")
    if st.button("Guardar Puntuación"): # Button to save score
        if player_name:
            st.session_state.highscores = add_highscore(player_name, st.session_state.game.player_points, st.session_state.highscores)
            save_highscores(st.session_state.highscores)
            st.success(f"Puntuación de {st.session_state.game.player_points} guardada para {player_name}!")
            # Clear input after saving, can cause an issue if player_name_input is not reset
            # A better way might be to disable the input/button or rerun after save.
            st.session_state.game_over = False # Prevent multiple saves after one game
            st.experimental_rerun() # Refresh to show updated highscores and reset game_over state visually
        else:
            st.warning("Por favor, introduce un nombre.")

st.info("Nota: Para mover el paddle del jugador, utiliza el deslizador 'Posición Vertical del Paddle' en la barra lateral.")
st.markdown("---")
st.caption("Desarrollado con Streamlit, Matplotlib y Python.")

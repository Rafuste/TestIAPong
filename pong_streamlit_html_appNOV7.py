import streamlit as st
import streamlit.components.v1 as components
import os
import json

# --- Archivos del juego Pong (HTML, CSS, JS) ---
HTML_FILE = "index.html"
CSS_FILE = "style.css"
JS_FILE = "pong.js"
HIGH_SCORES_FILE = "pong_highscores.json"

def load_file_content(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return None

# --- High Score Management (for display purposes, not dynamic from embedded game) ---
def load_highscores():
    if os.path.exists(HIGH_SCORES_FILE):
        with open(HIGH_SCORES_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return [
        {"name": "Player1", "score": 1500},
        {"name": "Player2", "score": 1200},
        {"name": "Player3", "score": 1000},
        {"name": "Player4", "score": 800},
        {"name": "Player5", "score": 600},
    ] # Dummy data for initial display

# Custom CSS for "PongXtreme" theme
custom_css = """
<style>
    body { /* Streamlit's body */
        background-color: #0d0d1a !important; /* Dark blue/purple */
        color: #e0e0ff !important; /* Light text */
        font-family: 'Consolas', monospace; /* Techy font */
    }
    h1, h2, h3, h4, h5, h6 { /* Streamlit headers */
        color: #00ffcc !important; /* Neon green */
        text-shadow: 0 0 5px #00ffcc; /* Neon glow */
    }
    .stButton>button {
        background-color: #4a00e0; /* Purple button */
        color: white;
        border: 2px solid #00ffcc; /* Neon border */
        box-shadow: 0 0 8px #00ffcc;
    }
    .stRadio>label>div {
        color: #99ccff; /* Light blue for radio options */
    }
    .stInfo {
        background-color: #1a1a33; /* Darker info box */
        border-left: 5px solid #00ffcc;
        color: #e0e0ff;
    }
    /* Adjust main content padding */
    .main .block-container {
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


html_content = load_file_content(HTML_FILE)
css_content = load_file_content(CSS_FILE)
js_content = load_file_content(JS_FILE)

if html_content and css_content and js_content:
    # Integramos el CSS y JS directamente en el HTML para la incrustación
    full_html_game = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Pong Game</title>
      <style>
        body {{ /* Ensure the embedded body doesn't inherit Streamlit's full body style */
            background: #111; 
            color: #fff;
            font-family: Arial, sans-serif;
            margin: 0; /* Remove default body margin */
            padding: 0;
        }}
        #scoreboard {{ /* Ensure scoreboard is visible within embedded HTML */
            font-size: 2em;
            margin-bottom: 10px;
            font-weight: bold;
            text-align: center;
        }}
        canvas {{ /* Ensure canvas styling is maintained */
            background: #222;
            display: block;
            margin: 0 auto;
            border: 2px solid #fff;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
        }}
        {css_content}
      </style>
    </head>
    <body>
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: flex-start; height: 100%;">
          <h1>Pong Game</h1>
          <div id="scoreboard">
            <span id="player-score">0</span> : <span id="ai-score">0</span>
          </div>
          <canvas id="gameCanvas" width="800" height="500"></canvas>
      </div>
      <script>
        {js_content}
      </script>
    </body>
    </html>
    """

    st.set_page_config(layout="wide")
    st.title("PONG XTREME!!!!")

    st.markdown("### ¡Juega al Pong clásico aquí!", unsafe_allow_html=True)
    st.info("Para jugar, haz clic en el área del juego. El paddle izquierdo se controla con el ratón o con las teclas de flecha (arriba/abajo).")

    # Incrustamos el juego HTML/JS con altura ajustada
    # Adjusted height to fit H1, scoreboard, canvas (500px), and some padding/margins
    components.html(full_html_game, height=650, width=850, scrolling=False)

    st.markdown("--- desarrollado con Streamlit y el juego Pong original en HTML/CSS/JS ---")
else:
    st.error("¡Error! No se pudieron cargar uno o más archivos del juego (index.html, style.css, pong.js). Asegúrate de que estén en el mismo directorio.")

# --- Controles y Clasificación en la Barra Lateral ---
with st.sidebar:
    st.header("Controles del Juego")
    game_mode_selection = st.radio(
        "Selecciona el modo de juego (¡Conceptual!):",
        ("Partido Rápido", "Arcade"),
        key="game_mode_radio"
    )
    st.info("Nota: La selección de modo aquí es solo de demostración visual. El juego incrustado no cambia su lógica de forma dinámica sin modificar el archivo pong.js.")

    if st.button("Iniciar / Reiniciar Juego"): # Start/Reset Button (for conceptual reset)
        st.write("Juego reiniciado (conceptualmente).") # Placeholder for actual reset logic if JS communication existed

    st.markdown("---")
    st.header("🏆 Top 5 Puntuaciones (Modo Arcade)")
    highscores = load_highscores()
    if highscores:
        for i, score_entry in enumerate(highscores):
            st.write(f"{i+1}. {score_entry['name']}: {score_entry['score']} puntos")
    else:
        st.write("No hay puntuaciones altas aún (ejemplo).")
    st.info("Estas puntuaciones son de ejemplo. El juego incrustado no las actualiza directamente sin comunicación avanzada.")


import streamlit as st
import streamlit.components.v1 as components
import os
import json

# --- Archivos del juego Pong (HTML, CSS, JS) ---
HTML_FILE = "index.html"
CSS_FILE = "style.css"
JS_FILE = "pong.js"
HIGH_SCORES_FILE = "pong_highscores.json" # This file is for Python-side highscores, not directly from JS local storage

def load_file_content(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return None

# --- High Score Management (for display purposes on Streamlit sidebar) ---
def load_highscores_from_file():
    if os.path.exists(HIGH_SCORES_FILE):
        with open(HIGH_SCORES_FILE, 'r') as f:
            try:
                scores = json.load(f)
                # Ensure scores is a list and contains dictionaries with 'name' and 'score'
                if isinstance(scores, list) and all(isinstance(s, dict) and 'name' in s and 'score' in s for s in scores):
                    return scores
            except json.JSONDecodeError:
                pass # Fall through to return empty list if file is corrupted
    return [] # Return empty list by default


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


highscores = load_highscores_from_file()

html_raw = load_file_content(HTML_FILE)
css_raw = load_file_content(CSS_FILE)
js_raw = load_file_content(JS_FILE)

# Initialize session state for game key counter if not present
if 'game_key_counter' not in st.session_state:
    st.session_state.game_key_counter = 0


if html_raw and css_raw and js_raw:
    # Game Control Panel (Sidebar) - Needs to be defined before components.html to get the mode
    with st.sidebar:
        st.header("Controles del Juego")
        game_mode_selection_py = st.radio(
            "Selecciona el modo de juego:",
            ("Partido Rápido", "Arcade"),
            key="game_mode_radio_html"
        )

        # Map Streamlit radio selection to JS game mode string
        js_game_mode = "quick_match" if game_mode_selection_py == "Partido Rápido" else "arcade"

        if st.button("Iniciar / Reiniciar Juego"):
            # Increment the counter to force re-render of the components.html with a new key
            st.session_state.game_key_counter += 1
            # No st.experimental_rerun() needed here, changing the key will cause a redraw

        st.markdown("---")
        st.header("🏆 Top 5 Puntuaciones (Modo Arcade)")
        
        if highscores:
            for i, score_entry in enumerate(highscores):
                st.write(f"{i+1}. {score_entry['name']}: {score_entry['score']} puntos")
        else:
            st.write("No hay puntuaciones altas en el servidor. Las puntuaciones del juego se guardan en el `localStorage` de tu navegador.")
        st.info("Nota: Las puntuaciones altas que ves aquí son gestionadas por el servidor de Streamlit (vacías por defecto). El juego incrustado gestiona sus propias puntuaciones en el `localStorage` de tu navegador. Para ver tus puntuaciones del juego, deberás jugar y el juego te las mostrará al finalizar una partida Arcade.")

    # Modify js_content to inject the selected mode
    js_content_modified = js_raw.replace("resetGame('quick_match');", f"resetGame('{js_game_mode}');")

    # Replace <link> and <script> tags in the raw HTML content
    # Use str.format() to avoid issues with f-string parsing of curly braces in CSS/JS content
    full_html_game = html_raw.replace(
        '<link rel="stylesheet" href="style.css">',
        '<style>{}</style>'.format(css_raw)
    )

    full_html_game = full_html_game.replace(
        '<script src="pong.js"></script>',
        '<script>{}</script>'.format(js_content_modified)
    )

    st.set_page_config(layout="wide")
    st.title("PONG XTREME!!!!")

    st.markdown("### ¡Juega al Pong clásico aquí!", unsafe_allow_html=True)
    st.info("Para jugar, haz clic en el área del juego. El paddle izquierdo se controla con el ratón o con las teclas de flecha (arriba/abajo).")

    # Incrustamos el juego HTML/JS con altura ajustada, using a dynamic key
    components.html(full_html_game, height=650, width=850, scrolling=False, key=f"pong_game_{st.session_state.game_key_counter}")

    st.markdown("---", unsafe_allow_html=True)
    st.markdown("Desarrollado con Streamlit y el juego Pong original en HTML/CSS/JS")
else:
    st.error("¡Error! No se pudieron cargar uno o más archivos del juego (index.html, style.css, pong.js). Asegúrate de que estén en el mismo directorio.")


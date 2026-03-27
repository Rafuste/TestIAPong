import streamlit as st
import streamlit.components.v1 as components
import os

# --- Archivos del juego Pong (HTML, CSS, JS) ---
# Asume que estos archivos están en el mismo directorio que tu script Streamlit
HTML_FILE = "index.html"
CSS_FILE = "style.css"
JS_FILE = "pong.js"

def load_file_content(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return None

html_content = load_file_content(HTML_FILE)
css_content = load_file_content(CSS_FILE)
js_content = load_file_content(JS_FILE)

if html_content and css_content and js_content:
    # Integramos el CSS y JS directamente en el HTML para la incrustación
    # Esto simplifica la gestión de rutas de archivos dentro del componente HTML
    full_html_game = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Pong Game</title>
      <style>
        {css_content}
      </style>
    </head>
    <body>
      {html_content.split('<body>')[1].split('</body>')[0]} <!-- Solo el contenido del body -->
      <script>
        {js_content}
      </script>
    </body>
    </html>
    """

    st.set_page_config(layout="wide")
    st.title("Pong Game (Streamlit Edition with HTML/JS Embed)")

    st.markdown("### ¡Juega al Pong clásico aquí!", unsafe_allow_html=True)
    st.info("Para jugar, haz clic en el área del juego. El paddle izquierdo se controla con el ratón o con las teclas de flecha (arriba/abajo).")

    # Incrustamos el juego HTML/JS
    components.html(full_html_game, height=550, width=850, scrolling=False)

    st.markdown("--- desarrollado con Streamlit y el juego Pong original en HTML/CSS/JS ---")
else:
    st.error("¡Error! No se pudieron cargar uno o más archivos del juego (index.html, style.css, pong.js). Asegúrate de que estén en el mismo directorio.")

# --- Instrucciones adicionales para el usuario ---
st.sidebar.header("Instrucciones")
st.sidebar.markdown(
    """
1. Asegúrate de que `index.html`, `style.css` y `pong.js` (los archivos que generamos antes) estén en el mismo directorio que este script.
2. Guarda este script como `pong_streamlit_html_app.py`.
3. Ejecuta `streamlit run pong_streamlit_html_app.py` en tu terminal.
4. Despliega en Streamlit Cloud con estos 4 archivos: `pong_streamlit_html_app.py`, `index.html`, `style.css`, `pong.js` y `requirements.txt`.
    """
)


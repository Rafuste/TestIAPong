import streamlit as st

# Setting up the game variables
score = {'Player1': 0, 'Player2': 0}
high_scores = {'Quick Play': 0, 'Arcade': 0}

# Function to update high scores
def update_high_score(mode):
    if score['Player1'] > high_scores[mode]:
        high_scores[mode] = score['Player1']
    if score['Player2'] > high_scores[mode]:
        high_scores[mode] = score['Player2']

# Quick Play Game
def quick_play():
    st.title('Quick Play Mode')
    # Game logic here
    st.write(f'Score - Player1: {score['Player1']}, Player2: {score['Player2']}')

# Arcade Mode
def arcade():
    st.title('Arcade Mode')
    # Game logic here
    st.write(f'Score - Player1: {score['Player1']}, Player2: {score['Player2']}')

# Main Game Function
if __name__ == '__main__':
    mode = st.sidebar.selectbox('Choose your mode:', ['Quick Play', 'Arcade'])
    if mode == 'Quick Play':
        quick_play()
    elif mode == 'Arcade':
        arcade()

st.sidebar.subheader('High Scores')
st.sidebar.write(high_scores)
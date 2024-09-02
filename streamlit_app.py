import streamlit as st
from streamlit import session_state as ss # Shortcut for session_state
import glob
import time

from helpers.song_panel import update as update_song_panel
from helpers.chords_panel import update as update_chords_panel

if 'sidebar_state' not in st.session_state:
    ss.sidebar_state = 'expanded'

st.set_page_config(layout="wide", 
                    page_title="StrumLit",
                    initial_sidebar_state=ss.sidebar_state
                    )

def collapse_sidebar():
    ss.sidebar_state = 'collapsed'

def expand_sidebar():
    ss.sidebar_state = 'expanded'

# Get the list of all the songs
song_files = sorted(glob.glob("songs/*.md"))

# Columns
c1, c2, c3 = st.columns([4,1,1])
# Create a dropdown to select the song
st.sidebar.header("StrumLit")
song = st.sidebar.selectbox("Select a song", song_files)

# Read the song file
with open(song, "r") as file:
    song_data = file.readlines()
# Read the properties
pattern = song_data[1].split(" = ")[1].strip().replace('"','').replace("'", "")
default_beats = int(song_data[2].split(" = ")[1].strip())
default_seconds = float(song_data[3].split(" = ")[1].strip())
song_chords_data = song_data[5:]

time_per_line = st.sidebar.number_input("Time per line [seconds]", 
                                min_value=0.0, max_value=10.0, 
                                value=default_seconds, step=0.1
                                )
n_beats = st.sidebar.number_input("Beats per second", 
                                min_value=0, max_value=10, 
                                value=default_beats, step=1
                                )
beep_sound = st.sidebar.checkbox("Beep sound", value=False)
sc1, sc2 = st.sidebar.columns(2)
start_song = sc1.button("Start song", on_click=collapse_sidebar)
stop_song = sc2.button("Stop song", on_click=expand_sidebar)

beep_duration = 0.1 # seconds
pause_duration = time_per_line/n_beats - beep_duration

song_title = song.split("/")[-1].split(".")[0]
song_title = song_title.replace("_", " ").replace("-", " ").title()
st.title(song_title)

body_ph = st.empty()
body_ph.markdown("  \n".join(song_chords_data))

# Update the song chords data so user has seconds to prepare
song_chords_data = ["3... 2... 1"] + song_chords_data

if start_song:
    # Initialize the panes
    left_pane, right_pane = body_ph.columns([5,2])
    # Initialize the panes
    prev_ph = left_pane.empty()
    curr_ph = left_pane.empty()
    next_ph = left_pane.empty()

    right_pane.markdown(f"## Pattern: **{pattern}**")
    chords_ph = right_pane.empty()
    # Collapse the sidebar
    for i in range(len(song_chords_data)):
        if not stop_song:
            # Update the left pane
            current_line = update_song_panel(i, song_chords_data, prev_ph, curr_ph, next_ph)
            # Update the right pane
            update_chords_panel(current_line, chords_ph)
            # Wait to update again
            for _ in range(n_beats):
                time.sleep(pause_duration)
                if beep_sound:
                    print('\a')

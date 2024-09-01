import streamlit as st
from streamlit import session_state as ss # Shortcut for session_state
import glob
import time

from helpers.song_panel import update as update_song_panel
from helpers.chords_panel import update as update_chords_panel

if 'sidebar_state' not in st.session_state:
    ss.sidebar_state = 'expanded'

st.set_page_config(layout="wide", initial_sidebar_state=ss.sidebar_state)

def collapse_sidebar():
    ss.sidebar_state = 'collapsed'

def expand_sidebar():
    ss.sidebar_state = 'expanded'

# Get the list of all the songs
song_files = sorted(glob.glob("songs/*.md"))

# Columns
c1, c2, c3 = st.columns([4,1,1])
# Create a dropdown to select the song
song = st.sidebar.selectbox("Select a song", song_files)
time_per_line = st.sidebar.number_input("Time per line [seconds]", 
                                min_value=0.0, max_value=10.0, value=4.0, step=0.1
                                )
n_beats = st.sidebar.number_input("Beats per second", 
                                min_value=0, max_value=10, value=4, step=1
                                )
beep_sound = st.sidebar.checkbox("Beep sound", value=True)
sc1, sc2 = st.sidebar.columns(2)
start_song = sc1.button("Start song", on_click=collapse_sidebar)
stop_song = sc2.button("Stop song", on_click=expand_sidebar)

# Read the song file
with open(song, "r") as file:
    song_data = file.readlines()

n_beats = 4
beep_duration = 0.1 # seconds
pause_duration = time_per_line/n_beats - beep_duration

left_pane, right_pane = st.columns([5,2])

left_pane.markdown("# ukemaSTer")

prev_ph = left_pane.empty()
curr_ph = left_pane.empty()
next_ph = left_pane.empty()

counter_ph = right_pane.empty()
chords_ph = right_pane.empty()

if start_song:
    # Collapse the sidebar
    for i in range(len(song_data)):
        if not stop_song:
            # Update the left pane
            current_line = update_song_panel(i, song_data, prev_ph, curr_ph, next_ph)
            # Update the right pane
            update_chords_panel(current_line, chords_ph)
            # Wait to update again
            if i == 0:
                counter_ph.markdown("## 3")
                time.sleep(1)
                counter_ph.markdown("## 2")
                time.sleep(1)
                counter_ph.markdown("## 1")
                time.sleep(1)
                counter_ph.empty()
            

            for _ in range(n_beats):
                time.sleep(pause_duration)
                if beep_sound:
                    print('\a')

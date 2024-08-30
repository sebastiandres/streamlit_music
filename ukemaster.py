import streamlit as st
import glob
import time

from song_panel import update as update_song_panel
from chords_panel import update as update_chords_panel
# Configure to use wide mode
st.set_page_config(layout="wide")

st.title("UkeMaster")

# Get the list of all the songs
song_files = glob.glob("songs/*.md")

# Create a dropdown to select the song
song = st.selectbox("Select a song", song_files)

# Read the song file
with open(song, "r") as file:
    song_data = file.readlines()

# Add an empty line, if not already present
time_per_line = st.number_input("Time per line [seconds]", 
                                min_value=0.0, max_value=10.0, value=4.0, step=0.1
                                )
c1, c2 = st.columns(2)
start_song = c1.button("Start song")
stop_song = c2.button("Stop song")

# Display the song data
# Considerations:
# Should show 3 lines: previous, current and next.
# Each line should be present for time_per_line seconds.
# The song should loop.

left_pane, right_pane = st.columns(2)

prev_ph = left_pane.empty()
curr_ph = left_pane.empty()
next_ph = left_pane.empty()

chords_ph = right_pane.empty()

if start_song:
    for i in range(len(song_data)):
        if not stop_song:
            # Update the left pane
            current_line = update_song_panel(i, song_data, prev_ph, curr_ph, next_ph)
            # Update the right pane
            update_chords_panel(current_line, chords_ph)
            # Wait to update again
            time.sleep(time_per_line)

import streamlit as st

def update(i, song_data, prev_ph, curr_ph, next_ph):
    # Get the previous line
    if i-1 >= 0:
        prev_text = str(i-1) + ": " + song_data[i-1]
    else:
        prev_text = str(i-1) + ": "
    # Get the current line
    curr_text = str(i) + ": " + song_data[i]
    # Get the next line
    if i+1 < len(song_data):
        next_text = str(i+1) + ": " + song_data[i+1]
    else:
        next_text = str(i+1) + ": "
    # Write the text to the previous, current and next placeholders
    prev_ph.write(prev_text)
    curr_ph.write("**"+curr_text.strip()+"**")
    next_ph.write(next_text)
    return curr_text
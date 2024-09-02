import re
from os.path import join, exists
import streamlit as st

def get_image_for_chord(chord):
    """
    chord is a string with the chord.
    We need to get the image of the chord from the chords dictionary.
    """
    # We see if the file is an image previously created
    image_filepath = join("chord_images", f"{chord}.png")
    if chord!="null" and not exists(image_filepath):
        # Return the image to the unknown chord
        image_filepath = join("chord_images", "?.png")
    return image_filepath


def update(current_line, chords_ph):
    """
    current line is a string with the lyrics and chords.
    The chords are in the format [Chord] as [G], [Gm], etc
    We need to display the chords in a graphical way.
    """
    # Get a list of current chords using regex from the current line
    # options: [*]
    current_chords_regex = r"\[(.*?)\]"
    current_chords = re.findall(current_chords_regex, current_line)
    print(current_chords)
    # Show the chords in panels
    N_PANELS = 2
    chords_ph.empty()
    with chords_ph.container():
        panel_columns_1 = st.columns(N_PANELS)
        panel_columns_2 = st.columns(N_PANELS)
        panel_columns = [panel_columns_1, panel_columns_2]
        # Show the new chords
        for k in range(2*N_PANELS):
            i, j = divmod(k, N_PANELS)
            if k < len(current_chords):
                chord = current_chords[k]
                image_filepath = get_image_for_chord(chord)
            else:
                image_filepath = get_image_for_chord("null")
            panel_columns[i][j].image(image_filepath)
    return

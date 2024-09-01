import beepy
import re
from os.path import join, exists


def get_image_for_chord(chord):
    """
    chord is a string with the chord.
    We need to get the image of the chord from the chords dictionary.
    """
    # We see if the file is an image previously created
    image_filepath = join("chord_images", f"{chord}.png")
    if not exists(image_filepath):
        # Return the image to the unknown chord
        image_filepath = join("chord_images", f"{chord}.png")
    return image_filepath


def update(current_line, chords_ph):
    """
    current line is a string with the lyrics and chords.
    The chords are in the format [Chord] as [G], [Gm], etc
    We need to display the chords in a graphical way.
    """
    # Get a list of current chords using regex from the current line
    current_chords_regex = r"\[([A-G]+(?:m|#|7|maj7)?)[\s\S]*?\]"
    current_chords = re.findall(current_chords_regex, current_line)
    # Show the chords in a 5 columns table, if needed
    N_PANELS = 2
    panel_columns_1 = chords_ph.columns(N_PANELS)
    panel_columns_2 = chords_ph.columns(N_PANELS)
    panel_columns = [panel_columns_1, panel_columns_2]
    # Clean the panels from previous chords
    for k in range(2*N_PANELS):
        i, j = divmod(k, N_PANELS)
        panel_columns[i][j].empty()
    # Show the new chords
    for k, chord in enumerate(current_chords):
        i, j = divmod(k, N_PANELS)
        image_filepath = get_image_for_chord(chord)
        panel_columns[i][j].image(image_filepath)
    return

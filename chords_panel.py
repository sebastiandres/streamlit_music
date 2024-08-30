import re
from chords import ukelele

def get_table_chords_from_str(chords_str):
    """
    chords_str is a string with the chords.
    Example: 3000
    Should return:
    [
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "o", "", ""],
    ]
    """
    chords_table = [["" for _ in range(5)] for _ in range(4)]
    for i in range(4):
        if chords_str[i] != "0":
            chords_table[i][int(chords_str[i])-1] = "o"
    return chords_table

def update(current_line, chords_ph):
    """
    current line is a string with the lyrics and chords.
    The chords are in the format [Chord] as [G], [Gm], etc
    We need to display the chords in a graphical way.
    """
    # Get a list of current chords using regex from the current line
    current_chords_regex = r"\[([A-G]+[m#]?)[\s\S]*?\]"
    current_chords = re.findall(current_chords_regex, current_line)
    # Get the chords from the chords dictionary into a dictionary
    current_chords_dict = {chord: ukelele.chords[chord] for chord in current_chords}
    # Show the chords in a 5 columns table, if needed
    panel_columns = chords_ph.columns(3)
    for i, (chord, value) in enumerate(current_chords_dict.items()):
        chords_table = get_table_chords_from_str(value)
        panel_columns[i].write("### " + chord)
        panel_columns[i].dataframe(chords_table)
    return

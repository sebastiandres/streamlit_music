"""
This file creates memory notes to learn the pentagram 
and their relationship to the notes on the guitar.

It defines a simple structure to store the notes and their properties.
It uses matplotlib to create a visual representation of the notes and their relationships.
"""
from math import ceil, floor
import warnings
import os

warnings.filterwarnings("ignore")
HEIGHT = 6
WIDTH = 6
DPI = 300

########################################################
# The data
########################################################
notes = [
            # (Pentagram position, 
            # Note name in Spanish, 
            # Note letter in International Standard & Octave, 
            # Guitar string & fret)
            (-2.5, "Mi", "E6", (6,0)),
            (-2.0, "Fa", "F6", (6,1)),
            (-1.5, "Sol", "G6", (6,3)),
            (-1.0, "La", "A6", (5,0)),
            (-0.5, "Si", "B6", (5,2)),
            (0.0, "Do", "C5", (5,3)),
            (0.5, "Re", "D5", (4,0)),
            (1.0, "Mi", "E5", (4,2)),
            (1.5, "Fa", "F5", (4,3)),
            (2.0, "Sol", "G5", (3,0)),
            (2.5, "La", "A5", (3,2)),
            (3.0, "Si", "B5", (2,0)),
            (3.5, "Do", "C4", (2,1)),
            (4.0, "Re", "D4", (2,3)),
            (4.5, "Mi", "E4", (1,0)),
            (5.0, "Fa", "F4", (1,1)),
            (5.5, "Sol", "G4", (1,3)),
            (6.0, "La", "A4", (1,5)),
            (6.5, "Si", "B4", (1,7)),
            (7.0, "Do", "C3", (1,8)),
            (7.5, "Re", "D3", (1,10)),
]

########################################################
# Making pretty plots
########################################################
import matplotlib.pyplot as plt

def plot_note(note, ax=None, path=None, prefix=""):
    # Create a figure and axis
    if ax is None:
        fig, ax = plt.subplots(figsize=(WIDTH, HEIGHT))
    ax.set_xlim(-1, 13)
    ax.set_ylim(-4, 9)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

    # Draw the pentagram
    ax.plot([1,1], [1,5], color='lightgrey')
    ax.plot([5,5], [1,5], color='lightgrey')
    for i in range(1,6):
        ax.plot([1, 5], [i, i], color='black', linewidth=2)

    # Draw the lines of the note
    pos, name, letter, (string, fret) = note
    if pos<=0:
        lowest_bar = ceil(pos)
        highest_bar = 0
    elif pos>=6:
        lowest_bar = 6
        highest_bar = floor(pos)
    else:
        lowest_bar = None
        highest_bar = None
    if lowest_bar is not None and highest_bar is not None:
        for i in range(lowest_bar, highest_bar+1):
            ax.plot([2, 4], [i, i], color='grey', linewidth=2)

    # Plot the note: a white circle with black border on the (3, position)
    ax.plot(3, pos, marker='o', markerfacecolor='white', markeredgecolor='blue', markersize=16, markeredgewidth=2)

    # Draw the name, letter and (string, fret)
    x_text = 11
    ax.text(x_text, 4, name, ha='left', va='center', fontsize=20, color='lightgrey')
    ax.text(x_text, 2, letter, ha='left', va='center', fontsize=16, color='lightgrey')
    ax.text(x_text, 0, f"{string} - {fret}", ha='left', va='center', fontsize=16, color='lightgrey')

    # Draw a folding line
    ax.plot([x_text-1, x_text-1], [-12, 12], color='lightgrey', linewidth=0.5, linestyle='--')

    # Save the plot
    if path is not None:
        filepath = os.path.join(path, f"{prefix}{letter}-{name}.png")
    else:
        filepath = f"{letter}-{name}.png"
    # Save the plot, with tight layout and minimum bounding box
    if ax is None:
        plt.savefig(filepath, dpi=DPI, bbox_inches='tight', pad_inches=0.03)
        plt.close()
    return

N_NOTES = len(notes)//3
"""
for i, note in enumerate(notes):
    print(note)
    plot_note(note, path="notes", prefix=f"{i:02d}_")
"""
for i in range(N_NOTES):
    print(i)
    # Create a new figure
    fig, axes = plt.subplots(1, 3, figsize=(3*WIDTH, HEIGHT))
    plt.subplots_adjust(wspace=0.0)
    # Plot the note
    plot_note(notes[3*i+0], ax=axes[0])
    plot_note(notes[3*i+1], ax=axes[1])
    plot_note(notes[3*i+2], ax=axes[2])
    # Save the plot
    plt.savefig(f"notes_3x1/note_{i:02d}.png", dpi=DPI, bbox_inches='tight', pad_inches=0.03)
    plt.close()
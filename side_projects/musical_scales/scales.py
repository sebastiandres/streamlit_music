"""
This script uses matplotlib to create images of:
- 12 Notes in a scale
- Mayor scale
- Minor scale
"""

import matplotlib.pyplot as plt
import numpy as np
import warnings

warnings.filterwarnings("ignore")

def plot_circular_text(text, rotation=False,
                        R=7.5, center=(0, 0),
                        color="black", fontsize=18, fontweight="bold", 
                        figtitle="", ax=None, fixed_lines=[]):
    # If no ax is provided, create a new figure
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
    x0, y0 = center
    # Define the notes in a scale
    position_angles = - np.pi -np.linspace(0, 2 * np.pi, len(text)+1)
    if rotation:
        rotation_angles = position_angles - np.pi/2
    else:
        rotation_angles = 0*position_angles
    # Plot the notes
    delta = 5*np.pi/180
    for i, (angle, t) in enumerate(zip(position_angles, text)):
        print("rotation", i, rotation, angle, rotation_angles[i])
        # Plot guidelines
        ax.plot([x0, x0 + R*np.cos(angle+3*delta)], [y0, y0 + R*np.sin(angle+3*delta)], color="lightgray", linewidth=2)
        # Plot the note
        x = x0 + 0.85*R*np.cos(angle)
        y = y0 + 0.85*R*np.sin(angle)
        ax.text(x, y, t, color=color, 
                ha='center', va='center', 
                fontsize = fontsize, fontweight = fontweight, 
                rotation=rotation_angles[i]*180/np.pi)

    # Plot a circle
    circle_angles = np.linspace(0, 2 * np.pi, 121)
    ax.plot(x0 + 0.95*R*np.cos(circle_angles), y0 + 0.95*R*np.sin(circle_angles), color=color, linewidth=3) 
    # Reference circle to cut
    ax.plot(x0 + R*np.cos(circle_angles), y0 + R*np.sin(circle_angles), color="lightgray", linewidth=1) 

    # if fixed_lines is provided, plot the lines
    for R_aux in fixed_lines:
        ax.plot(x0 + R_aux*np.cos(circle_angles), y0 + R_aux*np.sin(circle_angles), color="lightgray", linewidth=1, alpha=0.5)

    if figtitle:
        ax.text(x0 + 0.75*R, y0, figtitle, color=color,
                ha='center', va='center', 
                fontsize = fontsize, fontweight = fontweight, 
                rotation=-90, alpha=0.5)
    #plt.savefig(figname, dpi=300)
    return

# Notes and scales
notes_int   = [ "A",  "", "B",  "C",  "", "D",  "", "E",  "F",  "", "G",   ""]
notes_str   = [ "La", "", "Si", "Do", "", "Re", "", "Mi", "Fa", "", "Sol", ""]
notes_sharp   = [ "La", "La #", "Si", "Do", "Do #", "Re", "Re #", "Mi", "Fa", "Fa #",  "Sol", "Sol #"]
notes_flat    = [ "La", "Si b", "Si", "Do", "Re b", "Re", "Mi b", "Mi", "Fa", "Sol b", "Sol", "La b"]
major_scale = ["VI",   "",  "VII", "I",   "\nESCALA\nMAYOR", "II",   "", "III", "IV",   "", "V",   ""]
minor_scale = ["i",    "\nescala\nmenor",  "ii",  "iii", "", "iv",   "", "v",   "vi",   "", "vii", ""]

# Get one fig, 3 axes
fig, ax = plt.subplots(figsize=(21, 27)) # size of regular letter paper
ax.set_aspect('equal')
ax.set_xlim(0, 21)
ax.set_ylim(0, 27)
ax.set_xticks([])
ax.set_yticks([])
ax.axis('off')

WMAX = 21
HMAX = 27
R1 = 7.9
R2 = 0.8*R1
R3 = 0.5*R1

# Plots
fixed_lines = [0.8*R2, 0.625*R2, 0.8*R3, 0.5*R3]
# Fig 1: All the notes in the same circle
plot_circular_text(notes_str,  R=R1, color="black", fontsize=24, fontweight="bold", ax=ax, center=(R1, R1), fixed_lines=fixed_lines)
# Fig 2 : Minor scale (in green) - inside circle
plot_circular_text(minor_scale, rotation=True, R=R3, color="green", fontsize=18, fontweight="bold", figtitle="", ax=ax, center=(WMAX-R2, HMAX-R2))
# Fig 3 : Major scale (in blue) - outside circle
plot_circular_text(major_scale, rotation=True, R=R2, color="blue",  fontsize=18, fontweight="bold", figtitle="", ax=ax, center=(WMAX-R2, HMAX-R2), fixed_lines=fixed_lines)

# Add the notes in international notation
position_angles = -np.pi - np.linspace(0, 2*np.pi, len(notes_int)+1)
delta = 5*np.pi/180
x0, y0 = R1, R1
for i, angle in enumerate(position_angles[:-1]):
    x = x0 + 0.78*R1*np.cos(angle)
    y = y0 + 0.78*R1*np.sin(angle)
    ax.text(x, y, notes_int[i], color="grey", 
            ha='center', va='center', 
            fontsize = 18, fontweight = "bold", 
            )#rotation=np.pi/2+angle*180/np.pi)
    # Plot the sharp note
    x = x0 + 0.725*R2*np.cos(angle)
    y = y0 + 0.725*R2*np.sin(angle)
    ax.text(x, y, notes_flat[i], color="blue", 
            ha='center', va='center', 
            fontsize = 18, fontweight = "bold", 
            )#rotation=np.pi/2+angle*180/np.pi)
    # Plot the flat note
    x = x0 + 0.65*R3*np.cos(angle)
    y = y0 + 0.65*R3*np.sin(angle)
    ax.text(x, y, notes_sharp[i], color="green", 
            ha='center', va='center', 
            fontsize = 18, fontweight = "bold"
            )#rotation=np.pi/2+angle*180/np.pi)
# Save the figure
figname = "model.png"
fig.savefig(figname, dpi=300, bbox_inches='tight')
print(f"open {figname}")
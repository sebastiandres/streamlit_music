import matplotlib.pyplot as plt
import numpy as np
from os.path import join

# 4 strings, each with a width of 3
N_W, W = 4, 1.0
# 5 frets, each with a length of 5
N_L, L = 5, 1.2
#global N_W, W, N_L, L

def i2x(i):
    return i*W

def j2y(j):
    return (N_L-j)*L

def create_chord_diagram(chord_name, fret_positions, 
                        debug=False, savefig=False, show_fig=False):
    # Dynamically calculate the size of the image
    fig, ax =  plt.subplots(figsize=((N_W-1) * W, N_L * L))

    # Draw the horizontal lines
    for j in range(N_L+1):
        linewidth = 6 if j == 0 else 2
        ax.plot([i2x(0), i2x(N_W-1)], 
                [j2y(j), j2y(j)], 
                'k-', linewidth=linewidth)
    # Draw the vertical lines
    for i in range(0, N_W):
        linewidth = 1
        ax.plot([i2x(i), i2x(i)], 
                [j2y(0), j2y(N_L)], 
                'k-', linewidth=linewidth)

    # print (i,j) for each intersection
    if debug:
        for i in range(N_W+1):
            for j in range(N_L):
                print(i,j, i2x(i), j2y(j))
                ax.text(i2x(i), j2y(j), f'{i},{j}', color='r', fontsize=10, ha='center', va='center')

    # Draw the finger positions
    marker_size = 20
    for i, j in enumerate(fret_positions):
        x = i2x(i)
        if j == 0:
            y = j2y(j)
            #ax.plot(x, y, 'o', color='black', markersize=marker_size, markerfacecolor='white')
        else:
            y = j2y(j - 0.5)
            ax.plot(x, y, 'o', color='black', markersize=marker_size, markerfacecolor='black')

    # Set up the plot
    x_lims = [ i2x(-0.5), i2x(N_W-.5)]
    ax.set_xlim( min(x_lims), max(x_lims))
    y_lims = [j2y(-0.5), j2y(N_L+.5)]
    ax.set_ylim( min(y_lims), max(y_lims))
    ax.set_xticks([])
    ax.set_yticks([])
    plt.axis('off')
    ax.set_title(f'{chord_name}', fontsize=16)
    plt.tight_layout()
    if savefig:
        image_filepath = join("chord_images", f"{chord_name}.png")
        plt.savefig(image_filepath, bbox_inches='tight', pad_inches=0, transparent=True)
    if show_fig:
        plt.show()
    plt.close()
    return fig

if __name__ == '__main__':
    chords = {
        "C": [0,0,0,3],
        "D": [1,1,1,0],
        "Dm": [2,2,1,0],
        "F": [2,0,1,0],
        "G": [0,2,3,2],
        "Em": [0,4,3,2],
        "Am": [2,0,0,0],
        "E7": [1,2,0,2],
    }
    #create_chord_diagram("G", chords["G"], savefig=True, show_fig=True)
    for chord, positions in chords.items():
        create_chord_diagram(chord, positions, savefig=True)
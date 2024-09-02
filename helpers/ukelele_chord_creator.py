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
        plt.savefig(image_filepath, bbox_inches='tight', pad_inches=0, transparent=False)
    if show_fig:
        plt.show()
    plt.close()
    return fig

if __name__ == '__main__':
    chords = {
        # C
        "C": [0,0,0,3],
        "C7": [0,0,0,1],
        "Cm": [0,3,3,3],
        "Cm7": [3,3,3,3],
        "Cdim": [2.3,2,3],
        "Cmaj7": [0,0,0,2],
        "Caug": [1,0,0,4],
        "C6": [0,0,0,0],
        "Cmaj7": [0,0,0,2],
        "C9": [0,2,0,1],
        # D
        "Db": [1,1,1,4],
        "Db7": [1,1,1,2],
        "Dbm": [2,2,0,4],
        "Dbdim": [0,1,0,1],
        "Dbaug": [2,1,1,0],
        "Db6": [1,1,1,1],
        "Dbmaj7": [1,1,1,3],
        "Db9": [1,3,1,2],
        "D": [2,2,2,5],
        "D7": [2,2,2,3],
        "Dm": [2,2,1,0],
        "Dm7": [2,2,1,3],
        "Dmin": [1,2,1,2],
        "Daug": [3,2,2,1],
        "D6": [2,2,2,2],
        "Dmaj7": [2,2,2,4],
        "D9": [2,4,2,3],
        # E
        "E": [0,0,0,2],
        "E7": [1,2,0,2],
        "Em": [0,4,3,2],
        "Em7": [0,2,0,2],
        "Emaj7": [1,3,0,2],
        "E9": [1,2,2,2],
        # F
        "F": [2,0,1,0],
        "F7": [2,3,1,0],
        "Fm": [1,0,1,3],
        "Fm7": [1,3,1,3],
        "Fmaj7": [2,4,1,3],
        "F9": [2,3,3,3],
        # G
        "G": [0,2,3,2],
        "G7": [0,2,1,2],
        "Gm": [0,2,3,1],
        "Gm7": [0,2,1,1],
        "Gmaj7": [0,2,2,2],
        # A
        "A": [2,1,0,0],
        "A7": [0,1,0,0],
        "Am": [2,0,0,0],
        "A6": [2,4,2,4],
        "Amah7": [1,1,0,0],
        # B
        "B": [4,3,2,2],
        "B7": [2,3,2,2],
        "Bm": [2,4,2,2],
        "Bm7": [2,4,2,2],
        "Bdim": [1,2,1,2],
        "Baug": [4,3,3,2],
        "B6": [1,3,2,2],
        "Bmaj7": [3,3,2,2],
        "B9": [2,3,2,4],
    }
    #create_chord_diagram("G", chords["G"], savefig=True, show_fig=True)
    for chord, positions in chords.items():
        create_chord_diagram(chord, positions, savefig=True)
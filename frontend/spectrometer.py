import streamlit as st
from streamlit import session_state as ss # Shortcut for session_state

# From: https://stackoverflow.com/questions/54612204/trying-to-get-the-frequencies-of-a-wav-file-in-python
from scipy.fft import *
from scipy.io import wavfile
import numpy as np
import time
from ridgeplot import ridgeplot

from matplotlib import pyplot as plt

# Notes frequencies 
notes = {
    # Lower octave
    "A": 110.00,
    "B": 123.47,
    "C": 130.81,
    "D": 146.83,
    "E": 164.81,
    "F": 174.61,
    "G": 196.00,
    # Medium octave
    " A ": 220.00,
    " B ": 246.94,
    " C ": 261.63,
    " D ": 293.66,
    " E ": 329.63,
    " F ": 349.23,
    " G ": 392.00,
    # Higher octave
    "  A  ": 440.00,
    "  B  ": 493.88,
    "  C  ": 523.25,
    "  D  ": 587.33,
    "  E  ": 659.26,
    "  F  ": 698.46,
    "  G  ": 783.99,
}

def freq(file, start_index, end_index, min_freq=100, max_freq=800):
    """
    This function takes a wav file and returns the frequency spectrum of the audio.
    file: the wav file to read
    """
    # Open the file and convert to mono
    sr, data = wavfile.read(file)
    if data.ndim > 1:
        data = data[:, 0]
    else:
        pass

    # Return a slice of the data from start_time to end_time
    dataToRead = data[start_index : end_index]

    # Fourier Transform
    N = len(dataToRead)
    yf = rfft(dataToRead)
    xf = rfftfreq(N, 1 / sr)

    # Filter the frequency spectrum
    m = (xf >= min_freq) & (xf <= max_freq)
    xf = xf[m]
    yf = yf[m]
    return xf, yf


def plot_spectrogram(xf, yf, fig_ph, t=0):
    fig = plt.figure(figsize=(10, 3.5))
    # Plot the spectrogram
    ax = fig.add_subplot(111)
    yf_norm = np.abs(yf) / np.max(np.abs(yf))
    ax.plot(xf, yf_norm)
    # Plot the notes
    for note, freq in notes.items():
        ax.axvline(freq, color='black', linestyle='-', alpha=0.2)
        color = 'red' if "C" in note else 'black'
        ax.text(freq, 1.0, note, color=color, fontsize=12, alpha=0.5, ha='center')
    # Display in log scale
    ax.set_xscale('log')
    ax.set_title(f"Time: {t:.2f} s")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude (relative)")
    fig_ph.pyplot(fig)
    return


def page_content():
    st.title("Spectrometer")
    # Capture the audio
    audio_file = st.audio_input("Press here to record")
    # Play de audio
    if audio_file: # audio/wav
        # Get the data info
        sr, data = wavfile.read(audio_file)
        # Compute how many milliseconds are in the audio file
        total_seconds = len(data) / sr
        N = len(data)
        # Show buttons    
        c1, c2 = st.columns(2)
        with c1.container(border=True):
            show_all_button = c1.button("Animated", use_container_width=True)
            step_size = c1.number_input("Step size (s)", value=0.25, min_value=0.10, max_value=total_seconds/2, step=0.1)
        with c2.container(border=True):
            use_params_button = c2.button("Fixed", use_container_width=True)
            c21, c22 = c2.columns(2)
            init_time = c21.number_input("Initial time (s)", value=0.5, min_value=0.0, max_value=total_seconds, step=0.1)
            window_size = c22.number_input("Window size (s)", value=0.5, min_value=0.5, max_value=total_seconds/2, step=0.1)
        fig_ph = st.empty()
        # Play the audio
        if show_all_button:
            # Get the spectrogram
            delta = 2*int(step_size*sr)
            for i in np.arange(0.0, N, int(step_size*sr)):
                min_index = int(max(0, i-delta))
                max_index = int(min(N, i+delta))
                xf, yf = freq(audio_file, min_index, max_index)
                plot_spectrogram(xf, yf, fig_ph, t=i/sr)
                time.sleep(1)
        # Show with fixed parameters
        if use_params_button:
            # Get the spectrogram
            start_index = int(max(0, init_time*sr-window_size*sr))
            end_index = int(min(N, init_time*sr+window_size*sr))
            xf, yf = freq(audio_file, start_index, end_index)
            plot_spectrogram(xf, yf, fig_ph, t=init_time)


page_content()

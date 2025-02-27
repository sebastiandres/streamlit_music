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

def freq(file, start_time, end_time, min_freq=100, max_freq=800):
    """
    This function takes a wav file and returns the frequency spectrum of the audio.
    file: the wav file to read
    start_time: the start time of the audio to read (in milliseconds)
    end_time: the end time of the audio to read (in milliseconds)
    """
    # Open the file and convert to mono
    sr, data = wavfile.read(file)
    if data.ndim > 1:
        data = data[:, 0]
    else:
        pass

    # Return a slice of the data from start_time to end_time
    dataToRead = data[int(start_time * sr / 1000) : int(end_time * sr / 1000) + 1]

    # Fourier Transform
    N = len(dataToRead)
    yf = rfft(dataToRead)
    xf = rfftfreq(N, 1 / sr)

    # Filter the frequency spectrum
    m = (xf >= min_freq) & (xf <= max_freq)
    xf = xf[m]
    yf = yf[m]
    return xf, yf


def plot_spectrogram(xf, yf, fig_ph):
    fig = plt.figure(figsize=(10, 5))
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
    fig_ph.pyplot(fig)
    return

def page_content():
    st.title("Spectrometer")
    c1, c2 = st.columns(2)
    # Capture the audio
    audio_file = c1.audio_input("Press here to record")
    # Play de audio
    if audio_file: # audio/wav
        # Play the audio
        if c2.button("Analyze"):
            # Get the sample rate and data
            sr, data = wavfile.read(audio_file)
            # Compute how many milliseconds are in the audio file
            total_seconds = len(data) / sr
            # Get the spectrogram
            ms = 1000.0
            fig_ph = st.empty()
            for i in np.arange(0.0, total_seconds, 1):
                xf, yf = freq(audio_file, i*ms, (i+1)*ms)
                plot_spectrogram(xf, yf, fig_ph)
                time.sleep(1)
        # Display the spectrogram
        #st.write(xf, yf)
        # 
        #fig = ridge_plot()
        #st.pyplot(fig)



page_content()

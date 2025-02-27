import streamlit as st
from streamlit import session_state as ss # Shortcut for session_state

import os

def page_content():
    st.set_page_config(page_title="Strumlit", page_icon=":musical_note:", layout="wide")
    pages_dict = [
        st.Page(os.path.join("frontend", "spectrometer.py"), title="Spectrometer", icon=":material/airwave:"),
        st.Page(os.path.join("frontend", "strumlit.py"), title="Strumlit", icon=":material/music_note:"),
    ]
    pg = st.navigation(pages_dict)
    pg.run()

page_content()
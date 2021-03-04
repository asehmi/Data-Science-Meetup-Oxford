import streamlit as st

from LayoutAndStyleUtils  import (Grid, Cell, BlockContainerStyler)
BlockContainerStyler().set_default_block_container_style()

from __init__ import session_state, messageboard, check_token

def main():
    is_authenticated = check_token(session_state.token)
    if not is_authenticated:
        return

    st.sidebar.write(f'({session_state.user} logged in)')
    st.sidebar.header('Settings')

    st.title('DuMMMy aPp')
    st.write('## Welcome to the app that does nothing! :smile:')

import streamlit as st

from LayoutAndStyleUtils  import (Grid, Cell, BlockContainerStyler)
BlockContainerStyler().set_default_block_container_style()

from app import session_state, messageboard
from auth0_login_component import check_token

messageboard.empty()

def main():
    is_authenticated = check_token(session_state.token)
    if not is_authenticated:
        messageboard.warning('Please login to use this application.')
        return

    st.sidebar.write(f'({session_state.user} logged in)')
    st.sidebar.header('Settings')

    st.title('DUmmmY ApP')
    st.write('## Welcome to another app that does nothing! :sunglasses:')

import streamlit as st

import auth0_login_component as auth_component

from LayoutAndStyleUtils  import (Grid, Cell, BlockContainerStyler)
BlockContainerStyler().set_default_block_container_style()

from app import messageboard

def main():
    is_authenticated = auth_component.check_token(auth_component.session_state.token)
    if not is_authenticated:
        messageboard.warning('Please login to use this application.')
        return

    st.sidebar.write(f'({auth_component.session_state.user} logged in)')
    st.sidebar.header('Settings')

    st.title('DuMMMy aPp')
    st.write('## Welcome to the app that does nothing! :smile:')

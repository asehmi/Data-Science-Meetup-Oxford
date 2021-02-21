import streamlit as st
import streamlit.components.v1 as components

import settings

from LayoutAndStyleUtils  import (Grid, Cell, BlockContainerStyler)
BlockContainerStyler().set_default_block_container_style()

from app import session_state, messageboard
messageboard.empty()

from auth0_login_component import check_token, run_login_component

def main():
    is_authenticated = check_token(session_state.token)
    if not is_authenticated:
        messageboard.info('Thanks! Signed out.')
    else:
        run_login_component()
        components.iframe(src=f'{settings.API_BASE_URL}/api/logout', width=None, height=0, scrolling=False)
        session_state.token={'value': None, 'expiry': None}
        session_state.user=None
        session_state.email=None

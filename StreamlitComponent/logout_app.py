import streamlit as st
import streamlit.components.v1 as components

from LayoutAndStyleUtils  import (Grid, Cell, BlockContainerStyler)
BlockContainerStyler().set_default_block_container_style()

from app import messageboard
messageboard.empty()

import auth0_login_component as auth_component

def main():
    is_authenticated = auth_component.check_token(auth_component.session_state.token)
    if not is_authenticated:
        messageboard.info('Thanks! Signed out.')
    else:
        auth_component.run_login_component()
        components.iframe(src='http://localhost:3001/api/logout', width=None, height=0, scrolling=False)

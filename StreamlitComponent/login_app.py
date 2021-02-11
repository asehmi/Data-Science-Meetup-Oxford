import streamlit as st
import streamlit.components.v1 as components

from LayoutAndStyleUtils  import (Grid, Cell, BlockContainerStyler)
BlockContainerStyler().set_default_block_container_style()

from app import messageboard
messageboard.empty()

import auth0_login_component as auth_component

def main():
    is_authenticated = auth_component.check_token(auth_component.session_state.token)
    if is_authenticated:
        # token_value = auth_component.session_state.token['value']
        # token_expiry = datetime.fromtimestamp(int(auth_component.session_state.token['expiry']))
        # messageboard.info(f'You are already logged in.\n\nToken is {token_value[0:30]}... | Expires at {token_expiry}')
        user = auth_component.session_state.user
        messageboard.info(f'{user}, you\'re logged in and authorized to use the app.')
    else:
        auth_component.run_login_component()
        components.iframe(src='http://localhost:3001/api/login', width=None, height=600, scrolling=True)

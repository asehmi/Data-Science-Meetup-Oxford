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
    if is_authenticated:
        # token_value = auth_component.session_state.token['value']
        # token_expiry = datetime.fromtimestamp(int(auth_component.session_state.token['expiry']))
        # messageboard.info(f'You are already logged in.\n\nToken is {token_value[0:30]}... | Expires at {token_expiry}')
        messageboard.info(f'You\'re logged in and authorized to use the app.')
    else:
        run_login_component()
        components.iframe(src=f'{settings.API_BASE_URL}/api/login', width=None, height=600, scrolling=True)

import streamlit as st

import settings

import ptvsd
ptvsd.enable_attach(address=('localhost', 6790))
# ptvsd.wait_for_attach() # Only include this line if you always want to manually attach the debugger

from LayoutAndStyleUtils  import (Grid, Cell, BlockContainerStyler)
BlockContainerStyler().set_default_block_container_style()

from __init__ import session_state, messageboard, check_token
import auth_component_handler

# --------------------------------------------------------------------------------

# import must come after messageboard as these apps use app.messageboard
import dumb_app, dumber_app

# --------------------------------------------------------------------------------

# !! Appears to throw errors if initialized using messageboard.empty() !!
messageboard = st.empty()

if settings.USE_AUTHENTICATION:
    AUTH_LABEL = 'Authenticate'

    label = AUTH_LABEL
    if (check_token(session_state.token)):
        label = f'{session_state.user} ({session_state.email})'
    with st.beta_expander(label):
        auth_component_handler.init()
        # force a rerun to flip the expander label
        logged_in_but_showing_login_label = (check_token(session_state.token) and label == AUTH_LABEL)
        logged_out_but_showing_logged_in_label = (not check_token(session_state.token) and label != AUTH_LABEL)
        if (logged_in_but_showing_login_label or logged_out_but_showing_logged_in_label):
            st.experimental_rerun()

# --------------------------------------------------------------------------------

def main():
    pages = {
        'DuMMMy aPp 1': [dumb_app.main],      # DUMMY APP 1
        'DUmmmY ApP 2': [dumber_app.main],    # DUMMY APP 2
    }

    def _launch_apps():
        messageboard.empty()
        choice = st.sidebar.radio('What do you want to do?', tuple(pages.keys()))
        pages[choice][0](title=choice, *pages[choice][1:])

    if settings.USE_AUTHENTICATION:
        if (check_token(session_state.token)):
            _launch_apps()
        else:
            messageboard.info('Please login below...')
    else:
        _launch_apps()

    # ABOUT
    st.sidebar.header('About')
    st.sidebar.info('Auth0 authentication Streamlit component demo.\n\n' + \
        '(c) 2021. Oxford Economics Ltd. All rights reserved.')
    st.sidebar.markdown('---')

    # Style
    st.sidebar.markdown('---')
    if st.sidebar.checkbox('Configure Style'):
        BlockContainerStyler().block_container_styler()

if __name__ == '__main__':
    st.sidebar.image('./images/logo.jpg', output_format='jpg')
    main()

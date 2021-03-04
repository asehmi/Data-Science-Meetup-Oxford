import streamlit as st

import settings

import ptvsd
ptvsd.enable_attach(address=('localhost', 6790))
# ptvsd.wait_for_attach() # Only include this line if you always want to manually attach the debugger

from LayoutAndStyleUtils  import (Grid, Cell, BlockContainerStyler)
BlockContainerStyler().set_default_block_container_style()

from __init__ import session_state, messageboard, check_token

# --------------------------------------------------------------------------------

# import must come after messageboard as these apps use app.messageboard
import dumb_app, dumber_app

# --------------------------------------------------------------------------------

if settings.USE_AUTHENTICATION:
    from auth0_login_component import run_login_component
    run_login_component()

# --------------------------------------------------------------------------------

def main():
    pages = {
        'DuMMMy aPp [1]': [dumb_app.main],      # DUMMY APP 1
        'DUmmmY ApP [2]': [dumber_app.main],    # DUMMY APP 2
    }

    choice = st.sidebar.radio('What do you want to do?', tuple(pages.keys()))
    pages[choice][0](*pages[choice][1:])

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
